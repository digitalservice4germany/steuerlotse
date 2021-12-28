import PropTypes from "prop-types";
import React from "react";
import { selectionFieldPropType } from "../lib/propTypes";
import PauschbetragPage from "./PauschbetragPage";

export default function PauschbetragPersonBPage({
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
          selectedValue: fields.personBRequestsPauschbetrag.selectedValue,
          errors: fields.personBRequestsPauschbetrag.errors,
          options: fields.personBRequestsPauschbetrag.options,
          name: "person_b_requests_pauschbetrag",
        },
      }}
    />
  );
}

PauschbetragPersonBPage.propTypes = {
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
    personBRequestsPauschbetrag: selectionFieldPropType,
  }).isRequired,
  pauschbetrag: PropTypes.number.isRequired,
  prevUrl: PropTypes.string.isRequired,
};
