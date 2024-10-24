"""IndependentReportablePropertiesBase"""

from __future__ import annotations

from typing import ClassVar, Generic, TYPE_CHECKING, TypeVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import

_INDEPENDENT_REPORTABLE_PROPERTIES_BASE = python_net_import(
    "SMT.MastaAPI.Utility", "IndependentReportablePropertiesBase"
)

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.bearings.bearing_results import _1999
    from mastapy._private.bearings.bearing_results.rolling import _2030, _2124
    from mastapy._private.bearings.tolerances import _1971
    from mastapy._private.electric_machines import _1303
    from mastapy._private.electric_machines.load_cases_and_analyses import _1425
    from mastapy._private.gears import _358
    from mastapy._private.gears.gear_designs.cylindrical import (
        _1052,
        _1083,
        _1091,
        _1092,
        _1095,
        _1096,
        _1104,
        _1112,
        _1114,
        _1118,
        _1122,
    )
    from mastapy._private.geometry import _321
    from mastapy._private.materials.efficiency import _310
    from mastapy._private.math_utility.measured_data import _1614, _1615, _1616
    from mastapy._private.system_model.analyses_and_results.static_loads import _6961
    from mastapy._private.utility import _1649

    Self = TypeVar("Self", bound="IndependentReportablePropertiesBase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="IndependentReportablePropertiesBase._Cast_IndependentReportablePropertiesBase",
    )

T = TypeVar("T", bound="IndependentReportablePropertiesBase")

__docformat__ = "restructuredtext en"
__all__ = ("IndependentReportablePropertiesBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_IndependentReportablePropertiesBase:
    """Special nested class for casting IndependentReportablePropertiesBase to subclasses."""

    __parent__: "IndependentReportablePropertiesBase"

    @property
    def oil_pump_detail(self: "CastSelf") -> "_310.OilPumpDetail":
        from mastapy._private.materials.efficiency import _310

        return self.__parent__._cast(_310.OilPumpDetail)

    @property
    def packaging_limits(self: "CastSelf") -> "_321.PackagingLimits":
        from mastapy._private.geometry import _321

        return self.__parent__._cast(_321.PackagingLimits)

    @property
    def specification_for_the_effect_of_oil_kinematic_viscosity(
        self: "CastSelf",
    ) -> "_358.SpecificationForTheEffectOfOilKinematicViscosity":
        from mastapy._private.gears import _358

        return self.__parent__._cast(
            _358.SpecificationForTheEffectOfOilKinematicViscosity
        )

    @property
    def cylindrical_gear_micro_geometry_settings(
        self: "CastSelf",
    ) -> "_1052.CylindricalGearMicroGeometrySettings":
        from mastapy._private.gears.gear_designs.cylindrical import _1052

        return self.__parent__._cast(_1052.CylindricalGearMicroGeometrySettings)

    @property
    def hardened_material_properties(
        self: "CastSelf",
    ) -> "_1083.HardenedMaterialProperties":
        from mastapy._private.gears.gear_designs.cylindrical import _1083

        return self.__parent__._cast(_1083.HardenedMaterialProperties)

    @property
    def ltca_load_case_modifiable_settings(
        self: "CastSelf",
    ) -> "_1091.LTCALoadCaseModifiableSettings":
        from mastapy._private.gears.gear_designs.cylindrical import _1091

        return self.__parent__._cast(_1091.LTCALoadCaseModifiableSettings)

    @property
    def ltca_settings(self: "CastSelf") -> "_1092.LTCASettings":
        from mastapy._private.gears.gear_designs.cylindrical import _1092

        return self.__parent__._cast(_1092.LTCASettings)

    @property
    def micropitting(self: "CastSelf") -> "_1095.Micropitting":
        from mastapy._private.gears.gear_designs.cylindrical import _1095

        return self.__parent__._cast(_1095.Micropitting)

    @property
    def muller_residual_stress_definition(
        self: "CastSelf",
    ) -> "_1096.MullerResidualStressDefinition":
        from mastapy._private.gears.gear_designs.cylindrical import _1096

        return self.__parent__._cast(_1096.MullerResidualStressDefinition)

    @property
    def scuffing(self: "CastSelf") -> "_1104.Scuffing":
        from mastapy._private.gears.gear_designs.cylindrical import _1104

        return self.__parent__._cast(_1104.Scuffing)

    @property
    def surface_roughness(self: "CastSelf") -> "_1112.SurfaceRoughness":
        from mastapy._private.gears.gear_designs.cylindrical import _1112

        return self.__parent__._cast(_1112.SurfaceRoughness)

    @property
    def tiff_analysis_settings(self: "CastSelf") -> "_1114.TiffAnalysisSettings":
        from mastapy._private.gears.gear_designs.cylindrical import _1114

        return self.__parent__._cast(_1114.TiffAnalysisSettings)

    @property
    def tooth_flank_fracture_analysis_settings(
        self: "CastSelf",
    ) -> "_1118.ToothFlankFractureAnalysisSettings":
        from mastapy._private.gears.gear_designs.cylindrical import _1118

        return self.__parent__._cast(_1118.ToothFlankFractureAnalysisSettings)

    @property
    def usage(self: "CastSelf") -> "_1122.Usage":
        from mastapy._private.gears.gear_designs.cylindrical import _1122

        return self.__parent__._cast(_1122.Usage)

    @property
    def eccentricity(self: "CastSelf") -> "_1303.Eccentricity":
        from mastapy._private.electric_machines import _1303

        return self.__parent__._cast(_1303.Eccentricity)

    @property
    def temperatures(self: "CastSelf") -> "_1425.Temperatures":
        from mastapy._private.electric_machines.load_cases_and_analyses import _1425

        return self.__parent__._cast(_1425.Temperatures)

    @property
    def lookup_table_base(self: "CastSelf") -> "_1614.LookupTableBase":
        from mastapy._private.math_utility.measured_data import _1614

        return self.__parent__._cast(_1614.LookupTableBase)

    @property
    def onedimensional_function_lookup_table(
        self: "CastSelf",
    ) -> "_1615.OnedimensionalFunctionLookupTable":
        from mastapy._private.math_utility.measured_data import _1615

        return self.__parent__._cast(_1615.OnedimensionalFunctionLookupTable)

    @property
    def twodimensional_function_lookup_table(
        self: "CastSelf",
    ) -> "_1616.TwodimensionalFunctionLookupTable":
        from mastapy._private.math_utility.measured_data import _1616

        return self.__parent__._cast(_1616.TwodimensionalFunctionLookupTable)

    @property
    def skf_loss_moment_multipliers(
        self: "CastSelf",
    ) -> "_1649.SKFLossMomentMultipliers":
        from mastapy._private.utility import _1649

        return self.__parent__._cast(_1649.SKFLossMomentMultipliers)

    @property
    def roundness_specification(self: "CastSelf") -> "_1971.RoundnessSpecification":
        from mastapy._private.bearings.tolerances import _1971

        return self.__parent__._cast(_1971.RoundnessSpecification)

    @property
    def equivalent_load_factors(self: "CastSelf") -> "_1999.EquivalentLoadFactors":
        from mastapy._private.bearings.bearing_results import _1999

        return self.__parent__._cast(_1999.EquivalentLoadFactors)

    @property
    def iso14179_settings_per_bearing_type(
        self: "CastSelf",
    ) -> "_2030.ISO14179SettingsPerBearingType":
        from mastapy._private.bearings.bearing_results.rolling import _2030

        return self.__parent__._cast(_2030.ISO14179SettingsPerBearingType)

    @property
    def rolling_bearing_friction_coefficients(
        self: "CastSelf",
    ) -> "_2124.RollingBearingFrictionCoefficients":
        from mastapy._private.bearings.bearing_results.rolling import _2124

        return self.__parent__._cast(_2124.RollingBearingFrictionCoefficients)

    @property
    def additional_acceleration_options(
        self: "CastSelf",
    ) -> "_6961.AdditionalAccelerationOptions":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6961,
        )

        return self.__parent__._cast(_6961.AdditionalAccelerationOptions)

    @property
    def independent_reportable_properties_base(
        self: "CastSelf",
    ) -> "IndependentReportablePropertiesBase":
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
class IndependentReportablePropertiesBase(_0.APIBase, Generic[T]):
    """IndependentReportablePropertiesBase

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _INDEPENDENT_REPORTABLE_PROPERTIES_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_IndependentReportablePropertiesBase":
        """Cast to another type.

        Returns:
            _Cast_IndependentReportablePropertiesBase
        """
        return _Cast_IndependentReportablePropertiesBase(self)
