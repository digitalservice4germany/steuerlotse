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
        wantsPauschbetrag: {
          ...fields.personAWantsPauschbetrag,
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
  pauschbetrag: PropTypes.number.isRequired,
  prevUrl: PropTypes.string.isRequired,
};
