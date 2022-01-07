import PropTypes from "prop-types";
import React from "react";
import { Trans, useTranslation } from "react-i18next";
import DetailsSeparated from "../components/DetailsSeparated";
import FormHeader from "../components/FormHeader";
import StepForm from "../components/StepForm";
import StepHeaderButtons from "../components/StepHeaderButtons";
import {
  extendedSelectionFieldPropType,
  stepHeaderPropType,
} from "../lib/propTypes";
import FormFieldRadioGroup from "../components/FormFieldRadioGroup";

export default function FahrkostenpauschalePage({
  stepHeader,
  form,
  fields,
  prevUrl,
  fahrkostenpauschaleAmount,
}) {
  const { t } = useTranslation();

  return (
    <>
      <StepHeaderButtons url={prevUrl} />
      <FormHeader
        title={stepHeader.title}
        intro={
          <Trans
            i18nKey="lotse.fahrkostenpauschale.introText"
            values={{ fahrkostenpauschaleAmount }}
            components={{ bold: <b /> }}
          />
        }
      />
      <DetailsSeparated
        title={t("lotse.fahrkostenpauschale.helpTitle")}
        detailsId="fahrkostenpauschale.details"
      >
        <Trans
          t={t}
          i18nKey="lotse.fahrkostenpauschale.helpText"
          values={{ fahrkostenpauschaleAmount }}
          components={{ bold: <b /> }}
        />
      </DetailsSeparated>
      <StepForm {...form}>
        <FormFieldRadioGroup
          fieldName={fields.requestsFahrkostenpauschale.name}
          fieldId={fields.requestsFahrkostenpauschale.name}
          options={[
            {
              value: "yes",
              displayName: t(
                "lotse.fahrkostenpauschale.requestsFahrkostenpauschale.yesLabel"
              ),
            },
            {
              value: "no",
              displayName: t(
                "lotse.fahrkostenpauschale.requestsFahrkostenpauschale.noLabel"
              ),
            },
          ]}
          value={fields.requestsFahrkostenpauschale.selectedValue}
          errors={fields.requestsFahrkostenpauschale.errors}
        />
      </StepForm>
    </>
  );
}

FahrkostenpauschalePage.propTypes = {
  stepHeader: stepHeaderPropType.isRequired,
  form: PropTypes.exact({
    action: PropTypes.string,
    csrfToken: PropTypes.string,
    showOverviewButton: PropTypes.bool,
    nextButtonLabel: PropTypes.string,
  }).isRequired,
  fields: PropTypes.exact({
    requestsFahrkostenpauschale: extendedSelectionFieldPropType,
  }).isRequired,
  fahrkostenpauschaleAmount: PropTypes.string.isRequired,
  prevUrl: PropTypes.string.isRequired,
};
