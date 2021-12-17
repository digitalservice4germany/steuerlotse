import PropTypes from "prop-types";
import React from "react";
import FormHeader from "../components/FormHeader";
import StepForm from "../components/StepForm";
import StepHeaderButtons from "../components/StepHeaderButtons";
import { selectionFieldPropType } from "../lib/propTypes";
import FormFieldRadio from "../components/FormFieldRadio";

export default function PauschbetragPagePersonA({
  stepHeader,
  form,
  fields,
  prevUrl,
}) {
  return (
    <>
      <StepHeaderButtons url={prevUrl} />
      <FormHeader {...stepHeader} />
      <StepForm {...form}>
        <FormFieldRadio
          fieldName="person_a_wants_pauschbetrag"
          fieldId="person_a_wants_pauschbetrag"
          label={{ text: "" }}
          // TODO set text here, not in server
          options={fields.personAWantsPauschbetrag.options}
          value={fields.personAWantsPauschbetrag.selectedValue}
          errors={fields.personAWantsPauschbetrag.errors}
        />
      </StepForm>
    </>
  );
}

PauschbetragPagePersonA.propTypes = {
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
