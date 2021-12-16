import PropTypes from "prop-types";
import React from "react";
import { useTranslation } from "react-i18next";
import FormHeader from "../components/FormHeader";
import FormFieldRadio from "../components/FormFieldRadio";
import StepForm from "../components/StepForm";
import StepHeaderButtons from "../components/StepHeaderButtons";
import Details from "../components/Details";

export default function DisabilityQuestionPage({
  stepHeader,
  form,
  fields,
  prevUrl,
  errors,
}) {
  const { t } = useTranslation();

  return (
    <>
      <StepHeaderButtons url={prevUrl} />
      <FormHeader {...stepHeader} />
      <StepForm {...form}>
        <Details
          title={t("lotse.disabilityQuestion.details.title")}
          detailsId="disability_details"
        >
          {{
            paragraphs: [t("lotse.disabilityQuestion.details.text")],
          }}
        </Details>
        <FormFieldRadio
          fieldId="disability_radio"
          fieldName="disability_radio"
          options={[
            {
              value: "Yes",
              displayName: t("fields.switch.Yes"),
            },
            {
              value: "No",
              displayName: t("fields.switch.No"),
            },
          ]}
          errors={errors}
          value={fields.disabilityExists}
          required
        />
      </StepForm>
    </>
  );
}

DisabilityQuestionPage.propTypes = {
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
    disabilityExists: PropTypes.string,
  }).isRequired,
  prevUrl: PropTypes.string.isRequired,
  errors: PropTypes.arrayOf(PropTypes.string).isRequired,
};
