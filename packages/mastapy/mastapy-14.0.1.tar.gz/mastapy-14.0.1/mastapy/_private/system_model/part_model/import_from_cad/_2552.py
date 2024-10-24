"""AbstractShaftFromCAD"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model.import_from_cad import _2554

_ABSTRACT_SHAFT_FROM_CAD = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.ImportFromCAD", "AbstractShaftFromCAD"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.part_model.import_from_cad import _2564, _2568

    Self = TypeVar("Self", bound="AbstractShaftFromCAD")
    CastSelf = TypeVar(
        "CastSelf", bound="AbstractShaftFromCAD._Cast_AbstractShaftFromCAD"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractShaftFromCAD",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractShaftFromCAD:
    """Special nested class for casting AbstractShaftFromCAD to subclasses."""

    __parent__: "AbstractShaftFromCAD"

    @property
    def component_from_cad(self: "CastSelf") -> "_2554.ComponentFromCAD":
        return self.__parent__._cast(_2554.ComponentFromCAD)

    @property
    def planet_shaft_from_cad(self: "CastSelf") -> "_2564.PlanetShaftFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2564

        return self.__parent__._cast(_2564.PlanetShaftFromCAD)

    @property
    def shaft_from_cad(self: "CastSelf") -> "_2568.ShaftFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2568

        return self.__parent__._cast(_2568.ShaftFromCAD)

    @property
    def abstract_shaft_from_cad(self: "CastSelf") -> "AbstractShaftFromCAD":
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
class AbstractShaftFromCAD(_2554.ComponentFromCAD):
    """AbstractShaftFromCAD

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_SHAFT_FROM_CAD

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def inner_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "InnerDiameter")

        if temp is None:
            return 0.0

        return temp

    @inner_diameter.setter
    @enforce_parameter_types
    def inner_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "InnerDiameter", float(value) if value is not None else 0.0
        )

    @property
    def length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Length")

        if temp is None:
            return 0.0

        return temp

    @length.setter
    @enforce_parameter_types
    def length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Length", float(value) if value is not None else 0.0
        )

    @property
    def offset(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Offset")

        if temp is None:
            return 0.0

        return temp

    @offset.setter
    @enforce_parameter_types
    def offset(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Offset", float(value) if value is not None else 0.0
        )

    @property
    def outer_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OuterDiameter")

        if temp is None:
            return 0.0

        return temp

    @outer_diameter.setter
    @enforce_parameter_types
    def outer_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "OuterDiameter", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_AbstractShaftFromCAD":
        """Cast to another type.

        Returns:
            _Cast_AbstractShaftFromCAD
        """
        return _Cast_AbstractShaftFromCAD(self)
