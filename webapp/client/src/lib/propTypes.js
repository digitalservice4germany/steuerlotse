import PropTypes from "prop-types";
import FieldLabelScaffolding from "../components/FieldLabelScaffolding";

// Used if the field is handed to a more abstract component.
// e.g. MerkzeichenPersonAPage -> MerkzeichenPage
const abstractedFieldPropType = PropTypes.exact({
  name: PropTypes.string.isRequired,
  label: FieldLabelScaffolding.propTypes.label,
});

export const checkboxPropType = PropTypes.exact({
  errors: PropTypes.arrayOf(PropTypes.string),
  checked: PropTypes.bool,
});

export const fieldPropType = PropTypes.exact({
  value: PropTypes.any,
  errors: PropTypes.arrayOf(PropTypes.string),
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

export const extendedSelectionFieldPropType = PropTypes.exact({
  ...selectionFieldPropType,
  ...abstractedFieldPropType,
});
