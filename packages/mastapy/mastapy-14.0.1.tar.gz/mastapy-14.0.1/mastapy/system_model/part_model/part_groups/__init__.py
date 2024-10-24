"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model.part_groups._2545 import (
        ConcentricOrParallelPartGroup,
    )
    from mastapy._private.system_model.part_model.part_groups._2546 import (
        ConcentricPartGroup,
    )
    from mastapy._private.system_model.part_model.part_groups._2547 import (
        ConcentricPartGroupParallelToThis,
    )
    from mastapy._private.system_model.part_model.part_groups._2548 import (
        DesignMeasurements,
    )
    from mastapy._private.system_model.part_model.part_groups._2549 import (
        ParallelPartGroup,
    )
    from mastapy._private.system_model.part_model.part_groups._2550 import (
        ParallelPartGroupSelection,
    )
    from mastapy._private.system_model.part_model.part_groups._2551 import PartGroup
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model.part_groups._2545": [
            "ConcentricOrParallelPartGroup"
        ],
        "_private.system_model.part_model.part_groups._2546": ["ConcentricPartGroup"],
        "_private.system_model.part_model.part_groups._2547": [
            "ConcentricPartGroupParallelToThis"
        ],
        "_private.system_model.part_model.part_groups._2548": ["DesignMeasurements"],
        "_private.system_model.part_model.part_groups._2549": ["ParallelPartGroup"],
        "_private.system_model.part_model.part_groups._2550": [
            "ParallelPartGroupSelection"
        ],
        "_private.system_model.part_model.part_groups._2551": ["PartGroup"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ConcentricOrParallelPartGroup",
    "ConcentricPartGroup",
    "ConcentricPartGroupParallelToThis",
    "DesignMeasurements",
    "ParallelPartGroup",
    "ParallelPartGroupSelection",
    "PartGroup",
)
