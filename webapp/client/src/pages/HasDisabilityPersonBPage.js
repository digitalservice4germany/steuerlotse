import PropTypes from "prop-types";
import React from "react";
import { Trans, useTranslation } from "react-i18next";
import FormHeader from "../components/FormHeader";
import FormFieldRadioGroup from "../components/FormFieldRadioGroup";
import StepForm from "../components/StepForm";
import StepHeaderButtons from "../components/StepHeaderButtons";
import Details from "../components/Details";
import { fieldPropType } from "../lib/propTypes";

export default function HasDisabilityPersonBPage({
  form,
  fields,
  prevUrl,
  stepHeader,
}) {
  const { t } = useTranslation();

  const translationBold = function translationBold(key) {
    return <Trans t={t} i18nKey={key} components={{ bold: <b /> }} />;
  };

  return (
    <>
      <StepHeaderButtons url={prevUrl} />
      <FormHeader
        title={stepHeader.title}
        intro={translationBold("lotse.hasDisability.intro_person_b")}
      />
      <StepForm {...form}>
        <Details
          title={t("lotse.hasDisability.details.title")}
          detailsId="person_b_has_disability"
        >
          {translationBold("lotse.hasDisability.details.text")}
        </Details>
        <FormFieldRadioGroup
          fieldId="person_b_has_disability"
          fieldName="person_b_has_disability"
          options={[
            {
              value: "yes",
              displayName: t("fields.yesNoSwitch.Yes"),
            },
            {
              value: "no",
              displayName: t("fields.yesNoSwitch.No"),
            },
          ]}
          value={fields.personBHasDisability.value}
          errors={fields.personBHasDisability.errors}
          required
        />
      </StepForm>
    </>
  );
}

HasDisabilityPersonBPage.propTypes = {
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
    personBHasDisability: fieldPropType,
  }).isRequired,
  prevUrl: PropTypes.string.isRequired,
};
