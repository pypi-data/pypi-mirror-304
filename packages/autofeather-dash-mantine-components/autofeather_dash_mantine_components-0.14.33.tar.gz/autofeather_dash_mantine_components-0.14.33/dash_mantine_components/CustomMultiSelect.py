# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class CustomMultiSelect(Component):
    """A CustomMultiSelect component.
tiSelect

Keyword arguments:

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- aria-* (string; optional):
    Wild card aria attributes.

- bd (string | number; optional):
    Border.

- bg (boolean | number | string | dict | list; optional):
    Background, theme key: theme.colors.

- bga (boolean | number | string | dict | list; optional):
    BackgroundAttachment.

- bgp (string | number; optional):
    BackgroundPosition.

- bgr (boolean | number | string | dict | list; optional):
    BackgroundRepeat.

- bgsz (string | number; optional):
    BackgroundSize.

- bottom (string | number; optional)

- c (boolean | number | string | dict | list; optional):
    Color.

- checkIconPosition (a value equal to: 'left', 'right'; optional):
    Position of the check icon relative to the option label, `'left'`
    by default.

- className (string; optional):
    Class added to the root element, if applicable.

- classNames (dict; optional):
    Adds class names to Mantine components.

- clearButtonProps (dict; optional):
    Props passed down to the clear button.

    `clearButtonProps` is a dict with keys:

    - children (a list of or a singular dash component, string or number; optional):
        Content rendered inside the button, for example
        `VisuallyHidden` with label for screen readers.

    - disabled (boolean; optional):
        Sets `disabled` and `data-disabled` attributes on the button
        element.

    - icon (a list of or a singular dash component, string or number; optional):
        Replaces default close icon. If set, `iconSize` prop is
        ignored.

    - iconSize (string | number; optional):
        `X` icon `width` and `height`, `80%` by default.

    - radius (number; optional):
        Key of `theme.radius` or any valid CSS value to set
        border-radius. Numbers are converted to rem.
        `theme.defaultRadius` by default.

    - size (number; optional):
        Controls width and height of the button. Numbers are converted
        to rem. `'md'` by default.

- clearable (boolean; optional):
    Determines whether the clear button should be displayed in the
    right section when the component has value, `False` by default.

- comboboxProps (dict; optional):
    Props passed down to `Combobox` component.

    `comboboxProps` is a dict with keys:

    - arrowOffset (number; optional):
        Arrow offset in px, `5` by default.

    - arrowPosition (a value equal to: 'center', 'side'; optional):
        Arrow position.

    - arrowRadius (number; optional):
        Arrow `border-radius` in px, `0` by default.

    - arrowSize (number; optional):
        Arrow size in px, `7` by default.

    - children (a list of or a singular dash component, string or number; optional):
        Combobox content.

    - classNames (dict; optional):
        Adds class names to Mantine components.

    - disabled (boolean; optional):
        If set, popover dropdown will not be rendered.

    - dropdownPadding (string | number; optional):
        Controls `padding` of the dropdown, `4` by default.

    - floatingStrategy (a value equal to: 'fixed', 'absolute'; optional):
        Changes floating ui [position
        strategy](https://floating-ui.com/docs/usefloating#strategy),
        `'absolute'` by default.

    - keepMounted (boolean; optional):
        If set dropdown will not be unmounted from the DOM when it is
        hidden, `display: none` styles will be added instead.

    - middlewares (dict; optional):
        Floating ui middlewares to configure position handling, `{
        flip: True, shift: True, inline: False }` by default.

        `middlewares` is a dict with keys:

        - flip (dict; optional)

            `flip` is a dict with keys:

    - altBoundary (boolean; optional):
        Whether to check for overflow using the alternate element's
        boundary  (`clippingAncestors` boundary only).
        @,default,False.

    - boundary (dict; optional)

        `boundary` is a dict with keys:

        - height (number; required)

        - width (number; required)

        - x (number; required)

        - y (number; required)

              Or list of a list of or a singular dash component, string or numbers

    - crossAxis (boolean; optional):
        The axis that runs along the alignment of the floating
        element. Determines  whether overflow along this axis is
        checked to perform a flip. @,default,True.

    - elementContext (a value equal to: 'reference', 'floating'; optional):
        The element in which overflow is being checked relative to a
        boundary. @,default,'floating'.

    - fallbackAxisSideDirection (a value equal to: 'none', 'end', 'start'; optional):
        Whether to allow fallback to the perpendicular axis of the
        preferred  placement, and if so, which side direction along
        the axis to prefer. @,default,'none' (disallow fallback).

    - fallbackPlacements (list of a value equal to: 'top', 'left', 'bottom', 'right', 'top-end', 'top-start', 'left-end', 'left-start', 'bottom-end', 'bottom-start', 'right-end', 'right-start's; optional):
        Placements to try sequentially if the preferred `placement`
        does not fit. @,default,[oppositePlacement] (computed).

    - fallbackStrategy (a value equal to: 'bestFit', 'initialPlacement'; optional):
        What strategy to use when no placements fit.
        @,default,'bestFit'.

    - flipAlignment (boolean; optional):
        Whether to flip to placements with the opposite alignment if
        they fit  better. @,default,True.

    - mainAxis (boolean; optional):
        The axis that runs along the side of the floating element.
        Determines  whether overflow along this axis is checked to
        perform a flip. @,default,True.

    - padding (dict; optional):
        Virtual padding for the resolved overflow detection offsets.
        @,default,0.

        `padding` is a number

          Or dict with keys:

        - bottom (number; optional)

        - left (number; optional)

        - right (number; optional)

        - top (number; optional)

    - rootBoundary (dict; optional):
        The root clipping area in which overflow will be checked.
        @,default,'viewport'.

        `rootBoundary` is a dict with keys:

        - height (number; required)

        - width (number; required)

        - x (number; required)

        - y (number; required)

        - inline (boolean | number | string | dict | list; optional)

        - shift (optional)

        - size (optional)

    - offset (number; optional):
        Offset of the dropdown element, `8` by default.

    - portalProps (dict; optional):
        Props to pass down to the `Portal` when `withinPortal` is
        True.

    - position (a value equal to: 'top', 'left', 'bottom', 'right', 'top-end', 'top-start', 'left-end', 'left-start', 'bottom-end', 'bottom-start', 'right-end', 'right-start'; optional):
        Dropdown position relative to the target element, `'bottom'`
        by default.

    - positionDependencies (list of boolean | number | string | dict | lists; optional):
        `useEffect` dependencies to force update dropdown position,
        `[]` by default.

    - radius (number; optional):
        Key of `theme.radius` or any valid CSS value to set
        border-radius, `theme.defaultRadius` by default.

    - readOnly (boolean; optional):
        Determines whether Combobox value can be changed.

    - resetSelectionOnOptionHover (boolean; optional):
        Determines whether selection should be reset when option is
        hovered, `False` by default.

    - returnFocus (boolean; optional):
        Determines whether focus should be automatically returned to
        control when dropdown closes, `False` by default.

    - shadow (boolean | number | string | dict | list; optional):
        Key of `theme.shadows` or any other valid CSS `box-shadow`
        value.

    - size (boolean | number | string | dict | list; optional):
        Controls items `font-size` and `padding`, `'sm'` by default.

    - styles (boolean | number | string | dict | list; optional):
        Mantine styles API.

    - transitionProps (dict; optional):
        Props passed down to the `Transition` component that used to
        animate dropdown presence, use to configure duration and
        animation type, `{ duration: 150, transition: 'fade' }` by
        default.

        `transitionProps` is a dict with keys:

        - duration (number; optional):
            Transition duration in ms, `250` by default.

        - exitDuration (number; optional):
            Exit transition duration in ms, `250` by default.

        - keepMounted (boolean; optional):
            If set element will not be unmounted from the DOM when it
            is hidden, `display: none` styles will be applied instead.

        - mounted (boolean; required):
            Determines whether component should be mounted to the DOM.

        - timingFunction (string; optional):
            Transition timing function,
            `theme.transitionTimingFunction` by default.

        - transition (boolean | number | string | dict | list; optional):
            Transition name or object.

    - unstyled (boolean; optional):
        Remove all Mantine styling from the component.

    - variant (string; optional):
        variant.

    - width (string | number; optional):
        Dropdown width, or `'target'` to make dropdown width the same
        as target element, `'max-content'` by default.

    - withArrow (boolean; optional):
        Determines whether component should have an arrow, `False` by
        default.

    - withinPortal (boolean; optional):
        Determines whether dropdown should be rendered within the
        `Portal`, `True` by default.

    - zIndex (string | number; optional):
        Dropdown `z-index`, `300` by default.

- darkHidden (boolean; optional):
    Determines whether component should be hidden in dark color scheme
    with `display: none`.

- data (list of strings; optional):
    Array of available select options.

- data-* (string; optional):
    Wild card data attributes.

- description (a list of or a singular dash component, string or number; optional):
    Contents of `Input.Description` component. If not set, description
    is not rendered.

- descriptionProps (dict with strings as keys and values of type boolean | number | string | dict | list; optional):
    Props passed down to the `Input.Description` component.

- disabled (boolean; optional):
    Sets `disabled` attribute on the `input` element.

- display (boolean | number | string | dict | list; optional)

- dropdownHeight (number; optional):
    Maximum height of the dropdown.

- dropdownOpened (boolean; optional):
    Controlled dropdown opened state.

- error (a list of or a singular dash component, string or number; optional):
    Contents of `Input.Error` component. If not set, error is not
    rendered.

- errorProps (dict with strings as keys and values of type boolean | number | string | dict | list; optional):
    Props passed down to the `Input.Error` component.

- ff (boolean | number | string | dict | list; optional):
    FontFamily.

- finalValue (list of strings; optional):
    Values selected when dropdown is closed.

- flex (string | number; optional)

- fs (boolean | number | string | dict | list; optional):
    FontStyle.

- fw (boolean | number | string | dict | list; optional):
    FontWeight.

- fz (number; optional):
    FontSize, theme key: theme.fontSizes.

- h (string | number; optional):
    Height, theme key: theme.spacing.

- hiddenFrom (boolean | number | string | dict | list; optional):
    Breakpoint above which the component is hidden with `display:
    none`.

- hiddenInputProps (dict; optional):
    Props passed down to the hidden input.

- hiddenInputValuesDivider (string; optional):
    Divider used to separate values in the hidden input `value`
    attribute, `','` by default.

- hidePickedOptions (boolean; optional):
    Determines whether picked options should be removed from the
    options list, `False` by default.

- inputWrapperOrder (list of a value equal to: 'label', 'input', 'description', 'error's; optional):
    Controls order of the elements, `['label', 'description', 'input',
    'error']` by default.

- inset (string | number; optional)

- label (a list of or a singular dash component, string or number; optional):
    Contents of `Input.Label` component. If not set, label is not
    rendered.

- labelProps (dict with strings as keys and values of type boolean | number | string | dict | list; optional):
    Props passed down to the `Input.Label` component.

- left (string | number; optional)

- leftSection (a list of or a singular dash component, string or number; optional):
    Content section rendered on the left side of the input.

- leftSectionPointerEvents (a value equal to: 'auto', '-moz-initial', 'inherit', 'initial', 'revert', 'revert-layer', 'unset', 'none', 'all', 'fill', 'painted', 'stroke', 'visible', 'visibleFill', 'visiblePainted', 'visibleStroke'; optional):
    Sets `pointer-events` styles on the `leftSection` element,
    `'none'` by default.

- leftSectionProps (dict; optional):
    Props passed down to the `leftSection` element.

- leftSectionWidth (string | number; optional):
    Left section width, used to set `width` of the section and input
    `padding-left`, by default equals to the input height.

- lh (number; optional):
    LineHeight, theme key: lineHeights.

- lightHidden (boolean; optional):
    Determines whether component should be hidden in light color
    scheme with `display: none`.

- limit (number; optional):
    Maximum number of options displayed at a time, `Infinity` by
    default.

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

- lts (string | number; optional):
    LetterSpacing.

- m (number; optional):
    Margin, theme key: theme.spacing.

- mah (string | number; optional):
    MaxHeight, theme key: theme.spacing.

- maw (string | number; optional):
    MaxWidth, theme key: theme.spacing.

- maxDropdownHeight (string | number; optional):
    `max-height` of the dropdown, only applicable when
    `withScrollArea` prop is `True`, `250` by default.

- maxValues (number; optional):
    Maximum number of values, `Infinity` by default.

- mb (number; optional):
    MarginBottom, theme key: theme.spacing.

- me (number; optional):
    MarginInlineEnd, theme key: theme.spacing.

- mih (string | number; optional):
    MinHeight, theme key: theme.spacing.

- miw (string | number; optional):
    MinWidth, theme key: theme.spacing.

- ml (number; optional):
    MarginLeft, theme key: theme.spacing.

- mod (string | dict with strings as keys and values of type boolean | number | string | dict | list; optional):
    Element modifiers transformed into `data-` attributes, for
    example, `{ 'data-size': 'xl' }`, falsy values are removed.

- mr (number; optional):
    MarginRight, theme key: theme.spacing.

- ms (number; optional):
    MarginInlineStart, theme key: theme.spacing.

- mt (number; optional):
    MarginTop, theme key: theme.spacing.

- mx (number; optional):
    MarginInline, theme key: theme.spacing.

- my (number; optional):
    MarginBlock, theme key: theme.spacing.

- name (string; optional):
    Name prop.

- nothingFoundMessage (a list of or a singular dash component, string or number; optional):
    Message displayed when no option matched current search query,
    only applicable when `searchable` prop is set.

- opacity (boolean | number | string | dict | list; optional)

- p (number; optional):
    Padding, theme key: theme.spacing.

- pb (number; optional):
    PaddingBottom, theme key: theme.spacing.

- pe (number; optional):
    PaddingInlineEnd, theme key: theme.spacing.

- persisted_props (list of strings; default ["value"]):
    Properties whose user interactions will persist after refreshing
    the component or the page. Since only `value` is allowed this prop
    can normally be ignored.

- persistence (string | number; optional):
    Used to allow user interactions in this component to be persisted
    when the component - or the page - is refreshed. If `persisted` is
    truthy and hasn't changed from its previous value, a `value` that
    the user has changed while using the app will keep that change, as
    long as the new `value` also matches what was given originally.
    Used in conjunction with `persistence_type`.

- persistence_type (a value equal to: 'local', 'session', 'memory'; default 'local'):
    Where persisted user changes will be stored: memory: only kept in
    memory, reset on page refresh. local: window.localStorage, data is
    kept after the browser quit. session: window.sessionStorage, data
    is cleared once the browser quit.

- pl (number; optional):
    PaddingLeft, theme key: theme.spacing.

- placeholder (string; optional):
    Placeholder.

- pointer (boolean; optional):
    Determines whether the input should have `cursor: pointer` style,
    `False` by default.

- pos (boolean | number | string | dict | list; optional):
    Position.

- pr (number; optional):
    PaddingRight, theme key: theme.spacing.

- ps (number; optional):
    PaddingInlineStart, theme key: theme.spacing.

- pt (number; optional):
    PaddingTop, theme key: theme.spacing.

- px (number; optional):
    PaddingInline, theme key: theme.spacing.

- py (number; optional):
    PaddingBlock, theme key: theme.spacing.

- radius (number; optional):
    Key of `theme.radius` or any valid CSS value to set
    `border-radius`, numbers are converted to rem,
    `theme.defaultRadius` by default.

- readOnly (boolean; optional):
    Readonly.

- required (boolean; optional):
    Adds required attribute to the input and a red asterisk on the
    right side of label, `False` by default.

- right (string | number; optional)

- rightSection (a list of or a singular dash component, string or number; optional):
    Content section rendered on the right side of the input.

- rightSectionPointerEvents (a value equal to: 'auto', '-moz-initial', 'inherit', 'initial', 'revert', 'revert-layer', 'unset', 'none', 'all', 'fill', 'painted', 'stroke', 'visible', 'visibleFill', 'visiblePainted', 'visibleStroke'; optional):
    Sets `pointer-events` styles on the `rightSection` element,
    `'none'` by default.

- rightSectionProps (dict; optional):
    Props passed down to the `rightSection` element.

- rightSectionWidth (string | number; optional):
    Right section width, used to set `width` of the section and input
    `padding-right`, by default equals to the input height.

- searchValue (string; optional):
    Controlled search value.

- searchable (boolean; optional):
    Determines whether the select should be searchable, `False` by
    default.

- selectFirstOptionOnChange (boolean; optional):
    Determines whether the first option should be selected when value
    changes, `False` by default.

- size (boolean | number | string | dict | list; optional):
    Controls input `height` and horizontal `padding`, `'sm'` by
    default.

- style (optional):
    Inline style added to root component element, can subscribe to
    theme defined on MantineProvider.

- styles (boolean | number | string | dict | list; optional):
    Mantine styles API.

- ta (boolean | number | string | dict | list; optional):
    TextAlign.

- tabIndex (number; optional):
    tab-index.

- td (string | number; optional):
    TextDecoration.

- top (string | number; optional)

- tt (boolean | number | string | dict | list; optional):
    TextTransform.

- unstyled (boolean; optional):
    Remove all Mantine styling from the component.

- value (list of strings; optional):
    Controlled component value.

- variant (string; optional):
    variant.

- visibleFrom (boolean | number | string | dict | list; optional):
    Breakpoint below which the component is hidden with `display:
    none`.

- w (string | number; optional):
    Width, theme key: theme.spacing.

- withAsterisk (boolean; optional):
    Determines whether the required asterisk should be displayed.
    Overrides `required` prop. Does not add required attribute to the
    input. `False` by default.

- withCheckIcon (boolean; optional):
    Determines whether check icon should be displayed near the
    selected option label, `True` by default.

- withErrorStyles (boolean; optional):
    Determines whether the input should have red border and red text
    color when the `error` prop is set, `True` by default.

- withScrollArea (boolean; optional):
    Determines whether the options should be wrapped with
    `ScrollArea.AutoSize`, `True` by default.

- wrapperProps (dict with strings as keys and values of type boolean | number | string | dict | list; optional):
    Props passed down to the root element."""
    _children_props = ['nothingFoundMessage', 'clearButtonProps.children', 'clearButtonProps.icon', 'label', 'description', 'error', 'leftSection', 'rightSection', 'comboboxProps.children', 'comboboxProps.middlewares.flip.boundary']
    _base_nodes = ['nothingFoundMessage', 'label', 'description', 'error', 'leftSection', 'rightSection', 'children']
    _namespace = 'dash_mantine_components'
    _type = 'CustomMultiSelect'
    @_explicitize_args
    def __init__(self, value=Component.UNDEFINED, data=Component.UNDEFINED, finalValue=Component.UNDEFINED, searchValue=Component.UNDEFINED, maxValues=Component.UNDEFINED, searchable=Component.UNDEFINED, nothingFoundMessage=Component.UNDEFINED, withCheckIcon=Component.UNDEFINED, checkIconPosition=Component.UNDEFINED, hidePickedOptions=Component.UNDEFINED, clearable=Component.UNDEFINED, clearButtonProps=Component.UNDEFINED, hiddenInputProps=Component.UNDEFINED, hiddenInputValuesDivider=Component.UNDEFINED, dropdownHeight=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, hiddenFrom=Component.UNDEFINED, visibleFrom=Component.UNDEFINED, lightHidden=Component.UNDEFINED, darkHidden=Component.UNDEFINED, mod=Component.UNDEFINED, m=Component.UNDEFINED, my=Component.UNDEFINED, mx=Component.UNDEFINED, mt=Component.UNDEFINED, mb=Component.UNDEFINED, ms=Component.UNDEFINED, me=Component.UNDEFINED, ml=Component.UNDEFINED, mr=Component.UNDEFINED, p=Component.UNDEFINED, py=Component.UNDEFINED, px=Component.UNDEFINED, pt=Component.UNDEFINED, pb=Component.UNDEFINED, ps=Component.UNDEFINED, pe=Component.UNDEFINED, pl=Component.UNDEFINED, pr=Component.UNDEFINED, bd=Component.UNDEFINED, bg=Component.UNDEFINED, c=Component.UNDEFINED, opacity=Component.UNDEFINED, ff=Component.UNDEFINED, fz=Component.UNDEFINED, fw=Component.UNDEFINED, lts=Component.UNDEFINED, ta=Component.UNDEFINED, lh=Component.UNDEFINED, fs=Component.UNDEFINED, tt=Component.UNDEFINED, td=Component.UNDEFINED, w=Component.UNDEFINED, miw=Component.UNDEFINED, maw=Component.UNDEFINED, h=Component.UNDEFINED, mih=Component.UNDEFINED, mah=Component.UNDEFINED, bgsz=Component.UNDEFINED, bgp=Component.UNDEFINED, bgr=Component.UNDEFINED, bga=Component.UNDEFINED, pos=Component.UNDEFINED, top=Component.UNDEFINED, left=Component.UNDEFINED, bottom=Component.UNDEFINED, right=Component.UNDEFINED, inset=Component.UNDEFINED, display=Component.UNDEFINED, flex=Component.UNDEFINED, wrapperProps=Component.UNDEFINED, readOnly=Component.UNDEFINED, label=Component.UNDEFINED, description=Component.UNDEFINED, error=Component.UNDEFINED, required=Component.UNDEFINED, withAsterisk=Component.UNDEFINED, labelProps=Component.UNDEFINED, descriptionProps=Component.UNDEFINED, errorProps=Component.UNDEFINED, inputWrapperOrder=Component.UNDEFINED, leftSection=Component.UNDEFINED, leftSectionWidth=Component.UNDEFINED, leftSectionProps=Component.UNDEFINED, leftSectionPointerEvents=Component.UNDEFINED, rightSection=Component.UNDEFINED, rightSectionWidth=Component.UNDEFINED, rightSectionProps=Component.UNDEFINED, rightSectionPointerEvents=Component.UNDEFINED, radius=Component.UNDEFINED, disabled=Component.UNDEFINED, size=Component.UNDEFINED, pointer=Component.UNDEFINED, withErrorStyles=Component.UNDEFINED, placeholder=Component.UNDEFINED, name=Component.UNDEFINED, dropdownOpened=Component.UNDEFINED, selectFirstOptionOnChange=Component.UNDEFINED, comboboxProps=Component.UNDEFINED, limit=Component.UNDEFINED, withScrollArea=Component.UNDEFINED, maxDropdownHeight=Component.UNDEFINED, classNames=Component.UNDEFINED, styles=Component.UNDEFINED, unstyled=Component.UNDEFINED, variant=Component.UNDEFINED, id=Component.UNDEFINED, tabIndex=Component.UNDEFINED, loading_state=Component.UNDEFINED, persistence=Component.UNDEFINED, persisted_props=Component.UNDEFINED, persistence_type=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'aria-*', 'bd', 'bg', 'bga', 'bgp', 'bgr', 'bgsz', 'bottom', 'c', 'checkIconPosition', 'className', 'classNames', 'clearButtonProps', 'clearable', 'comboboxProps', 'darkHidden', 'data', 'data-*', 'description', 'descriptionProps', 'disabled', 'display', 'dropdownHeight', 'dropdownOpened', 'error', 'errorProps', 'ff', 'finalValue', 'flex', 'fs', 'fw', 'fz', 'h', 'hiddenFrom', 'hiddenInputProps', 'hiddenInputValuesDivider', 'hidePickedOptions', 'inputWrapperOrder', 'inset', 'label', 'labelProps', 'left', 'leftSection', 'leftSectionPointerEvents', 'leftSectionProps', 'leftSectionWidth', 'lh', 'lightHidden', 'limit', 'loading_state', 'lts', 'm', 'mah', 'maw', 'maxDropdownHeight', 'maxValues', 'mb', 'me', 'mih', 'miw', 'ml', 'mod', 'mr', 'ms', 'mt', 'mx', 'my', 'name', 'nothingFoundMessage', 'opacity', 'p', 'pb', 'pe', 'persisted_props', 'persistence', 'persistence_type', 'pl', 'placeholder', 'pointer', 'pos', 'pr', 'ps', 'pt', 'px', 'py', 'radius', 'readOnly', 'required', 'right', 'rightSection', 'rightSectionPointerEvents', 'rightSectionProps', 'rightSectionWidth', 'searchValue', 'searchable', 'selectFirstOptionOnChange', 'size', 'style', 'styles', 'ta', 'tabIndex', 'td', 'top', 'tt', 'unstyled', 'value', 'variant', 'visibleFrom', 'w', 'withAsterisk', 'withCheckIcon', 'withErrorStyles', 'withScrollArea', 'wrapperProps']
        self._valid_wildcard_attributes =            ['data-', 'aria-']
        self.available_properties = ['id', 'aria-*', 'bd', 'bg', 'bga', 'bgp', 'bgr', 'bgsz', 'bottom', 'c', 'checkIconPosition', 'className', 'classNames', 'clearButtonProps', 'clearable', 'comboboxProps', 'darkHidden', 'data', 'data-*', 'description', 'descriptionProps', 'disabled', 'display', 'dropdownHeight', 'dropdownOpened', 'error', 'errorProps', 'ff', 'finalValue', 'flex', 'fs', 'fw', 'fz', 'h', 'hiddenFrom', 'hiddenInputProps', 'hiddenInputValuesDivider', 'hidePickedOptions', 'inputWrapperOrder', 'inset', 'label', 'labelProps', 'left', 'leftSection', 'leftSectionPointerEvents', 'leftSectionProps', 'leftSectionWidth', 'lh', 'lightHidden', 'limit', 'loading_state', 'lts', 'm', 'mah', 'maw', 'maxDropdownHeight', 'maxValues', 'mb', 'me', 'mih', 'miw', 'ml', 'mod', 'mr', 'ms', 'mt', 'mx', 'my', 'name', 'nothingFoundMessage', 'opacity', 'p', 'pb', 'pe', 'persisted_props', 'persistence', 'persistence_type', 'pl', 'placeholder', 'pointer', 'pos', 'pr', 'ps', 'pt', 'px', 'py', 'radius', 'readOnly', 'required', 'right', 'rightSection', 'rightSectionPointerEvents', 'rightSectionProps', 'rightSectionWidth', 'searchValue', 'searchable', 'selectFirstOptionOnChange', 'size', 'style', 'styles', 'ta', 'tabIndex', 'td', 'top', 'tt', 'unstyled', 'value', 'variant', 'visibleFrom', 'w', 'withAsterisk', 'withCheckIcon', 'withErrorStyles', 'withScrollArea', 'wrapperProps']
        self.available_wildcard_properties =            ['data-', 'aria-']
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(CustomMultiSelect, self).__init__(**args)
