# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class ThemeSwitcher(Component):
    """A ThemeSwitcher component.
ionIcon

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The icons to display when the switch is dark, light, and auto.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- aria-* (string; optional):
    Wild card aria attributes.

- data-* (string; optional):
    Wild card data attributes.

- loading_state (dict; optional):
    Object that holds the loading state object coming from
    dash-renderer.

    `loading_state` is a dict with keys:

    - component_name (string; required):
        Holds the name of the component that is loading.

    - is_loading (boolean; required):
        Determines if the component is loading or not.

    - prop_name (string; required):
        Holds which property is loading.

- n_clicks (number; default 0):
    An integer that represents the number of times that this element
    has been clicked on.

- result (a value equal to: 'dark', 'light'; optional):
    The resulting theme to set.

- tabIndex (number; optional):
    tab-index.

- value (string; optional):
    The value of the switch."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_mantine_components'
    _type = 'ThemeSwitcher'
    @_explicitize_args
    def __init__(self, children=None, n_clicks=Component.UNDEFINED, value=Component.UNDEFINED, result=Component.UNDEFINED, id=Component.UNDEFINED, tabIndex=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'aria-*', 'data-*', 'loading_state', 'n_clicks', 'result', 'tabIndex', 'value']
        self._valid_wildcard_attributes =            ['data-', 'aria-']
        self.available_properties = ['children', 'id', 'aria-*', 'data-*', 'loading_state', 'n_clicks', 'result', 'tabIndex', 'value']
        self.available_wildcard_properties =            ['data-', 'aria-']
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(ThemeSwitcher, self).__init__(children=children, **args)
