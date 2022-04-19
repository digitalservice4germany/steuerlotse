import PropTypes from "prop-types";
import React from "react";
import { stepHeaderPropType, selectionFieldPropType } from "../lib/propTypes";
import PauschbetragPage from "./PauschbetragPage";

export default function PauschbetragPersonAPage({
  stepHeader,
  form,
  fields,
  pauschbetrag,
  prevUrl,
  plausibleDomain,
}) {
  const plausibleProps = {
    method: "CTA Pauschbetrag für Menschen mit Behinderung für Person A",
  };

  return (
    <PauschbetragPage
      plausibleDomain={plausibleDomain}
      plausibleProps={plausibleProps}
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
  stepHeader: stepHeaderPropType.isRequired,
  form: PropTypes.exact({
    action: PropTypes.string,
    csrfToken: PropTypes.string,
    showOverviewButton: PropTypes.bool,
    nextButtonLabel: PropTypes.string,
  }).isRequired,
  fields: PropTypes.exact({
    personARequestsPauschbetrag: selectionFieldPropType,
  }).isRequired,
  pauschbetrag: PropTypes.string.isRequired,
  prevUrl: PropTypes.string.isRequired,
  plausibleDomain: PropTypes.string,
};

PauschbetragPersonAPage.defaultProps = {
  plausibleDomain: null,
};
