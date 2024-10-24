"""basenodemaps.py
Base maps for HDF5 objects with node methods.
"""
# Package Header #
from ...header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #

# Third-Party Packages #
import h5py

# Local Packages #
from ...hdf5bases import GroupMap, DatasetMap
from ...dataset import ObjectReferenceComponent
from ..datasetcomponents import NodeDatasetComponent
from ..groupcomponents import NodeGroupComponent


# Definitions #
# Classes #
class BaseNodeDatasetMap(DatasetMap):
    """A dataset map which outlines a dataset with basic node methods."""

    default_dtype = (("Node", h5py.ref_dtype),)
    default_component_types = {
        "object_reference": (
            ObjectReferenceComponent,
            {
                "reference_fields": {"dataset": "Dataset"},
                "primary_reference_field": "dataset",
            },
        ),
        "tree_node": (NodeDatasetComponent, {}),
    }


class BaseNodeGroupMap(GroupMap):
    """A group map which outlines a group with basic node methods."""

    default_attribute_names = {"tree_type": "tree_type"}
    default_attributes = {"tree_type": "Node"}
    default_map_names = {"node_map": "node_map"}
    default_maps = {"node_map": BaseNodeDatasetMap()}
    default_component_types = {
        "tree_node": (NodeGroupComponent, {}),
    }
