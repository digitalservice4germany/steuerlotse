import React from "react";
import PropTypes from "prop-types";
import warningIcon from "../assets/icons/warning.svg";

function FieldError({ children, fieldName }) {
  return (
    // TODO: styled-components
    <div className="invalid-feedback d-block" htmlFor={fieldName} role="alert">
      <img
        className="invalid-feedback"
        src={warningIcon}
        aria-label="errors.warning-image.aria-label" // TODO: intl
      />{" "}
      {children}
    </div>
  );
}

FieldError.propTypes = {
  children: PropTypes.node.isRequired,
  fieldName: PropTypes.string.isRequired,
};

export default FieldError;
