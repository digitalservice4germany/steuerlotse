import PropTypes from "prop-types";
import React from "react";
import { Trans, useTranslation } from "react-i18next";
import FormHeader from "../components/FormHeader";
import FormFieldRadio from "../components/FormFieldRadio";
import StepForm from "../components/StepForm";
import StepHeaderButtons from "../components/StepHeaderButtons";
import Details from "../components/Details";

export default function HasDisabilityPage({ form, fields, prevUrl, errors }) {
  const { t } = useTranslation();

  const tbold = function (key) {
    return <Trans t={t} i18nKey={key} components={{ bold: <b /> }} />;
  };

  return (
    <>
      <StepHeaderButtons url={prevUrl} />
      <FormHeader
        title={t("lotse.HasDisability.title")}
        intro={t("lotse.HasDisability.intro")}
      />
      <StepForm {...form}>
        <Details
          title={t("lotse.HasDisability.details.title")}
          detailsId="has_disability"
        >
          {{
            paragraphs: [tbold("lotse.HasDisability.details.text")],
          }}
        </Details>
        <FormFieldRadio
          fieldId="has_disability"
          fieldName="has_disability"
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
          value={fields.hasDisability}
          required
        />
      </StepForm>
    </>
  );
}

HasDisabilityPage.propTypes = {
  form: PropTypes.exact({
    action: PropTypes.string,
    csrfToken: PropTypes.string,
    showOverviewButton: PropTypes.bool,
    nextButtonLabel: PropTypes.string,
  }).isRequired,
  fields: PropTypes.exact({
    hasDisability: PropTypes.string,
  }).isRequired,
  prevUrl: PropTypes.string.isRequired,
  errors: PropTypes.arrayOf(PropTypes.string).isRequired,
};
