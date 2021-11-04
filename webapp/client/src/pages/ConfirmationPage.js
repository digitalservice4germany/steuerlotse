import PropTypes from "prop-types";
import React from "react";
import { Trans, useTranslation } from "react-i18next";
import FormFieldConsentBox from "../components/FormFieldConsentBox";
import FormHeader from "../components/FormHeader";
import StepForm from "../components/StepForm";
import StepHeaderButtons from "../components/StepHeaderButtons";
import { checkboxPropType } from "../lib/propTypes";

export default function ConfirmationPage({
  stepHeader,
  form,
  fields,
  dataPrivacyLink,
  termsOfServiceLink,
}) {
  const { t } = useTranslation();

  return (
    <>
      <StepHeaderButtons />
      <FormHeader {...stepHeader} />
      <StepForm {...form} nextButtonLabel={t("lotse.confirmation.finish")}>
        <FormFieldConsentBox
          required
          fieldName="confirm_data_privacy"
          fieldId="confirm_data_privacy"
          checked={fields.confirmDataPrivacy.checked}
          labelText={
            <Trans
              t={t}
              i18nKey="unlockCodeRequest.fieldRegistrationConfirmDataPrivacy.labelText"
              components={{
                // The anchors get content in the translation file
                // eslint-disable-next-line jsx-a11y/anchor-has-content
                dataPrivacyLink: <a href={dataPrivacyLink} />,
                taxGdprLink: (
                  // eslint-disable-next-line jsx-a11y/anchor-has-content
                  <a
                    href="https://www.bundesfinanzministerium.de/Content/DE/Downloads/BMF_Schreiben/Weitere_Steuerthemen/Abgabenordnung/2020-07-01-Korrektur-Allgemeine-Informationen-Datenschutz-Grundverordnung-Steuerverwaltung-anlage-1.pdf?__blob=publicationFile&v=3"
                    rel="noreferrer"
                    target="_blank"
                  />
                ),
              }}
            />
          }
          errors={fields.confirmDataPrivacy.errors}
        />
        <FormFieldConsentBox
          required
          fieldName="confirm_terms_of_service"
          fieldId="confirm_terms_of_service"
          checked={fields.confirmTermsOfService.checked}
          labelText={
            <Trans
              t={t}
              i18nKey="unlockCodeRequest.fieldRegistrationConfirmTermsOfService.labelText"
              components={{
                // The anchors get content in the translation file
                // eslint-disable-next-line jsx-a11y/anchor-has-content
                termsOfServiceLink: <a href={termsOfServiceLink} />,
              }}
            />
          }
          errors={fields.confirmTermsOfService.errors}
        />
      </StepForm>
    </>
  );
}

ConfirmationPage.propTypes = {
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
    confirmDataPrivacy: checkboxPropType,
    confirmTermsOfService: checkboxPropType,
  }).isRequired,
  dataPrivacyLink: PropTypes.string.isRequired,
  termsOfServiceLink: PropTypes.string.isRequired,
};
