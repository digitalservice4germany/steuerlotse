import React from "react";
import PropTypes from "prop-types";
import { useTranslation } from "react-i18next";
import styled from "styled-components";
import warningIcon from "../assets/icons/warning.svg";

const Error = styled.div`
  &.invalid-feedback {
    font-size: var(--text-sm);
    font-weight: var(--font-bold);
    color: var(--error-color);
  }

  img.invalid-feedback {
    display: inline;
    vertical-align: middle;
    height: 2em;
    width: 2em;
    margin-right: 9px;
  }
`;

function FieldError({ children, fieldName }) {
  const { t } = useTranslation();

  return (
    <Error
      className="invalid-feedback d-block"
      htmlFor={fieldName}
      role="alert"
    >
      <img
        className="invalid-feedback"
        src={warningIcon}
        aria-label={t("errors.warningImage.ariaLabel")}
      />{" "}
      {children}
    </Error>
  );
}

FieldError.propTypes = {
  children: PropTypes.node.isRequired,
  fieldName: PropTypes.string.isRequired,
};

export default FieldError;
