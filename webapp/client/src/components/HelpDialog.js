import React from "react";
import PropTypes from "prop-types";

function HelpDialog({ dialogFieldId, title, helpText }) {
  return (
    <div
      className="modal fade"
      id={`help_dialog_${dialogFieldId}`}
      tabIndex="-1"
      role="dialog"
      aria-hidden="true"
    >
      <div className="modal-dialog modal-dialog-centered" role="document">
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title mb-n2">{title}</h5>
            <button
              type="button"
              className="close"
              data-dismiss="modal"
              aria-label="button.close.aria-label" // TODO: intl
            >
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div className="modal-body">{helpText}</div>
        </div>
      </div>
    </div>
  );
}

HelpDialog.propTypes = {
  dialogFieldId: PropTypes.string.isRequired,
  title: PropTypes.string.isRequired,
  helpText: PropTypes.string.isRequired,
};

export default HelpDialog;
