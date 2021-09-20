import React from "react";
import PropTypes from "prop-types";
import styled from "styled-components";

const Help = styled.a`
  width: 22px !important;
  height: 22px !important;
  border-radius: 11px !important;
  padding: 0;
  font-size: 0.9em;
  font-weight: bold;
  display: inline-flex;
  align-items: center;
  justify-content: center;

  background: var(--link-color);
  color: var(--inverse-text-color) !important;
  text-decoration: none;

  &:hover {
    background: var(--link-hover-color);
    color: var(--inverse-text-color) !important;
    text-decoration: none;
  }

  &:focus {
    background: var(--focus-color);
    color: var(--text-color) !important;
    text-decoration: none;
  }
`;

function HelpButton({ dialogFieldId }) {
  return (
    // TODO: intl
    <Help
      href=""
      className="btn ml-1"
      data-toggle="modal"
      data-target={`#help_dialog_${dialogFieldId}`}
      aria-label="button.help"
    >
      ?
    </Help>
  );
}
HelpButton.propTypes = {
  dialogFieldId: PropTypes.string.isRequired,
};

export default HelpButton;
