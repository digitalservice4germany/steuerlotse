import PropTypes from "prop-types";
import React from "react";
import { fieldPropType, stepHeaderPropType } from "../lib/propTypes";
import FahrkostenpauschalePage from "./FahrkostenpauschalePage";

export default function FahrkostenpauschalePersonBPage({
  stepHeader,
  form,
  fields,
  prevUrl,
  fahrkostenpauschaleAmount,
}) {
  return (
    <FahrkostenpauschalePage
      {...{ stepHeader, form, prevUrl, fahrkostenpauschaleAmount }}
      fields={{
        requestsFahrkostenpauschale: {
          ...fields.personBRequestsFahrkostenpauschale,
          name: "person_b_requests_fahrkostenpauschale",
        },
      }}
    />
  );
}

FahrkostenpauschalePersonBPage.propTypes = {
  stepHeader: stepHeaderPropType.isRequired,
  form: PropTypes.exact({
    action: PropTypes.string,
    csrfToken: PropTypes.string,
    showOverviewButton: PropTypes.bool,
    nextButtonLabel: PropTypes.string,
  }).isRequired,
  fields: PropTypes.exact({
    personBRequestsFahrkostenpauschale: fieldPropType,
  }).isRequired,
  fahrkostenpauschaleAmount: PropTypes.number.isRequired,
  prevUrl: PropTypes.string.isRequired,
};
