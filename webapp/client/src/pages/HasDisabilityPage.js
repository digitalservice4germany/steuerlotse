import PropTypes from "prop-types";
import React from "react";
import { Trans, useTranslation } from "react-i18next";
import FormHeader from "../components/FormHeader";
import FormFieldRadioGroup from "../components/FormFieldRadioGroup";
import StepForm from "../components/StepForm";
import StepHeaderButtons from "../components/StepHeaderButtons";
import Details from "../components/Details";
import { extendedFieldPropType } from "../lib/propTypes";

export default function HasDisabilityPage({
  form,
  fields,
  prevUrl,
  stepHeader,
  headerIntro,
}) {
  const { t } = useTranslation();

  const translationBold = function translationBold(key) {
    return <Trans t={t} i18nKey={key} components={{ bold: <b /> }} />;
  };

  return (
    <>
      <StepHeaderButtons url={prevUrl} />
      <FormHeader title={stepHeader.title} intro={headerIntro} />
      <StepForm {...form}>
        <Details //TODO Replace with DetailSeparate when component has been merged
          title={t("lotse.hasDisability.details.title")}
          detailsId={`${fields.hasDisability.name}_detail`}
        >
          {translationBold("lotse.hasDisability.details.text")}
        </Details>
        <FormFieldRadioGroup
          fieldId={fields.hasDisability.name}
          fieldName={fields.hasDisability.name}
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
          value={fields.hasDisability.value}
          errors={fields.hasDisability.errors}
          required
        />
      </StepForm>
    </>
  );
}

HasDisabilityPage.propTypes = {
  stepHeader: PropTypes.shape({
    title: PropTypes.string,
  }).isRequired,
  headerIntro: PropTypes.string.isRequired,
  form: PropTypes.exact({
    action: PropTypes.string,
    csrfToken: PropTypes.string,
    showOverviewButton: PropTypes.bool,
    nextButtonLabel: PropTypes.string,
  }).isRequired,
  fields: PropTypes.exact({
    hasDisability: extendedFieldPropType,
  }).isRequired,
  numUsers: PropTypes.number.isRequired,
  prevUrl: PropTypes.string.isRequired,
};
