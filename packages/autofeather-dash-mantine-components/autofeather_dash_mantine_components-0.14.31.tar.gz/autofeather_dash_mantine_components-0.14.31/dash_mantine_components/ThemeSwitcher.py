# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class ThemeSwitcher(Component):
    """A ThemeSwitcher component.
ionIcon

Keyword arguments:

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- aria-* (string; optional):
    Wild card aria attributes.

- data-* (string; optional):
    Wild card data attributes.

- icon_auto (string; optional):
    The icon to display when the switch is in auto mode.

- icon_dark (string; optional):
    The icon to display when the switch is dark.

- icon_light (string; optional):
    The icon to display when the switch is light.

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

- tabIndex (number; optional):
    tab-index.

- value (string; optional):
    The value of the switch."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_mantine_components'
    _type = 'ThemeSwitcher'
    @_explicitize_args
    def __init__(self, n_clicks=Component.UNDEFINED, value=Component.UNDEFINED, icon_dark=Component.UNDEFINED, icon_light=Component.UNDEFINED, icon_auto=Component.UNDEFINED, id=Component.UNDEFINED, tabIndex=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'aria-*', 'data-*', 'icon_auto', 'icon_dark', 'icon_light', 'loading_state', 'n_clicks', 'tabIndex', 'value']
        self._valid_wildcard_attributes =            ['data-', 'aria-']
        self.available_properties = ['id', 'aria-*', 'data-*', 'icon_auto', 'icon_dark', 'icon_light', 'loading_state', 'n_clicks', 'tabIndex', 'value']
        self.available_wildcard_properties =            ['data-', 'aria-']
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(ThemeSwitcher, self).__init__(**args)
