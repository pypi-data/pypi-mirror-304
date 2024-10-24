"""FaceGearMeshSystemDeflection"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.system_deflections import _2846

_FACE_GEAR_MESH_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "FaceGearMeshSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.conical import _1200
    from mastapy._private.gears.rating.face import _460
    from mastapy._private.system_model.analyses_and_results import _2736, _2738, _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7710,
        _7712,
        _7713,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4193
    from mastapy._private.system_model.analyses_and_results.static_loads import _7036
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2814,
        _2854,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2366

    Self = TypeVar("Self", bound="FaceGearMeshSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="FaceGearMeshSystemDeflection._Cast_FaceGearMeshSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("FaceGearMeshSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FaceGearMeshSystemDeflection:
    """Special nested class for casting FaceGearMeshSystemDeflection to subclasses."""

    __parent__: "FaceGearMeshSystemDeflection"

    @property
    def gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2846.GearMeshSystemDeflection":
        return self.__parent__._cast(_2846.GearMeshSystemDeflection)

    @property
    def inter_mountable_component_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2854.InterMountableComponentConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2854,
        )

        return self.__parent__._cast(
            _2854.InterMountableComponentConnectionSystemDeflection
        )

    @property
    def connection_system_deflection(
        self: "CastSelf",
    ) -> "_2814.ConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2814,
        )

        return self.__parent__._cast(_2814.ConnectionSystemDeflection)

    @property
    def connection_fe_analysis(self: "CastSelf") -> "_7712.ConnectionFEAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7712,
        )

        return self.__parent__._cast(_7712.ConnectionFEAnalysis)

    @property
    def connection_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7713.ConnectionStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7713,
        )

        return self.__parent__._cast(_7713.ConnectionStaticLoadAnalysisCase)

    @property
    def connection_analysis_case(self: "CastSelf") -> "_7710.ConnectionAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7710,
        )

        return self.__parent__._cast(_7710.ConnectionAnalysisCase)

    @property
    def connection_analysis(self: "CastSelf") -> "_2736.ConnectionAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2736

        return self.__parent__._cast(_2736.ConnectionAnalysis)

    @property
    def design_entity_single_context_analysis(
        self: "CastSelf",
    ) -> "_2740.DesignEntitySingleContextAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2740

        return self.__parent__._cast(_2740.DesignEntitySingleContextAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2738.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2738

        return self.__parent__._cast(_2738.DesignEntityAnalysis)

    @property
    def face_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "FaceGearMeshSystemDeflection":
        return self.__parent__

    def __getattr__(self: "CastSelf", name: str) -> "Any":
        try:
            return self.__getattribute__(name)
        except AttributeError:
            class_name = utility.camel(name)
            raise CastException(
                f'Detected an invalid cast. Cannot cast to type "{class_name}"'
            ) from None


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class FaceGearMeshSystemDeflection(_2846.GearMeshSystemDeflection):
    """FaceGearMeshSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FACE_GEAR_MESH_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def angular_misalignment_in_surface_of_action(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AngularMisalignmentInSurfaceOfAction"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def linear_misalignment_in_surface_of_action(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LinearMisalignmentInSurfaceOfAction"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def pinion_angular_misalignment_in_surface_of_action(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PinionAngularMisalignmentInSurfaceOfAction"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def wheel_angular_misalignment_in_surface_of_action(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "WheelAngularMisalignmentInSurfaceOfAction"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def rating(self: "Self") -> "_460.FaceGearMeshRating":
        """mastapy.gears.rating.face.FaceGearMeshRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Rating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_detailed_analysis(self: "Self") -> "_460.FaceGearMeshRating":
        """mastapy.gears.rating.face.FaceGearMeshRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDetailedAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_design(self: "Self") -> "_2366.FaceGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.FaceGearMesh

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_load_case(self: "Self") -> "_7036.FaceGearMeshLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.FaceGearMeshLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def misalignments_pinion(self: "Self") -> "_1200.ConicalMeshMisalignments":
        """mastapy.gears.gear_designs.conical.ConicalMeshMisalignments

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MisalignmentsPinion")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def misalignments_total(self: "Self") -> "_1200.ConicalMeshMisalignments":
        """mastapy.gears.gear_designs.conical.ConicalMeshMisalignments

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MisalignmentsTotal")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def misalignments_wheel(self: "Self") -> "_1200.ConicalMeshMisalignments":
        """mastapy.gears.gear_designs.conical.ConicalMeshMisalignments

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MisalignmentsWheel")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def power_flow_results(self: "Self") -> "_4193.FaceGearMeshPowerFlow":
        """mastapy.system_model.analyses_and_results.power_flows.FaceGearMeshPowerFlow

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerFlowResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_FaceGearMeshSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_FaceGearMeshSystemDeflection
        """
        return _Cast_FaceGearMeshSystemDeflection(self)
