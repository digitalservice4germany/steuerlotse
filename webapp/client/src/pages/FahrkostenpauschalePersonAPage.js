import PropTypes from "prop-types";
import React from "react";
import { selectionFieldPropType, stepHeaderPropType } from "../lib/propTypes";
import FahrkostenpauschalePage from "./FahrkostenpauschalePage";

export default function FahrkostenpauschalePersonAPage({
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
          ...fields.personARequestsFahrkostenpauschale,
          name: "person_a_requests_fahrkostenpauschale",
        },
      }}
    />
  );
}

FahrkostenpauschalePersonAPage.propTypes = {
  stepHeader: stepHeaderPropType.isRequired,
  form: PropTypes.exact({
    action: PropTypes.string,
    csrfToken: PropTypes.string,
    showOverviewButton: PropTypes.bool,
    nextButtonLabel: PropTypes.string,
  }).isRequired,
  fields: PropTypes.exact({
    personARequestsFahrkostenpauschale: selectionFieldPropType,
  }).isRequired,
  fahrkostenpauschaleAmount: PropTypes.string.isRequired,
  prevUrl: PropTypes.string.isRequired,
};
