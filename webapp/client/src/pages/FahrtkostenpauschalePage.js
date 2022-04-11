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

export default function FahrtkostenpauschalePage({
  stepHeader,
  form,
  fields,
  prevUrl,
  fahrtkostenpauschaleAmount,
  plausibleDomain,
  plausibleProps,
}) {
  const { t } = useTranslation();

  return (
    <>
      <StepHeaderButtons url={prevUrl} />
      <FormHeader
        title={stepHeader.title}
        intro={
          <Trans
            i18nKey="lotse.fahrtkostenpauschale.introText"
            values={{ fahrtkostenpauschaleAmount }}
            components={{ bold: <b /> }}
          />
        }
      />
      <DetailsSeparated
        title={t("lotse.fahrtkostenpauschale.helpTitle")}
        detailsId="fahrtkostenpauschale.details"
      >
        <Trans
          t={t}
          i18nKey="lotse.fahrtkostenpauschale.helpText"
          values={{ fahrtkostenpauschaleAmount }}
          components={{ bold: <b /> }}
        />
      </DetailsSeparated>
      <StepForm
        plausibleDomain={plausibleDomain}
        plausibleProps={plausibleProps}
        {...form}
      >
        <FormFieldRadioGroup
          fieldName={fields.requestsFahrtkostenpauschale.name}
          fieldId={fields.requestsFahrtkostenpauschale.name}
          options={[
            {
              value: "yes",
              displayName: t(
                "lotse.fahrtkostenpauschale.requestsFahrtkostenpauschale.yesLabel"
              ),
            },
            {
              value: "no",
              displayName: t(
                "lotse.fahrtkostenpauschale.requestsFahrtkostenpauschale.noLabel"
              ),
            },
          ]}
          value={fields.requestsFahrtkostenpauschale.selectedValue}
          errors={fields.requestsFahrtkostenpauschale.errors}
        />
      </StepForm>
    </>
  );
}

FahrtkostenpauschalePage.propTypes = {
  stepHeader: stepHeaderPropType.isRequired,
  form: PropTypes.exact({
    action: PropTypes.string,
    csrfToken: PropTypes.string,
    showOverviewButton: PropTypes.bool,
    nextButtonLabel: PropTypes.string,
  }).isRequired,
  fields: PropTypes.exact({
    requestsFahrtkostenpauschale: extendedSelectionFieldPropType,
  }).isRequired,
  fahrtkostenpauschaleAmount: PropTypes.string.isRequired,
  prevUrl: PropTypes.string.isRequired,
  plausibleProps: PropTypes.shape({ method: PropTypes.string }),
  plausibleDomain: PropTypes.string,
};

FahrtkostenpauschalePage.defaultProps = {
  plausibleProps: undefined,
  plausibleDomain: null,
};
