import PropTypes from "prop-types";
import React, { useState } from "react";
import { Trans, useTranslation } from "react-i18next";
import styled from "styled-components";
import Details from "../components/Details";
import FormFieldConsentBox from "../components/FormFieldConsentBox";
import FormFieldDate from "../components/FormFieldDate";
import FormFieldIdNr from "../components/FormFieldIdNr";
import FormHeader from "../components/FormHeader";
import FormRowCentered from "../components/FormRowCentered";
import StepFormAsync from "../components/StepFormAsync";
import StepHeaderButtons from "../components/StepHeaderButtons";
import SubHeading from "../components/SubHeading";
import { checkboxPropType, fieldPropType } from "../lib/propTypes";

const Link = styled.a`
  ${({ disable }) =>
    disable &&
    `
            pointer-events: none;
    cursor: default;
    color: var(--blue-400) !important;
  `}
`;

export default function RegistrationPage({
  stepHeader,
  form,
  fields,
  loginLink,
  eligibilityLink,
  termsOfServiceLink,
  dataPrivacyLink,
  waitingMomentActive,
}) {
  const { t } = useTranslation();
  const translateText = function translateText(key) {
    return (
      <Trans
        t={t}
        i18nKey={key}
        components={{
          steuerIdLink: (
            // eslint-disable-next-line jsx-a11y/anchor-has-content
            <a
              aria-label="Info zur Steuerliche Identifikationsnummer"
              href="https://www.bzst.de/DE/Privatpersonen/SteuerlicheIdentifikationsnummer/steuerlicheidentifikationsnummer_node.html"
              target="_blank"
              rel="noreferrer"
            />
          ),
        }}
      />
    );
  };

  const [isDisable, setIsDisable] = useState(waitingMomentActive);

  const sendDisableCall = () => {
    setIsDisable(true);
  };

  return (
    <>
      <StepHeaderButtons />
      <FormHeader
        {...stepHeader}
        intro={
          <Trans
            t={t}
            i18nKey="unlockCodeRequest.input.intro"
            components={{ bold: <b /> }}
          />
        }
      />
      <StepFormAsync
        {...form}
        loadingFromOutside={waitingMomentActive}
        sendDisableCall={sendDisableCall}
        waitingMessages={{
          firstMessage: t("waitingMoment.registration.firstMessage"),
          secondMessage: t("waitingMoment.registration.secondMessage"),
        }}
        explanatoryButtonText={
          <Trans
            t={t}
            i18nKey="unlockCodeRequest.gotFsc"
            components={{
              // The anchors get content in the translation file
              // eslint-disable-next-line jsx-a11y/anchor-has-content
              loginLink: <a href={loginLink} />,
            }}
          />
        }
      >
        <FormRowCentered>
          <FormFieldDate
            disable={isDisable}
            autofocus
            required
            fieldName="dob"
            fieldId="dob"
            values={fields.dob.value}
            label={{
              text: t("fields.dob.labelText"),
            }}
            errors={fields.dob.errors}
          />
        </FormRowCentered>
        <FormRowCentered>
          <FormFieldIdNr
            disable={isDisable}
            required
            fieldName="idnr"
            fieldId="idnr"
            values={fields.idnr.value}
            label={{
              text: t("fields.idnr.labelText"),
            }}
            details={{
              title: t("fields.idnr.help.title"),
              text: translateText("fields.idnr.help.text"),
            }}
            errors={fields.idnr.errors}
          />
        </FormRowCentered>
        <SubHeading>
          {t("unlockCodeRequest.dataPrivacyAndAgb.title")}
        </SubHeading>
        <FormFieldConsentBox
          disable={isDisable}
          required
          fieldName="registration_confirm_data_privacy"
          fieldId="registration_confirm_data_privacy"
          checked={fields.registrationConfirmDataPrivacy.checked}
          labelText={
            <Trans
              t={t}
              i18nKey="unlockCodeRequest.fieldRegistrationConfirmDataPrivacy.labelText"
              components={{
                // The anchors get content in the translation file
                // eslint-disable-next-line jsx-a11y/anchor-has-content
                dataPrivacyLink: (
                  <Link
                    disable={isDisable}
                    tabIndex={isDisable ? "-1" : undefined}
                    href={dataPrivacyLink}
                    rel="noreferrer"
                    target="_blank"
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
          errors={fields.registrationConfirmDataPrivacy.errors}
        />
        <FormFieldConsentBox
          disable={isDisable}
          required
          fieldName="registration_confirm_terms_of_service"
          fieldId="registration_confirm_terms_of_service"
          checked={fields.registrationConfirmTermsOfService.checked}
          labelText={
            <Trans
              t={t}
              i18nKey="unlockCodeRequest.fieldRegistrationConfirmTermsOfService.labelText"
              components={{
                // The anchors get content in the translation file
                // eslint-disable-next-line jsx-a11y/anchor-has-content
                termsOfServiceLink: (
                  <Link
                    disable={isDisable}
                    tabIndex={isDisable ? "-1" : undefined}
                    href={termsOfServiceLink}
                  />
                ),
              }}
            />
          }
          errors={fields.registrationConfirmTermsOfService.errors}
        />
        <FormFieldConsentBox
          disable={isDisable}
          required
          fieldName="registration_confirm_incomes"
          fieldId="registration_confirm_incomes"
          checked={fields.registrationConfirmIncomes.checked}
          labelText={
            <Trans
              t={t}
              i18nKey="unlockCodeRequest.fieldRegistrationConfirmIncomes.labelText"
              components={{
                // The anchors get content in the translation file
                // eslint-disable-next-line jsx-a11y/anchor-has-content
                eligibilityLink: (
                  <Link
                    disable={isDisable}
                    tabIndex={isDisable ? "-1" : undefined}
                    href={eligibilityLink}
                  />
                ),
              }}
            />
          }
          errors={fields.registrationConfirmIncomes.errors}
        />
        <SubHeading>{t("unlockCodeRequest.eData.title")}</SubHeading>
        <Details
          disable={isDisable}
          title={t("unlockCodeRequest.eData.helpTitle")}
          detailsId="registration_confirm_e_data"
        >
          <p>
            <Trans
              t={t}
              i18nKey="unlockCodeRequest.eData.helpText"
              components={{ bold: <b /> }}
            />
          </p>
        </Details>
        <FormFieldConsentBox
          disable={isDisable}
          required
          fieldName="registration_confirm_e_data"
          fieldId="registration_confirm_e_data"
          checked={fields.registrationConfirmEData.checked}
          labelText={t(
            "unlockCodeRequest.fieldRegistrationConfirmEData.labelText"
          )}
          errors={fields.registrationConfirmEData.errors}
        />
      </StepFormAsync>
    </>
  );
}

RegistrationPage.propTypes = {
  stepHeader: PropTypes.exact({
    // TODO: define these here, not in Python
    title: PropTypes.string,
    intro: PropTypes.string,
  }).isRequired,
  form: PropTypes.exact({
    action: PropTypes.string, // TODO: does this change? if not, define here, not in Python
    csrfToken: PropTypes.string,
    showOverviewButton: PropTypes.bool,
    nextButtonLabel: PropTypes.string, // TODO: define here, not in Python
  }).isRequired,
  fields: PropTypes.exact({
    idnr: fieldPropType,
    dob: fieldPropType,
    registrationConfirmDataPrivacy: checkboxPropType,
    registrationConfirmTermsOfService: checkboxPropType,
    registrationConfirmIncomes: checkboxPropType,
    registrationConfirmEData: checkboxPropType,
  }).isRequired,
  loginLink: PropTypes.string.isRequired,
  eligibilityLink: PropTypes.string.isRequired,
  termsOfServiceLink: PropTypes.string.isRequired,
  dataPrivacyLink: PropTypes.string.isRequired,
  waitingMomentActive: PropTypes.bool,
};

RegistrationPage.defaultProps = {
  waitingMomentActive: false,
};
