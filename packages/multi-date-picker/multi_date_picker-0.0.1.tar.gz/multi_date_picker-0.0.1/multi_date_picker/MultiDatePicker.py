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

- animations (list; optional)

- arrow (boolean | dash component; optional)

- arrowClassName (string; optional)

- arrowStyle (dict; optional)

- buttons (boolean; optional)

- calendar (string; optional)

- calendarPosition (string; optional)

- className (string; optional)

- containerClassName (string; optional)

- containerStyle (dict; optional)

- currentDate (dict; optional)

- digits (list; optional)

- disableDayPicker (boolean; optional)

- disableMonthPicker (boolean; optional)

- disableYearPicker (boolean; optional)

- disabled (boolean; optional)

- displayWeekNumbers (boolean; optional)

- editable (boolean; optional)

- fixMainPosition (boolean; optional)

- fixRelativePosition (boolean; optional)

- format (string; optional)

- formattingIgnoreList (list; optional)

- fullYear (boolean; optional)

- hideMonth (boolean; optional)

- hideOnScroll (boolean; optional)

- hideYear (boolean; optional)

- inputClass (string; optional)

- inputMode (string; optional)

- locale (string; optional)

- maxDate (dict | string | number; optional)

- minDate (dict | string | number; optional)

- mobileButtons (list; optional)

- mobileLabels (dict; optional)

- months (list; optional)

- multiple (boolean; optional)

- name (string; optional)

- numberOfMonths (number; optional)

- offsetX (number; optional)

- offsetY (number; optional)

- onOpenPickNewDate (boolean; optional)

- onlyMonthPicker (boolean; optional)

- onlyShowInRangeDates (boolean; optional)

- onlyYearPicker (boolean; optional)

- placeholder (string; optional)

- plugins (list; optional)

- portal (boolean; optional)

- range (boolean; optional)

- rangeHover (boolean; optional)

- readOnly (boolean; optional)

- render (optional)

- renderButton (dash component; optional)

- scrollSensitive (boolean; optional)

- shadow (boolean; optional)

- showOtherDays (boolean; optional)

- sort (boolean; optional)

- style (dict; optional)

- title (string; optional)

- value (dict | string | number | list; optional):
    The value displayed in the input.

- weekDays (list; optional)

- weekNumber (string; optional)

- weekPicker (boolean; optional)

- weekStartDayIndex (number; optional)

- zIndex (number; optional)"""
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
