# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class MultiDatePicker(Component):
    """A MultiDatePicker component.
ExampleComponent is an example component.
It takes a property, `label`, and
displays it.
It renders an input with the property `value`
which is editable by the user.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- animations (list; optional):
    List of animations to apply to the calendar.

- arrow (boolean | dash component; optional):
    Whether to display an arrow next to the input.

- arrowClassName (string; optional):
    CSS class name for the arrow.

- arrowStyle (dict; optional):
    Style object for the arrow.

- buttons (boolean; optional):
    Whether to display navigation buttons.

- calendar (string; optional):
    Type of calendar to use (e.g. 'gregorian', 'persian').

- calendarPosition (string; optional):
    Specifies the position of the calendar relative to the input
    field.

- className (string; optional):
    Custom CSS class name for the component.

- containerClassName (string; optional):
    Sets the CSS class for the container of the date picker.

- containerStyle (dict; optional):
    Defines the style object for the container of the date picker.

- currentDate (dict; optional):
    Current date to use as a basis for the month(s) displayed.

- digits (list; optional):
    List of digits to use in the calendar.

- disableDayPicker (boolean; optional):
    Whether to disable the day picker.

- disableMonthPicker (boolean; optional):
    Whether to disable the month picker.

- disableYearPicker (boolean; optional):
    Whether to disable the year picker.

- disabled (boolean; optional):
    Whether the input is disabled.

- displayWeekNumbers (boolean; optional):
    Whether to display week numbers.

- editable (boolean; optional):
    Determines whether the date picker input field is editable or not.

- fixMainPosition (boolean; optional):
    Determines whether the date picker should be fixed in the main
    position.

- fixRelativePosition (boolean; optional):
    Determines whether the date picker should be fixed in the relative
    position.

- format (string; optional):
    The `format` prop specifies the format in which the date should be
    displayed in the input field. The supported formats are similar to
    those in the `Date.prototype.toLocaleDateString()` method, such as
    \"dd/MM/yyyy\", \"MM/dd/yyyy\", \"yyyy-MM-dd\", etc. Example
    usage: format=\"yyyy-MM-dd\".

- formattingIgnoreList (list; optional):
    List of format tokens to ignore when parsing the `value`.

- fullYear (boolean; optional):
    Whether to display the full year (i.e. 12 months).

- hideMonth (boolean; optional):
    Whether to hide the month dropdown.

- hideOnScroll (boolean; optional):
    Controls whether or not the date picker should hide when
    scrolling.

- hideYear (boolean; optional):
    Whether to hide the year dropdown.

- inputClass (string; optional):
    CSS class name for the input field.

- inputMode (string; optional):
    Sets the input mode for the date picker.

- locale (string; optional):
    Language/locale to use (e.g. 'en-US', 'fa-IR').

- maxDate (dict | string | number; optional):
    Latest selectable date (can be a string, number, or `Date`
    object).

- minDate (dict | string | number; optional):
    Earliest selectable date (can be a string, number, or `Date`
    object).

- mobileButtons (list; optional):
    Sets the buttons for the mobile version of the date picker.

- mobileLabels (dict; optional):
    Sets the mobile labels for the date picker.

- months (list; optional):
    List of month names.

- multiple (boolean; optional):
    If `multiple` is True, the date picker allows selecting multiple
    dates. The `value` prop should be an array of dates. Example
    usage: multiple={True} value={[\"2023-04-12\", \"2023-04-15\"]}.

- name (string; optional):
    Name of the input field.

- numberOfMonths (number; optional):
    Number of months to display at once.

- offsetX (number; optional):
    Sets the horizontal offset for the date picker.

- offsetY (number; optional):
    Sets the vertical offset for the date picker.

- onOpenPickNewDate (boolean; optional):
    Determines whether a new date should be picked when the date
    picker is opened.

- onlyMonthPicker (boolean; optional):
    If `onlyMonthPicker` is True, the date picker displays a dropdown
    for selecting a month, but not a day or year. Example usage:
    onlyMonthPicker={True}.

- onlyShowInRangeDates (boolean; optional):
    Restricts the date picker to only show dates within a specified
    range.

- onlyYearPicker (boolean; optional):
    If `onlyYearPicker` is True, the date picker displays a dropdown
    for selecting a year, but not a day or month. Example usage:
    onlyYearPicker={True}.

- placeholder (string; optional):
    Placeholder text for the input field.

- plugins (list; optional):
    List of additional plugins to use.

- portal (boolean; optional):
    Determines whether the date picker should be rendered inside a
    portal.

- range (boolean; optional):
    If `range` is True, the date picker allows selecting a date range.
    The `value` prop should be an array with two dates representing
    the start and end of the range. Example usage: range={True}
    value={[\"2023-04-12\", \"2023-04-15\"]}.

- rangeHover (boolean; optional):
    Whether to enable the range hover effect.

- readOnly (boolean; optional):
    Whether the input is read-only.

- render (optional):
    Defines the render function or component for the input field.

- renderButton (dash component; optional):
    Custom function or element to render navigation buttons.

- scrollSensitive (boolean; optional):
    Determines if the date picker should respond to scroll events.

- shadow (boolean; optional):
    Whether to display a shadow around the calendar.

- showOtherDays (boolean; optional):
    Whether to show days from other months.

- sort (boolean; optional):
    Whether to sort the months and weekdays alphabetically.

- style (dict; optional):
    Style object for the input field.

- title (string; optional):
    Title of the input field.

- value (string | list; optional):
    The value displayed in the input.

- weekDays (list; optional):
    List of week day names.

- weekNumber (string; optional):
    Format string for the week number label.

- weekPicker (boolean; optional):
    Whether to enable the week picker.

- weekStartDayIndex (number; optional):
    Index of the day on which each week starts (0 = Sunday, 1 =
    Monday, etc.).

- zIndex (number; optional):
    Custom z-index value for the component."""
    _children_props = ['renderButton', 'arrow']
    _base_nodes = ['renderButton', 'arrow', 'children']
    _namespace = 'multi_date_picker'
    _type = 'MultiDatePicker'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, value=Component.UNDEFINED, multiple=Component.UNDEFINED, range=Component.UNDEFINED, onlyMonthPicker=Component.UNDEFINED, onlyYearPicker=Component.UNDEFINED, format=Component.UNDEFINED, formattingIgnoreList=Component.UNDEFINED, calendar=Component.UNDEFINED, locale=Component.UNDEFINED, mapDays=Component.UNDEFINED, onChange=Component.UNDEFINED, className=Component.UNDEFINED, weekDays=Component.UNDEFINED, months=Component.UNDEFINED, showOtherDays=Component.UNDEFINED, minDate=Component.UNDEFINED, maxDate=Component.UNDEFINED, disableYearPicker=Component.UNDEFINED, disableMonthPicker=Component.UNDEFINED, zIndex=Component.UNDEFINED, plugins=Component.UNDEFINED, sort=Component.UNDEFINED, numberOfMonths=Component.UNDEFINED, currentDate=Component.UNDEFINED, digits=Component.UNDEFINED, buttons=Component.UNDEFINED, renderButton=Component.UNDEFINED, weekStartDayIndex=Component.UNDEFINED, disableDayPicker=Component.UNDEFINED, onPropsChange=Component.UNDEFINED, onMonthChange=Component.UNDEFINED, onYearChange=Component.UNDEFINED, onFocusedDateChange=Component.UNDEFINED, readOnly=Component.UNDEFINED, disabled=Component.UNDEFINED, hideMonth=Component.UNDEFINED, hideYear=Component.UNDEFINED, shadow=Component.UNDEFINED, fullYear=Component.UNDEFINED, displayWeekNumbers=Component.UNDEFINED, weekNumber=Component.UNDEFINED, weekPicker=Component.UNDEFINED, rangeHover=Component.UNDEFINED, arrow=Component.UNDEFINED, arrowStyle=Component.UNDEFINED, arrowClassName=Component.UNDEFINED, animations=Component.UNDEFINED, inputClass=Component.UNDEFINED, name=Component.UNDEFINED, title=Component.UNDEFINED, placeholder=Component.UNDEFINED, style=Component.UNDEFINED, render=Component.UNDEFINED, inputMode=Component.UNDEFINED, scrollSensitive=Component.UNDEFINED, hideOnScroll=Component.UNDEFINED, calendarPosition=Component.UNDEFINED, containerStyle=Component.UNDEFINED, containerClassName=Component.UNDEFINED, editable=Component.UNDEFINED, onlyShowInRangeDates=Component.UNDEFINED, onOpen=Component.UNDEFINED, onClose=Component.UNDEFINED, fixMainPosition=Component.UNDEFINED, fixRelativePosition=Component.UNDEFINED, offsetY=Component.UNDEFINED, offsetX=Component.UNDEFINED, onPositionChange=Component.UNDEFINED, mobileLabels=Component.UNDEFINED, portal=Component.UNDEFINED, portalTarget=Component.UNDEFINED, onOpenPickNewDate=Component.UNDEFINED, mobileButtons=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'animations', 'arrow', 'arrowClassName', 'arrowStyle', 'buttons', 'calendar', 'calendarPosition', 'className', 'containerClassName', 'containerStyle', 'currentDate', 'digits', 'disableDayPicker', 'disableMonthPicker', 'disableYearPicker', 'disabled', 'displayWeekNumbers', 'editable', 'fixMainPosition', 'fixRelativePosition', 'format', 'formattingIgnoreList', 'fullYear', 'hideMonth', 'hideOnScroll', 'hideYear', 'inputClass', 'inputMode', 'locale', 'maxDate', 'minDate', 'mobileButtons', 'mobileLabels', 'months', 'multiple', 'name', 'numberOfMonths', 'offsetX', 'offsetY', 'onOpenPickNewDate', 'onlyMonthPicker', 'onlyShowInRangeDates', 'onlyYearPicker', 'placeholder', 'plugins', 'portal', 'range', 'rangeHover', 'readOnly', 'render', 'renderButton', 'scrollSensitive', 'shadow', 'showOtherDays', 'sort', 'style', 'title', 'value', 'weekDays', 'weekNumber', 'weekPicker', 'weekStartDayIndex', 'zIndex']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'animations', 'arrow', 'arrowClassName', 'arrowStyle', 'buttons', 'calendar', 'calendarPosition', 'className', 'containerClassName', 'containerStyle', 'currentDate', 'digits', 'disableDayPicker', 'disableMonthPicker', 'disableYearPicker', 'disabled', 'displayWeekNumbers', 'editable', 'fixMainPosition', 'fixRelativePosition', 'format', 'formattingIgnoreList', 'fullYear', 'hideMonth', 'hideOnScroll', 'hideYear', 'inputClass', 'inputMode', 'locale', 'maxDate', 'minDate', 'mobileButtons', 'mobileLabels', 'months', 'multiple', 'name', 'numberOfMonths', 'offsetX', 'offsetY', 'onOpenPickNewDate', 'onlyMonthPicker', 'onlyShowInRangeDates', 'onlyYearPicker', 'placeholder', 'plugins', 'portal', 'range', 'rangeHover', 'readOnly', 'render', 'renderButton', 'scrollSensitive', 'shadow', 'showOtherDays', 'sort', 'style', 'title', 'value', 'weekDays', 'weekNumber', 'weekPicker', 'weekStartDayIndex', 'zIndex']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(MultiDatePicker, self).__init__(**args)
