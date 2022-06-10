import React from "react";
import PropTypes from "prop-types";
import { useTranslation } from "react-i18next";
import styled from "styled-components";
import warningIcon from "../assets/icons/warning.svg";

const Error = styled.div`
  display: flex;
  margin-top: var(--spacing-02);

  &.invalid-feedback {
    font-size: var(--text-sb);
    font-family: var(--font-bold);
    color: var(--error-color);
  }

  img.invalid-feedback {
    display: inline-block;
    flex-basis: 3%;
    vertical-align: middle;
    height: 2em;
    width: 2em;
    margin-right: 9px;
  }
  div {
    margin-top: var(--spacing-01);
    display: inline-block;
    flex-basis: 97%;
  }
`;

function FieldError({ children, fieldName }) {
  const { t } = useTranslation();

  return (
    <Error className="invalid-feedback" htmlFor={fieldName} role="alert">
      <img
        className="invalid-feedback"
        src={warningIcon}
        aria-label={t("errors.warningImage.ariaLabel")}
      />{" "}
      <div>{children}</div>
    </Error>
  );
}

FieldError.propTypes = {
  children: PropTypes.node.isRequired,
  fieldName: PropTypes.string.isRequired,
};

export default FieldError;
