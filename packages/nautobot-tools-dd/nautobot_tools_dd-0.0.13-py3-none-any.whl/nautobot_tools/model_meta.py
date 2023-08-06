"""
Helper function for returning the field information that is associated
with a YANG model class. This includes returning all the
relationships and their associated metadata.

Usage: `get_field_info(model)` returns a `FieldInfo` instance.
"""
from collections import OrderedDict, namedtuple

from yangson.schemanode import SequenceNode, InternalNode, TerminalNode, SchemaTreeNode

# Using namedtuple so field info can be added accordingly later
FieldInfo = namedtuple('FieldResult', [
    'fields',  # Dict of field name -> model field instance
    'relations'
])

RelationInfo = namedtuple('RelationInfo', [
    'model_field',
    'to_many',
])


def get_field_info(model: InternalNode):
    """
    Given a model class, returns a `FieldInfo` instance, which is a
    `namedtuple`, containing metadata about the various field types on the model
    including information about their relationships.
    """
    fields = _get_fields(model)
    relations = _get_relationships(model)
    return FieldInfo(fields, relations)


def _get_fields(model: InternalNode):
    fields = OrderedDict()
    for child in model.children:
        if child.ns == 'dd-nos':
            continue
        fields[child.iname()] = child
    return fields


def _get_relationships(model: InternalNode):
    """
    Returns an `OrderedDict` of field names to `RelationInfo`.
    """
    forward_relations = OrderedDict()
    for field in [
        child for child in model.children if
        child.ns != 'dd-nos' and
        (not isinstance(child, TerminalNode) or isinstance(child, SequenceNode))
    ]:
        if isinstance(field, SequenceNode):
            # Deal with forward many-to-many relationships.
            forward_relations[field.iname()] = RelationInfo(
                model_field=field,
                to_many=True
            )
        else:
            forward_relations[field.iname()] = RelationInfo(
                model_field=field,
                to_many=False
            )
    return forward_relations

