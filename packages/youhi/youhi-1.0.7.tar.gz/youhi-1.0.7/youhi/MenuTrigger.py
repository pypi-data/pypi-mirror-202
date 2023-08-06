# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class MenuTrigger(Component):
    """A MenuTrigger component.


Keyword arguments:

- children (boolean | number | string | dict | list; required)

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- className (string; optional)

- type (boolean | number | string | dict | list; default 'button')"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'youhi'
    _type = 'MenuTrigger'
    @_explicitize_args
    def __init__(self, children=None, className=Component.UNDEFINED, type=Component.UNDEFINED, id=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'className', 'type']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'className', 'type']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        if 'children' not in _explicit_args:
            raise TypeError('Required argument children was not specified.')

        super(MenuTrigger, self).__init__(children=children, **args)
