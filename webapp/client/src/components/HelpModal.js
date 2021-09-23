import React, { useState } from "react";
import PropTypes from "prop-types";
import styled from "styled-components";
import { useTranslation } from "react-i18next";
import Modal from "react-bootstrap/Modal";

const Help = styled.button`
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

const Title = ({ children }) => (
  <h5 className="modal-title mb-n2">{children}</h5>
);
Title.propTypes = { children: PropTypes.node.isRequired };

function HelpModal({ title, body }) {
  const { t } = useTranslation();

  const [show, setShow] = useState(false);
  const toggle = () => setShow(!show);

  return (
    <>
      <Help
        className="btn ml-1"
        onClick={toggle}
        aria-label={t("button.help.ariaLabel")}
      >
        ?
      </Help>
      <Modal show={show} onHide={toggle} centered>
        <Modal.Header closeButton closeLabel={t("button.close.ariaLabel")}>
          <Modal.Title as={Title}>{title}</Modal.Title>
        </Modal.Header>
        <Modal.Body>{body}</Modal.Body>
      </Modal>
    </>
  );
}

HelpModal.propTypes = {
  title: PropTypes.string.isRequired,
  body: PropTypes.string.isRequired,
};

export default HelpModal;
