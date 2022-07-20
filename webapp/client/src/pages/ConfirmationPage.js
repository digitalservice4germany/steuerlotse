import PropTypes from "prop-types";
import React, { useState } from "react";
import { Trans, useTranslation } from "react-i18next";
import styled from "styled-components";
import FormFieldConsentBox from "../components/FormFieldConsentBox";
import FormHeader from "../components/FormHeader";
import StepForm from "../components/StepForm";
import StepHeaderButtons from "../components/StepHeaderButtons";
import { checkboxPropType } from "../lib/propTypes";

const Link = styled.a`
  ${({ disable }) =>
    disable &&
    `
            pointer-events: none;
    cursor: default;
    color: var(--blue-400) !important;
  `}
`;

export default function ConfirmationPage({
  stepHeader,
  form,
  fields,
  dataPrivacyLink,
  termsOfServiceLink,
  prevUrl,
}) {
  const { t } = useTranslation();

  const [isDisable, setIsDisable] = useState(false);

  const sendDisableCall = () => {
    setIsDisable(true);
  };

  return (
    <>
      <StepHeaderButtons url={prevUrl} disable={isDisable} />
      <FormHeader {...stepHeader} />
      <StepForm
        {...form}
        nextButtonLabel={t("lotse.confirmation.finish")}
        sendDisableCall={sendDisableCall}
        waitingMessages={{
          firstMessage: t("waitingMoment.confirmation.firstMessage"),
          secondMessage: t("waitingMoment.confirmation.secondMessage"),
        }}
      >
        <FormFieldConsentBox
          disable={isDisable}
          required
          fieldName="confirm_data_privacy"
          fieldId="confirm_data_privacy"
          checked={fields.confirmDataPrivacy.checked}
          labelText={
            <Trans
              t={t}
              i18nKey="lotse.confirmation.fieldRegistrationConfirmDataPrivacy.labelText"
              components={{
                // The anchors get content in the translation file
                // eslint-disable-next-line jsx-a11y/anchor-has-content
                dataPrivacyLink: (
                  <Link
                    tabIndex={isDisable ? "-1" : undefined}
                    disable={isDisable}
                    href={dataPrivacyLink}
                  />
                ),
                taxGdprLink: (
                  // eslint-disable-next-line jsx-a11y/anchor-has-content
                  <Link
                    tabIndex={isDisable ? "-1" : undefined}
                    disable={isDisable}
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
          disable={isDisable}
          required
          fieldName="confirm_terms_of_service"
          fieldId="confirm_terms_of_service"
          checked={fields.confirmTermsOfService.checked}
          labelText={
            <Trans
              t={t}
              i18nKey="lotse.confirmation.fieldRegistrationConfirmTermsOfService.labelText"
              components={{
                // The anchors get content in the translation file
                // eslint-disable-next-line jsx-a11y/anchor-has-content
                termsOfServiceLink: (
                  <Link
                    tabIndex={isDisable ? "-1" : undefined}
                    disable={isDisable}
                    href={termsOfServiceLink}
                  />
                ),
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
  prevUrl: PropTypes.string.isRequired,
};
