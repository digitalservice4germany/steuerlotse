import PropTypes from "prop-types";
import React from "react";
import FormFieldIdNr from "../components/FormFieldIdNr";
import FormFieldUnlockCode from "../components/FormFieldUnlockCode";
import FormHeader from "../components/FormHeader";
import FormRowCentered from "../components/FormRowCentered";
import StepForm from "../components/StepForm";
import StepHeaderButtons from "../components/StepHeaderButtons";

export default function LoginPage({ backLink, stepHeader, form, fields }) {
  return (
    <>
      <StepHeaderButtons {...backLink} />
      <FormHeader {...stepHeader} />
      <StepForm {...form}>
        <FormRowCentered>
          <FormFieldIdNr
            autofocus
            required
            fieldName="idnr"
            // TODO: is the fieldId ever different from the fieldName?
            fieldId="idnr"
            values={fields.idnr.value}
            label={{
              // TODO: intl
              // text: 'unlock-code-activation.idnr',
              text: "Steuer-Identifikationsnummer",
            }}
            details={{
              // TODO: intl
              // title: 'unlock-code-request.idnr.help-title',
              title: "Wo finde ich diese Nummer?",
              // text: 'unlock-code-request.idnr.help-text'
              text: "Die 11-stellige Nummer haben Sie mit einem Brief vom Bundeszentralamt für Steuern erhalten. Die Nummer steht oben rechts groß auf dem Brief. Alternativ finden Sie diese Nummer auch auf Ihrem letzten Steuerbescheid.",
            }}
            errors={fields.idnr.errors}
          />
        </FormRowCentered>
        <FormRowCentered>
          <FormFieldUnlockCode
            required
            fieldName="unlock_code"
            fieldId="unlock_code" // field.id
            values={fields.unlockCode.value}
            label={{
              // TODO: intl
              // text: "unlock-code-activation.unlock-code",
              text: "Freischaltcode",
            }}
            details={{
              // TODO: intl
              // title: "unlock-code-request.unlock-code.help-title",
              title: "Wo finde ich diese Nummer?",
              // text: "unlock-code-request.unlock-code.help-text",
              text: "Wenn Sie sich beim Steuerlotsen erfolgreich registriert haben, bekommen Sie von Ihrer Finanzverwaltung einen Brief mit Ihrem persönlichen Freischaltcode zugeschickt. Den Freischaltcode finden Sie auf der letzten Seite des Briefes.",
            }}
            errors={fields.unlockCode.errors}
          />
        </FormRowCentered>
      </StepForm>
    </>
  );
}

const fieldPropType = PropTypes.exact({
  // field._value()
  value: PropTypes.any,
  // field.errors
  errors: PropTypes.arrayOf(PropTypes.string),
});

LoginPage.propTypes = {
  backLink: PropTypes.exact(StepHeaderButtons.propTypes),
  stepHeader: PropTypes.exact({
    // TODO: define these here, not in Python
    // render_info.step_title
    title: PropTypes.string,
    // render_info.step_intro
    intro: PropTypes.string,
  }).isRequired,
  form: PropTypes.exact({
    // render_info.submit_url
    action: PropTypes.string, // TODO: does this change? if not, define here, not in Python
    // csrf_token()
    csrfToken: PropTypes.string,
    // !!render_info.overview_url
    showOverviewButton: PropTypes.bool,
    // explanatory_button_text
    explanatoryButtonText: PropTypes.string, // TODO: define here, not in Python
    // render_info.additional_info.next_button_label
    nextButtonLabel: PropTypes.string, // TODO: define here, not in Python
  }).isRequired,
  fields: PropTypes.exact({
    idnr: fieldPropType,
    unlockCode: fieldPropType,
  }).isRequired,
};

LoginPage.defaultProps = {
  backLink: undefined,
};
