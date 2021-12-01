import PropTypes from "prop-types";
import React from "react";
import { useTranslation } from "react-i18next";
import FormHeader from "../components/FormHeader";
import StepForm from "../components/StepForm";
import StepHeaderButtons from "../components/StepHeaderButtons";
import { fieldPropType } from "../lib/propTypes";
import FormFieldTextInput from "../components/FormFieldTextInput";

export default function TelephoneNumberPage({
  stepHeader,
  form,
  fields,
  prevUrl,
}) {
  const { t } = useTranslation();

  return (
    <>
      <StepHeaderButtons url={prevUrl} />
      <FormHeader {...stepHeader} />
      <StepForm {...form}>
        <FormFieldTextInput
          fieldName="telephone_number"
          fieldId="telephone_number"
          value={fields.telephoneNumber.value}
          label={{
            text: t("lotse.telephoneNumber.fieldTelephoneNumber.label"),
            showOptionalTag: true,
          }}
          errors={fields.telephoneNumber.errors}
        />
      </StepForm>
    </>
  );
}

TelephoneNumberPage.propTypes = {
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
    telephoneNumber: fieldPropType,
  }).isRequired,
  prevUrl: PropTypes.string.isRequired,
};
