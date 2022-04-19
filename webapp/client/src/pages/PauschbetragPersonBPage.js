import PropTypes from "prop-types";
import React from "react";
import { stepHeaderPropType, selectionFieldPropType } from "../lib/propTypes";
import PauschbetragPage from "./PauschbetragPage";

export default function PauschbetragPersonBPage({
  stepHeader,
  form,
  fields,
  pauschbetrag,
  prevUrl,
  plausibleDomain,
}) {
  const plausibleProps = {
    method: "CTA Pauschbetrag für Menschen mit Behinderung für Person B",
  };

  return (
    <PauschbetragPage
      plausibleDomain={plausibleDomain}
      plausibleProps={plausibleProps}
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
  stepHeader: stepHeaderPropType.isRequired,
  form: PropTypes.exact({
    action: PropTypes.string,
    csrfToken: PropTypes.string,
    showOverviewButton: PropTypes.bool,
    nextButtonLabel: PropTypes.string,
  }).isRequired,
  fields: PropTypes.exact({
    personBRequestsPauschbetrag: selectionFieldPropType,
  }).isRequired,
  pauschbetrag: PropTypes.string.isRequired,
  prevUrl: PropTypes.string.isRequired,
  plausibleDomain: PropTypes.string,
};

PauschbetragPersonBPage.defaultProps = {
  plausibleDomain: null,
};
