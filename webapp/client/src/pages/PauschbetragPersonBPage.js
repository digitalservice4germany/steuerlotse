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
        wantsPauschbetrag: {
          selectedValue: fields.personBWantsPauschbetrag.selectedValue,
          errors: fields.personBWantsPauschbetrag.errors,
          options: fields.personBWantsPauschbetrag.options,
          name: "person_b_wants_pauschbetrag",
        },
      }}
    />
  );
}

PauschbetragPersonBPage.propTypes = {
  stepHeader: PropTypes.exact({
    title: PropTypes.string,
    intro: PropTypes.string,
  }).isRequired,
  form: PropTypes.exact({
    action: PropTypes.string,
    csrfToken: PropTypes.string,
    showOverviewButton: PropTypes.bool,
    nextButtonLabel: PropTypes.string,
  }).isRequired,
  fields: PropTypes.exact({
    personBWantsPauschbetrag: selectionFieldPropType,
  }).isRequired,
  pauschbetrag: PropTypes.number.isRequired,
  prevUrl: PropTypes.string.isRequired,
};
