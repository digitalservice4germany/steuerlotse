import PropTypes from "prop-types";

export const checkboxPropType = PropTypes.exact({
  errors: PropTypes.arrayOf(PropTypes.string),
  checked: PropTypes.bool,
});

export const labelPropType = PropTypes.exact({
  text: PropTypes.string,
  showOptionalTag: PropTypes.bool,
  help: PropTypes.string, // field.render_kw['help']
  exampleInput: PropTypes.string, // field.render_kw["example_input"]
});

export const extendedCheckboxPropType = PropTypes.exact({
  errors: PropTypes.arrayOf(PropTypes.string),
  checked: PropTypes.bool,
  name: PropTypes.string.isRequired,
  label: labelPropType,
});

export const fieldPropType = PropTypes.exact({
  value: PropTypes.any,
  errors: PropTypes.arrayOf(PropTypes.string),
});

export const extendedFieldPropType = PropTypes.exact({
  value: PropTypes.any,
  errors: PropTypes.arrayOf(PropTypes.string),
  name: PropTypes.string.isRequired,
  label: labelPropType,
});

export const optionsPropType = PropTypes.arrayOf(
  PropTypes.exact({
    value: PropTypes.string,
    displayName: PropTypes.oneOfType([PropTypes.string, PropTypes.element]),
  })
);

export const selectionFieldPropType = PropTypes.exact({
  selectedValue: PropTypes.any,
  options: optionsPropType,
  errors: PropTypes.arrayOf(PropTypes.string),
});

export const stepHeaderPropType = PropTypes.exact({
  title: PropTypes.string,
  intro: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.element,
    PropTypes.object,
  ]),
  hideIntro: PropTypes.bool,
});

export const extendedSelectionFieldPropType = PropTypes.exact({
  selectedValue: PropTypes.any,
  options: optionsPropType,
  errors: PropTypes.arrayOf(PropTypes.string),
  name: PropTypes.string.isRequired,
  label: labelPropType,
});
