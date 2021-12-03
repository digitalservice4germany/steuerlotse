import PropTypes from "prop-types";

export const checkboxPropType = PropTypes.exact({
  errors: PropTypes.arrayOf(PropTypes.string),
  checked: PropTypes.bool,
});

export const fieldPropType = PropTypes.exact({
  value: PropTypes.any,
  errors: PropTypes.arrayOf(PropTypes.string),
});

export const selectionFieldPropType = PropTypes.exact({
  selectedValue: PropTypes.any,
  options: PropTypes.arrayOf(
    PropTypes.exact({
      value: PropTypes.string,
      displayName: PropTypes.string,
    })
  ),
  errors: PropTypes.arrayOf(PropTypes.string),
});
