import PropTypes from "prop-types";
import React from "react";
import { selectionFieldPropType, stepHeaderPropType } from "../lib/propTypes";
import FahrtkostenpauschalePage from "./FahrtkostenpauschalePage";

export default function FahrtkostenpauschalePersonBPage({
  stepHeader,
  form,
  fields,
  prevUrl,
  fahrtkostenpauschaleAmount,
}) {
  return (
    <FahrtkostenpauschalePage
      {...{ stepHeader, form, prevUrl, fahrtkostenpauschaleAmount }}
      fields={{
        requestsFahrtkostenpauschale: {
          ...fields.personBRequestsFahrtkostenpauschale,
          name: "person_b_requests_fahrtkostenpauschale",
        },
      }}
    />
  );
}

FahrtkostenpauschalePersonBPage.propTypes = {
  stepHeader: stepHeaderPropType.isRequired,
  form: PropTypes.exact({
    action: PropTypes.string,
    csrfToken: PropTypes.string,
    showOverviewButton: PropTypes.bool,
    nextButtonLabel: PropTypes.string,
  }).isRequired,
  fields: PropTypes.exact({
    personBRequestsFahrtkostenpauschale: selectionFieldPropType,
  }).isRequired,
  fahrtkostenpauschaleAmount: PropTypes.number.isRequired,
  prevUrl: PropTypes.string.isRequired,
};
