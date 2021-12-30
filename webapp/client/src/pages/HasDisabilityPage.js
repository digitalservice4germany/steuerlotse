import PropTypes from "prop-types";
import React from "react";
import { Trans, useTranslation } from "react-i18next";
import FormHeader from "../components/FormHeader";
import FormFieldRadioGroup from "../components/FormFieldRadioGroup";
import StepForm from "../components/StepForm";
import StepHeaderButtons from "../components/StepHeaderButtons";
import DetailsSeparated from "../components/DetailsSeparated";
import { extendedFieldPropType } from "../lib/propTypes";

export default function HasDisabilityPage({
  form,
  fields,
  stepHeader,
  headerIntro,
  prevUrl,
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
        <DetailsSeparated
          title={t("lotse.hasDisability.details.title")}
          detailsId={`${fields.hasDisability.name}_detail`}
        >
          {translationBold("lotse.hasDisability.details.text")}
        </DetailsSeparated>
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
  headerIntro: PropTypes.oneOfType([PropTypes.string, PropTypes.object])
    .isRequired,
  form: PropTypes.exact({
    action: PropTypes.string,
    csrfToken: PropTypes.string,
    showOverviewButton: PropTypes.bool,
    nextButtonLabel: PropTypes.string,
  }).isRequired,
  fields: PropTypes.exact({
    hasDisability: extendedFieldPropType,
  }).isRequired,
  prevUrl: PropTypes.string.isRequired,
};
