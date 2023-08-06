from collections import OrderedDict

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from nautobot.core.api import (
    ChoiceField,
    SerializedPKRelatedField,
)
from nautobot.dcim.api.nested_serializers import (
    NestedDeviceSerializer,
    NestedLocationSerializer,
)
from nautobot.dcim.models import Device
from nautobot.extras.api.serializers import (
    NautobotModelSerializer,
    RoleModelSerializerMixin,
    StatusModelSerializerMixin,
    TaggedModelSerializerMixin,
)
from nautobot.ipam.choices import PrefixTypeChoices, ServiceProtocolChoices
from nautobot.ipam import constants
from nautobot.ipam.models import (
    IPAddress,
    Namespace,
    Prefix,
    RIR,
    RouteTarget,
    Service,
    VLAN,
    VLANGroup,
    VRF,
)
from nautobot.tenancy.api.nested_serializers import NestedTenantSerializer
from nautobot.virtualization.api.nested_serializers import (
    NestedVirtualMachineSerializer,
)

# Not all of these variable(s) are actually used anywhere in this file, but are required for the
# automagically replacing a Serializer with its corresponding NestedSerializer.
from .nested_serializers import (  # noqa: F401
    IPFieldSerializer,
    NestedIPAddressSerializer,
    NestedNamespaceSerializer,
    NestedPrefixSerializer,
    NestedRIRSerializer,
    NestedRouteTargetSerializer,
    NestedServiceSerializer,
    NestedVLANGroupSerializer,
    NestedVLANSerializer,
    NestedVRFSerializer,
)

#
# Namespaces
#


class NamespaceSerializer(NautobotModelSerializer, TaggedModelSerializerMixin):
    url = serializers.HyperlinkedIdentityField(view_name="ipam-api:namespace-detail")

    class Meta:
        model = Namespace
        fields = ["url", "name", "description", "location"]


#
# VRFs
#


class VRFSerializer(NautobotModelSerializer, TaggedModelSerializerMixin):
    url = serializers.HyperlinkedIdentityField(view_name="ipam-api:vrf-detail")
    tenant = NestedTenantSerializer(required=False, allow_null=True)
    import_targets = SerializedPKRelatedField(
        queryset=RouteTarget.objects.all(),
        serializer=NestedRouteTargetSerializer,
        required=False,
        many=True,
    )
    export_targets = SerializedPKRelatedField(
        queryset=RouteTarget.objects.all(),
        serializer=NestedRouteTargetSerializer,
        required=False,
        many=True,
    )
    devices = SerializedPKRelatedField(
        queryset=Device.objects.all(),
        serializer=NestedDeviceSerializer,
        required=False,
        many=True,
    )
    prefixes = SerializedPKRelatedField(
        queryset=Prefix.objects.all(),
        serializer=NestedPrefixSerializer,
        required=False,
        many=True,
    )
    namespace = NestedNamespaceSerializer()
    # FIXME(jathan); These two values come from annotation on `VRFViewSet.queryset`
    # ipaddress_count = serializers.IntegerField(read_only=True)
    # prefix_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = VRF
        fields = [
            "url",
            "name",
            "rd",
            "namespace",
            "tenant",
            "description",
            "import_targets",
            "export_targets",
            "devices",
            "prefixes",
            # "ipaddress_count",
            # "prefix_count",
        ]


#
# Route targets
#


class RouteTargetSerializer(NautobotModelSerializer, TaggedModelSerializerMixin):
    url = serializers.HyperlinkedIdentityField(view_name="ipam-api:routetarget-detail")
    tenant = NestedTenantSerializer(required=False, allow_null=True)

    class Meta:
        model = RouteTarget
        fields = [
            "url",
            "name",
            "tenant",
            "description",
        ]


#
# RIRs
#


class RIRSerializer(NautobotModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="ipam-api:rir-detail")
    assigned_prefix_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = RIR
        fields = [
            "url",
            "name",
            "is_private",
            "description",
            "assigned_prefix_count",
        ]


#
# VLANs
#


class VLANGroupSerializer(NautobotModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="ipam-api:vlangroup-detail")
    location = NestedLocationSerializer(required=False, allow_null=True)
    vlan_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = VLANGroup
        fields = [
            "url",
            "name",
            "slug",
            "location",
            "description",
            "vlan_count",
        ]
        # 2.0 TODO: Remove if/when slug is globally unique. This would be a breaking change.
        validators = []

    def validate(self, data):
        # Validate uniqueness of name and slug if a location has been assigned.
        # 2.0 TODO: Remove if/when slug is globally unique. This would be a breaking change.
        if data.get("location", None):
            for field in ["name", "slug"]:
                validator = UniqueTogetherValidator(queryset=VLANGroup.objects.all(), fields=("location", field))
                validator(data, self)

        # Enforce model validation
        super().validate(data)

        return data


class VLANSerializer(
    NautobotModelSerializer, TaggedModelSerializerMixin, StatusModelSerializerMixin, RoleModelSerializerMixin
):
    url = serializers.HyperlinkedIdentityField(view_name="ipam-api:vlan-detail")
    location = NestedLocationSerializer(required=False, allow_null=True)
    vlan_group = NestedVLANGroupSerializer(required=False, allow_null=True)
    tenant = NestedTenantSerializer(required=False, allow_null=True)
    prefix_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = VLAN
        fields = [
            "url",
            "location",
            "vlan_group",
            "vid",
            "name",
            "tenant",
            "status",
            "role",
            "description",
            "prefix_count",
        ]
        validators = []

    def validate(self, data):
        # Validate uniqueness of vid and name if a group has been assigned.
        if data.get("vlan_group", None):
            for field in ["vid", "name"]:
                validator = UniqueTogetherValidator(queryset=VLAN.objects.all(), fields=("vlan_group", field))
                validator(data, self)

        # Enforce model validation
        super().validate(data)

        return data


#
# Prefixes
#


class PrefixSerializer(
    NautobotModelSerializer, TaggedModelSerializerMixin, StatusModelSerializerMixin, RoleModelSerializerMixin
):
    url = serializers.HyperlinkedIdentityField(view_name="ipam-api:prefix-detail")
    prefix = IPFieldSerializer()
    type = ChoiceField(choices=PrefixTypeChoices, default=PrefixTypeChoices.TYPE_NETWORK)
    location = NestedLocationSerializer(required=False, allow_null=True)
    tenant = NestedTenantSerializer(required=False, allow_null=True)
    vlan = NestedVLANSerializer(required=False, allow_null=True)
    rir = NestedRIRSerializer(required=False, allow_null=True)
    namespace = NestedNamespaceSerializer()
    vrfs = NestedVRFSerializer(required=False, allow_null=True, many=True)

    class Meta:
        model = Prefix
        fields = [
            "url",
            "ip_version",
            "prefix",
            "type",
            "location",
            "vrfs",
            "namespace",
            "tenant",
            "vlan",
            "status",
            "role",
            "rir",
            "date_allocated",
            "description",
        ]
        read_only_fields = ["ip_version"]


class PrefixLengthSerializer(serializers.Serializer):
    prefix_length = serializers.IntegerField()

    def to_internal_value(self, data):
        requested_prefix = data.get("prefix_length")
        if requested_prefix is None:
            raise serializers.ValidationError({"prefix_length": "this field can not be missing"})
        if not isinstance(requested_prefix, int):
            raise serializers.ValidationError({"prefix_length": "this field must be int type"})

        prefix = self.context.get("prefix")
        if prefix.ip_version == 4 and requested_prefix > 32:
            raise serializers.ValidationError({"prefix_length": f"Invalid prefix length ({requested_prefix}) for IPv4"})
        elif prefix.ip_version == 6 and requested_prefix > 128:
            raise serializers.ValidationError({"prefix_length": f"Invalid prefix length ({requested_prefix}) for IPv6"})
        return data


class AvailablePrefixSerializer(serializers.Serializer):
    """
    Representation of a prefix which does not exist in the database.
    """

    ip_version = serializers.IntegerField(read_only=True)
    prefix = serializers.CharField(read_only=True)
    namespace = NestedNamespaceSerializer(read_only=True)

    def to_representation(self, instance):
        return OrderedDict(
            [
                ("ip_version", instance.version),
                ("prefix", str(instance)),
                ("namepace", instance.namespace),
            ]
        )


#
# IP addresses
#


class IPAddressSerializer(
    NautobotModelSerializer, TaggedModelSerializerMixin, StatusModelSerializerMixin, RoleModelSerializerMixin
):
    url = serializers.HyperlinkedIdentityField(view_name="ipam-api:ipaddress-detail")
    address = IPFieldSerializer()
    tenant = NestedTenantSerializer(required=False, allow_null=True)
    nat_inside = NestedIPAddressSerializer(required=False, allow_null=True)
    nat_outside_list = NestedIPAddressSerializer(read_only=True, many=True)

    class Meta:
        model = IPAddress
        fields = [
            "url",
            "ip_version",
            "address",
            "tenant",
            "status",
            "role",
            "nat_inside",
            "nat_outside_list",
            "dns_name",
            "description",
        ]
        read_only_fields = ["ip_version"]


class AvailableIPSerializer(serializers.Serializer):
    """
    Representation of an IP address which does not exist in the database.
    """

    ip_version = serializers.IntegerField(read_only=True)
    address = serializers.CharField(read_only=True)
    namespace = NestedNamespaceSerializer(read_only=True)
    # TODO: Should be requesting a prefix instead

    def to_representation(self, instance):
        return OrderedDict(
            [
                ("ip_verison", self.context["prefix"].version),
                ("address", f"{instance}/{self.context['prefix'].prefixlen}"),
                ("namespace", instance.namespace),
            ]
        )


#
# Services
#


class ServiceSerializer(NautobotModelSerializer, TaggedModelSerializerMixin):
    url = serializers.HyperlinkedIdentityField(view_name="ipam-api:service-detail")
    device = NestedDeviceSerializer(required=False, allow_null=True)
    virtual_machine = NestedVirtualMachineSerializer(required=False, allow_null=True)
    protocol = ChoiceField(choices=ServiceProtocolChoices, required=False)
    ip_addresses = SerializedPKRelatedField(
        queryset=IPAddress.objects.all(),
        serializer=NestedIPAddressSerializer,
        required=False,
        many=True,
    )
    ports = serializers.ListField(
        child=serializers.IntegerField(
            min_value=constants.SERVICE_PORT_MIN,
            max_value=constants.SERVICE_PORT_MAX,
        )
    )

    class Meta:
        model = Service
        fields = [
            "url",
            "device",
            "virtual_machine",
            "name",
            "ports",
            "protocol",
            "ip_addresses",
            "description",
        ]
