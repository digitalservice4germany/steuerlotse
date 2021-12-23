import PropTypes from "prop-types";
import React from "react";
import { selectionFieldPropType } from "../lib/propTypes";
import PauschbetragPage from "./PauschbetragPage";

export default function PauschbetragPersonAPage({
  stepHeader,
  form,
  fields,
  prevUrl,
}) {
  return (
    <PauschbetragPage
      {...{ stepHeader, form, prevUrl }}
      fields={{
        wantsPauschbetrag: {
          selectedValue: fields.personAWantsPauschbetrag.selectedValue,
          errors: fields.personAWantsPauschbetrag.errors,
          options: fields.personAWantsPauschbetrag.options,
          name: "person_a_wants_pauschbetrag",
        },
      }}
    />
  );
}

PauschbetragPersonAPage.propTypes = {
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
    personAWantsPauschbetrag: selectionFieldPropType,
  }).isRequired,
  prevUrl: PropTypes.string.isRequired,
};
