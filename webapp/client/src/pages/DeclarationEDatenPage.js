import PropTypes from "prop-types";
import React from "react";
import { useTranslation } from "react-i18next";
import FormFieldConsentBox from "../components/FormFieldConsentBox";
import FormHeader from "../components/FormHeader";
import StepForm from "../components/StepForm";
import StepHeaderButtons from "../components/StepHeaderButtons";
import { checkboxPropType } from "../lib/propTypes";

export default function DeclarationEDatenPage({
  stepHeader,
  form,
  fields,
  prevUrl,
}) {
  const { t } = useTranslation();

  return (
    <>
      <StepHeaderButtons url={prevUrl} />
      <FormHeader
        title={stepHeader.title}
        intro={[
          t("lotse.declarationEdaten.intro1"),
          t("lotse.declarationEdaten.intro2"),
        ]}
      />
      <StepForm {...form}>
        <FormFieldConsentBox
          autofocus
          required
          fieldName="declaration_edaten"
          fieldId="declaration_edaten"
          checked={fields.declarationEdaten.checked}
          labelText={t("lotse.declarationEdaten.labelText")}
          errors={fields.declarationEdaten.errors}
        />
      </StepForm>
    </>
  );
}

DeclarationEDatenPage.propTypes = {
  stepHeader: PropTypes.shape({
    title: PropTypes.string,
  }).isRequired,
  form: PropTypes.exact({
    action: PropTypes.string,
    csrfToken: PropTypes.string,
    showOverviewButton: PropTypes.bool,
    nextButtonLabel: PropTypes.string,
  }).isRequired,
  fields: PropTypes.exact({
    declarationEdaten: checkboxPropType,
  }).isRequired,
  prevUrl: PropTypes.string.isRequired,
};
