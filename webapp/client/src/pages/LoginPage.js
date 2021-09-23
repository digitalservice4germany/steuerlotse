import PropTypes from "prop-types";
import React from "react";
import { useTranslation } from "react-i18next";
import FormFieldIdNr from "../components/FormFieldIdNr";
import FormFieldUnlockCode from "../components/FormFieldUnlockCode";
import FormHeader from "../components/FormHeader";
import FormRowCentered from "../components/FormRowCentered";
import StepForm from "../components/StepForm";
import StepHeaderButtons from "../components/StepHeaderButtons";

export default function LoginPage({ stepHeader, form, fields }) {
  const { t } = useTranslation();

  return (
    <>
      <StepHeaderButtons />
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
              text: t("unlockCodeActivation.idnr.labelText"),
            }}
            details={{
              title: t("unlockCodeActivation.idnr.help.title"),
              text: t("unlockCodeActivation.idnr.help.text"),
            }}
            errors={fields.idnr.errors}
          />
        </FormRowCentered>
        <FormRowCentered>
          <FormFieldUnlockCode
            required
            fieldName="unlock_code"
            fieldId="unlock_code"
            values={fields.unlockCode.value}
            label={{
              text: t("unlockCodeActivation.unlockCode.labelText"),
            }}
            details={{
              title: t("unlockCodeActivation.unlockCode.help.title"),
              text: t("unlockCodeActivation.unlockCode.help.text"),
            }}
            errors={fields.unlockCode.errors}
          />
        </FormRowCentered>
      </StepForm>
    </>
  );
}

const fieldPropType = PropTypes.exact({
  value: PropTypes.any,
  errors: PropTypes.arrayOf(PropTypes.string),
});

LoginPage.propTypes = {
  stepHeader: PropTypes.exact({
    // TODO: define these here, not in Python
    title: PropTypes.string,
    intro: PropTypes.string,
  }).isRequired,
  form: PropTypes.exact({
    action: PropTypes.string, // TODO: does this change? if not, define here, not in Python
    csrfToken: PropTypes.string,
    showOverviewButton: PropTypes.bool,
  }).isRequired,
  fields: PropTypes.exact({
    idnr: fieldPropType,
    unlockCode: fieldPropType,
  }).isRequired,
};
