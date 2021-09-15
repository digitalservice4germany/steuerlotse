import React from "react";
import PropTypes from "prop-types";
import { useTranslation } from "react-i18next";
import warningIcon from "../assets/icons/warning.svg";

function FieldError({ children, fieldName }) {
  const { t } = useTranslation();

  return (
    // TODO: styled-components
    <div className="invalid-feedback d-block" htmlFor={fieldName} role="alert">
      <img
        className="invalid-feedback"
        src={warningIcon}
        aria-label={t("errors.warningImage.ariaLabel")}
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
