import PropTypes from "prop-types";
import React, { useState } from "react";
import { Trans, useTranslation } from "react-i18next";
import FormFieldIdNr from "../components/FormFieldIdNr";
import FormFieldUnlockCode from "../components/FormFieldUnlockCode";
import FormHeader from "../components/FormHeader";
import FormRowCentered from "../components/FormRowCentered";
import StepFormAsync from "../components/StepFormAsync";
import StepHeaderButtons from "../components/StepHeaderButtons";
import { fieldPropType } from "../lib/propTypes";

export default function LoginPage({
  stepHeader,
  form,
  fields,
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
      <FormHeader {...stepHeader} />
      <StepFormAsync
        {...form}
        loadingFromOutside={waitingMomentActive}
        sendDisableCall={sendDisableCall}
        waitingMessages={{
          firstMessage: t("waitingMoment.login.firstMessage"),
          secondMessage: t("waitingMoment.login.secondMessage"),
        }}
      >
        <FormRowCentered>
          <FormFieldIdNr
            disable={isDisable}
            autofocus
            required
            fieldName="idnr"
            // TODO: is the fieldId ever different from the fieldName?
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
        <FormRowCentered>
          <FormFieldUnlockCode
            disable={isDisable}
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
      </StepFormAsync>
    </>
  );
}

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
    nextButtonLabel: PropTypes.string, // TODO: define here, not in Python
  }).isRequired,
  fields: PropTypes.exact({
    idnr: fieldPropType,
    unlockCode: fieldPropType,
  }).isRequired,
  waitingMomentActive: PropTypes.bool,
};

LoginPage.defaultProps = {
  waitingMomentActive: false,
};
