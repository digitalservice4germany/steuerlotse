import PropTypes from "prop-types";
import React from "react";
import { selectionFieldPropType } from "../lib/propTypes";
import PauschbetragPage from "./PauschbetragPage";

export default function PauschbetragPersonAPage({
  stepHeader,
  form,
  fields,
  pauschbetrag,
  prevUrl,
}) {
  return (
    <PauschbetragPage
      {...{ stepHeader, form, pauschbetrag, prevUrl }}
      fields={{
        requestsPauschbetrag: {
          ...fields.personARequestsPauschbetrag,
          name: "person_a_requests_pauschbetrag",
        },
      }}
    />
  );
}

PauschbetragPersonAPage.propTypes = {
  stepHeader: PropTypes.shape({
    title: PropTypes.string,
  }).isRequired,
  form: PropTypes.exact({
    action: PropTypes.string,
    csrfToken: PropTypes.string,
    showOverviewButton: PropTypes.bool,
    nextButtonLabel: PropTypes.string,
  }).isRequired,
  fields: PropTypes.exact({
    personARequestsPauschbetrag: selectionFieldPropType,
  }).isRequired,
  pauschbetrag: PropTypes.number.isRequired,
  prevUrl: PropTypes.string.isRequired,
};
