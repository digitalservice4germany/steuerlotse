import PropTypes from "prop-types";
import React from "react";
import { Trans, useTranslation } from "react-i18next";
import styled from "styled-components";
import Details from "../components/Details";
import FormFieldConsentBox from "../components/FormFieldConsentBox";
import FormFieldDate from "../components/FormFieldDate";
import FormFieldIdNr from "../components/FormFieldIdNr";
import FormHeader from "../components/FormHeader";
import FormRowCentered from "../components/FormRowCentered";
import StepForm from "../components/StepForm";
import StepHeaderButtons from "../components/StepHeaderButtons";
import { checkboxPropType, fieldPropType } from "../lib/propTypes";

const SubHeading = styled.h2`
  &.form-sub-heading-smaller {
    font-size: var(--text-medium);
    margin-top: var(--spacing-09);
    margin-bottom: var(--spacing-03);
  }
`;

export default function RegistrationPage({
  stepHeader,
  form,
  fields,
  loginLink,
  eligibilityLink,
  termsOfServiceLink,
  dataPrivacyLink,
}) {
  const { t } = useTranslation();

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
      <StepForm
        {...form}
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
            autofocus
            required
            fieldName="dob"
            fieldId="dob"
            values={fields.dob.value}
            label={{
              text: t("unlockCodeRequest.dob.labelText"),
            }}
            errors={fields.dob.errors}
          />
        </FormRowCentered>
        <FormRowCentered>
          <FormFieldIdNr
            required
            fieldName="idnr"
            fieldId="idnr"
            values={fields.idnr.value}
            label={{
              text: t("unlockCodeActivation.idnr.labelText"),
            }}
            details={{
              title: t("unlockCodeActivation.idnr.help.title"),
              text: t("unlockCodeActivation.idnr.help.text"),
            }}
            errors={fields.idnr.errors}
          />
        </FormRowCentered>
        <SubHeading className="form-sub-heading-smaller">
          {t("unlockCodeRequest.dataPrivacyAndAgb.title")}
        </SubHeading>
        <FormFieldConsentBox
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
          errors={fields.registrationConfirmDataPrivacy.errors}
        />
        <FormFieldConsentBox
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
                termsOfServiceLink: <a href={termsOfServiceLink} />,
              }}
            />
          }
          errors={fields.registrationConfirmTermsOfService.errors}
        />
        <FormFieldConsentBox
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
                eligibilityLink: <a href={eligibilityLink} />,
              }}
            />
          }
          errors={fields.registrationConfirmIncomes.errors}
        />
        <SubHeading className="form-sub-heading-smaller">
          {t("unlockCodeRequest.eData.title")}
        </SubHeading>
        <Details
          title={t("unlockCodeRequest.eData.helpTitle")}
          detailsId="registration_confirm_e_data"
        >
          {{
            paragraphs: [
              <Trans
                t={t}
                i18nKey="unlockCodeRequest.eData.helpText"
                components={{ bold: <strong /> }}
              />,
            ],
          }}
        </Details>
        <FormFieldConsentBox
          required
          fieldName="registration_confirm_e_data"
          fieldId="registration_confirm_e_data"
          checked={fields.registrationConfirmEData.checked}
          labelText={t(
            "unlockCodeRequest.fieldRegistrationConfirmEData.labelText"
          )}
          errors={fields.registrationConfirmEData.errors}
        />
      </StepForm>
    </>
  );
}

RegistrationPage.propTypes = {
  stepHeader: PropTypes.exact({
    // TODO: define these here, not in Python
    title: PropTypes.string,
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
};
