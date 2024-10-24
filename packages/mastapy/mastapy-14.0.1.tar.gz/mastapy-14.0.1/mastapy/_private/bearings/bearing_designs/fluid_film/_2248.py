"""PlainOilFedJournalBearing"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.bearings.bearing_designs.fluid_film import _2246

_PLAIN_OIL_FED_JOURNAL_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.FluidFilm", "PlainOilFedJournalBearing"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.bearings import _1940
    from mastapy._private.bearings.bearing_designs import _2184, _2185, _2188
    from mastapy._private.bearings.bearing_designs.fluid_film import _2237, _2238, _2239

    Self = TypeVar("Self", bound="PlainOilFedJournalBearing")
    CastSelf = TypeVar(
        "CastSelf", bound="PlainOilFedJournalBearing._Cast_PlainOilFedJournalBearing"
    )


__docformat__ = "restructuredtext en"
__all__ = ("PlainOilFedJournalBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlainOilFedJournalBearing:
    """Special nested class for casting PlainOilFedJournalBearing to subclasses."""

    __parent__: "PlainOilFedJournalBearing"

    @property
    def plain_journal_bearing(self: "CastSelf") -> "_2246.PlainJournalBearing":
        return self.__parent__._cast(_2246.PlainJournalBearing)

    @property
    def detailed_bearing(self: "CastSelf") -> "_2185.DetailedBearing":
        from mastapy._private.bearings.bearing_designs import _2185

        return self.__parent__._cast(_2185.DetailedBearing)

    @property
    def non_linear_bearing(self: "CastSelf") -> "_2188.NonLinearBearing":
        from mastapy._private.bearings.bearing_designs import _2188

        return self.__parent__._cast(_2188.NonLinearBearing)

    @property
    def bearing_design(self: "CastSelf") -> "_2184.BearingDesign":
        from mastapy._private.bearings.bearing_designs import _2184

        return self.__parent__._cast(_2184.BearingDesign)

    @property
    def plain_oil_fed_journal_bearing(self: "CastSelf") -> "PlainOilFedJournalBearing":
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
class PlainOilFedJournalBearing(_2246.PlainJournalBearing):
    """PlainOilFedJournalBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLAIN_OIL_FED_JOURNAL_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def feed_type(self: "Self") -> "_1940.JournalOilFeedType":
        """mastapy.bearings.JournalOilFeedType"""
        temp = pythonnet_property_get(self.wrapped, "FeedType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Bearings.JournalOilFeedType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings._1940", "JournalOilFeedType"
        )(value)

    @feed_type.setter
    @enforce_parameter_types
    def feed_type(self: "Self", value: "_1940.JournalOilFeedType") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Bearings.JournalOilFeedType"
        )
        pythonnet_property_set(self.wrapped, "FeedType", value)

    @property
    def land_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LandWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    def number_of_axial_points_for_pressure_distribution(
        self: "Self",
    ) -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfAxialPointsForPressureDistribution"
        )

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @number_of_axial_points_for_pressure_distribution.setter
    @enforce_parameter_types
    def number_of_axial_points_for_pressure_distribution(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "NumberOfAxialPointsForPressureDistribution", value
        )

    @property
    def number_of_circumferential_points_for_pressure_distribution(
        self: "Self",
    ) -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfCircumferentialPointsForPressureDistribution"
        )

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @number_of_circumferential_points_for_pressure_distribution.setter
    @enforce_parameter_types
    def number_of_circumferential_points_for_pressure_distribution(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "NumberOfCircumferentialPointsForPressureDistribution", value
        )

    @property
    def axial_groove_oil_feed(self: "Self") -> "_2237.AxialGrooveJournalBearing":
        """mastapy.bearings.bearing_designs.fluid_film.AxialGrooveJournalBearing

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AxialGrooveOilFeed")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def axial_hole_oil_feed(self: "Self") -> "_2238.AxialHoleJournalBearing":
        """mastapy.bearings.bearing_designs.fluid_film.AxialHoleJournalBearing

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AxialHoleOilFeed")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def circumferential_groove_oil_feed(
        self: "Self",
    ) -> "_2239.CircumferentialFeedJournalBearing":
        """mastapy.bearings.bearing_designs.fluid_film.CircumferentialFeedJournalBearing

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CircumferentialGrooveOilFeed")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_PlainOilFedJournalBearing":
        """Cast to another type.

        Returns:
            _Cast_PlainOilFedJournalBearing
        """
        return _Cast_PlainOilFedJournalBearing(self)
