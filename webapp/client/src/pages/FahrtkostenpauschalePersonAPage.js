import PropTypes from "prop-types";
import React from "react";
import { selectionFieldPropType, stepHeaderPropType } from "../lib/propTypes";
import FahrtkostenpauschalePage from "./FahrtkostenpauschalePage";

export default function FahrtkostenpauschalePersonAPage({
  stepHeader,
  form,
  fields,
  prevUrl,
  fahrtkostenpauschaleAmount,
  plausibleDomain,
}) {
  const plausibleProps = {
    method: "CTA Behinderungsbedingte Fahrtkostenpauschale für Person A",
  };

  return (
    <FahrtkostenpauschalePage
      plausibleDomain={plausibleDomain}
      plausibleProps={plausibleProps}
      {...{ stepHeader, form, prevUrl, fahrtkostenpauschaleAmount }}
      fields={{
        requestsFahrtkostenpauschale: {
          ...fields.personARequestsFahrtkostenpauschale,
          name: "person_a_requests_fahrtkostenpauschale",
        },
      }}
    />
  );
}

FahrtkostenpauschalePersonAPage.propTypes = {
  stepHeader: stepHeaderPropType.isRequired,
  form: PropTypes.exact({
    action: PropTypes.string,
    csrfToken: PropTypes.string,
    showOverviewButton: PropTypes.bool,
    nextButtonLabel: PropTypes.string,
  }).isRequired,
  fields: PropTypes.exact({
    personARequestsFahrtkostenpauschale: selectionFieldPropType,
  }).isRequired,
  fahrtkostenpauschaleAmount: PropTypes.number.isRequired,
  prevUrl: PropTypes.string.isRequired,
  plausibleDomain: PropTypes.string,
};

FahrtkostenpauschalePersonAPage.defaultProps = {
  plausibleDomain: null,
};
