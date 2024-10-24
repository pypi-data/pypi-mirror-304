"""MultiNodeFELink"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.fe.links import _2474

_MULTI_NODE_FE_LINK = python_net_import(
    "SMT.MastaAPI.SystemModel.FE.Links", "MultiNodeFELink"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.fe.links import (
        _2475,
        _2477,
        _2478,
        _2479,
        _2480,
        _2482,
        _2483,
        _2484,
        _2485,
        _2486,
        _2487,
    )

    Self = TypeVar("Self", bound="MultiNodeFELink")
    CastSelf = TypeVar("CastSelf", bound="MultiNodeFELink._Cast_MultiNodeFELink")


__docformat__ = "restructuredtext en"
__all__ = ("MultiNodeFELink",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MultiNodeFELink:
    """Special nested class for casting MultiNodeFELink to subclasses."""

    __parent__: "MultiNodeFELink"

    @property
    def fe_link(self: "CastSelf") -> "_2474.FELink":
        return self.__parent__._cast(_2474.FELink)

    @property
    def electric_machine_stator_fe_link(
        self: "CastSelf",
    ) -> "_2475.ElectricMachineStatorFELink":
        from mastapy._private.system_model.fe.links import _2475

        return self.__parent__._cast(_2475.ElectricMachineStatorFELink)

    @property
    def gear_mesh_fe_link(self: "CastSelf") -> "_2477.GearMeshFELink":
        from mastapy._private.system_model.fe.links import _2477

        return self.__parent__._cast(_2477.GearMeshFELink)

    @property
    def gear_with_duplicated_meshes_fe_link(
        self: "CastSelf",
    ) -> "_2478.GearWithDuplicatedMeshesFELink":
        from mastapy._private.system_model.fe.links import _2478

        return self.__parent__._cast(_2478.GearWithDuplicatedMeshesFELink)

    @property
    def multi_angle_connection_fe_link(
        self: "CastSelf",
    ) -> "_2479.MultiAngleConnectionFELink":
        from mastapy._private.system_model.fe.links import _2479

        return self.__parent__._cast(_2479.MultiAngleConnectionFELink)

    @property
    def multi_node_connector_fe_link(
        self: "CastSelf",
    ) -> "_2480.MultiNodeConnectorFELink":
        from mastapy._private.system_model.fe.links import _2480

        return self.__parent__._cast(_2480.MultiNodeConnectorFELink)

    @property
    def planetary_connector_multi_node_fe_link(
        self: "CastSelf",
    ) -> "_2482.PlanetaryConnectorMultiNodeFELink":
        from mastapy._private.system_model.fe.links import _2482

        return self.__parent__._cast(_2482.PlanetaryConnectorMultiNodeFELink)

    @property
    def planet_based_fe_link(self: "CastSelf") -> "_2483.PlanetBasedFELink":
        from mastapy._private.system_model.fe.links import _2483

        return self.__parent__._cast(_2483.PlanetBasedFELink)

    @property
    def planet_carrier_fe_link(self: "CastSelf") -> "_2484.PlanetCarrierFELink":
        from mastapy._private.system_model.fe.links import _2484

        return self.__parent__._cast(_2484.PlanetCarrierFELink)

    @property
    def point_load_fe_link(self: "CastSelf") -> "_2485.PointLoadFELink":
        from mastapy._private.system_model.fe.links import _2485

        return self.__parent__._cast(_2485.PointLoadFELink)

    @property
    def rolling_ring_connection_fe_link(
        self: "CastSelf",
    ) -> "_2486.RollingRingConnectionFELink":
        from mastapy._private.system_model.fe.links import _2486

        return self.__parent__._cast(_2486.RollingRingConnectionFELink)

    @property
    def shaft_hub_connection_fe_link(
        self: "CastSelf",
    ) -> "_2487.ShaftHubConnectionFELink":
        from mastapy._private.system_model.fe.links import _2487

        return self.__parent__._cast(_2487.ShaftHubConnectionFELink)

    @property
    def multi_node_fe_link(self: "CastSelf") -> "MultiNodeFELink":
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
class MultiNodeFELink(_2474.FELink):
    """MultiNodeFELink

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MULTI_NODE_FE_LINK

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_MultiNodeFELink":
        """Cast to another type.

        Returns:
            _Cast_MultiNodeFELink
        """
        return _Cast_MultiNodeFELink(self)
