"""VirtualComponentMultibodyDynamicsAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private._math.vector_3d import Vector3D
from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5594

_VIRTUAL_COMPONENT_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses",
    "VirtualComponentMultibodyDynamicsAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7721,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
        _5532,
        _5587,
        _5591,
        _5597,
        _5604,
        _5605,
        _5645,
    )
    from mastapy._private.system_model.part_model import _2538

    Self = TypeVar("Self", bound="VirtualComponentMultibodyDynamicsAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="VirtualComponentMultibodyDynamicsAnalysis._Cast_VirtualComponentMultibodyDynamicsAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("VirtualComponentMultibodyDynamicsAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_VirtualComponentMultibodyDynamicsAnalysis:
    """Special nested class for casting VirtualComponentMultibodyDynamicsAnalysis to subclasses."""

    __parent__: "VirtualComponentMultibodyDynamicsAnalysis"

    @property
    def mountable_component_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5594.MountableComponentMultibodyDynamicsAnalysis":
        return self.__parent__._cast(_5594.MountableComponentMultibodyDynamicsAnalysis)

    @property
    def component_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5532.ComponentMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5532,
        )

        return self.__parent__._cast(_5532.ComponentMultibodyDynamicsAnalysis)

    @property
    def part_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5597.PartMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5597,
        )

        return self.__parent__._cast(_5597.PartMultibodyDynamicsAnalysis)

    @property
    def part_time_series_load_analysis_case(
        self: "CastSelf",
    ) -> "_7721.PartTimeSeriesLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7721,
        )

        return self.__parent__._cast(_7721.PartTimeSeriesLoadAnalysisCase)

    @property
    def part_analysis_case(self: "CastSelf") -> "_7717.PartAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7717,
        )

        return self.__parent__._cast(_7717.PartAnalysisCase)

    @property
    def part_analysis(self: "CastSelf") -> "_2744.PartAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2744

        return self.__parent__._cast(_2744.PartAnalysis)

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
    def mass_disc_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5587.MassDiscMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5587,
        )

        return self.__parent__._cast(_5587.MassDiscMultibodyDynamicsAnalysis)

    @property
    def measurement_component_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5591.MeasurementComponentMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5591,
        )

        return self.__parent__._cast(
            _5591.MeasurementComponentMultibodyDynamicsAnalysis
        )

    @property
    def point_load_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5604.PointLoadMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5604,
        )

        return self.__parent__._cast(_5604.PointLoadMultibodyDynamicsAnalysis)

    @property
    def power_load_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5605.PowerLoadMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5605,
        )

        return self.__parent__._cast(_5605.PowerLoadMultibodyDynamicsAnalysis)

    @property
    def unbalanced_mass_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5645.UnbalancedMassMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5645,
        )

        return self.__parent__._cast(_5645.UnbalancedMassMultibodyDynamicsAnalysis)

    @property
    def virtual_component_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "VirtualComponentMultibodyDynamicsAnalysis":
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
class VirtualComponentMultibodyDynamicsAnalysis(
    _5594.MountableComponentMultibodyDynamicsAnalysis
):
    """VirtualComponentMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _VIRTUAL_COMPONENT_MULTIBODY_DYNAMICS_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def acceleration_translation_local_coordinate_system(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AccelerationTranslationLocalCoordinateSystem"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    def displacement_translation_local_coordinate_system(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "DisplacementTranslationLocalCoordinateSystem"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    def velocity_translation_local_coordinate_system(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "VelocityTranslationLocalCoordinateSystem"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    def component_design(self: "Self") -> "_2538.VirtualComponent":
        """mastapy.system_model.part_model.VirtualComponent

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_VirtualComponentMultibodyDynamicsAnalysis":
        """Cast to another type.

        Returns:
            _Cast_VirtualComponentMultibodyDynamicsAnalysis
        """
        return _Cast_VirtualComponentMultibodyDynamicsAnalysis(self)
