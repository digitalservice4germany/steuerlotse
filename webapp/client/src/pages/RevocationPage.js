import PropTypes from "prop-types";
import React, { useState } from "react";
import { Trans, useTranslation } from "react-i18next";
import FormFieldIdNr from "../components/FormFieldIdNr";
import FormFieldDate from "../components/FormFieldDate";
import FormHeader from "../components/FormHeader";
import FormRowCentered from "../components/FormRowCentered";
import StepForm from "../components/StepForm";
import StepHeaderButtons from "../components/StepHeaderButtons";
import { fieldPropType } from "../lib/propTypes";

export default function RevocationPage({
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
      <StepForm
        {...form}
        loadingFromOutside={waitingMomentActive}
        sendDisableCall={sendDisableCall}
        waitingMessages={{
          firstMessage: t("waitingMoment.revocation.firstMessage"),
          secondMessage: t("waitingMoment.revocation.secondMessage"),
        }}
      >
        <FormRowCentered>
          <FormFieldIdNr
            disable={isDisable}
            autofocus
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
        <FormRowCentered>
          <FormFieldDate
            disable={isDisable}
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
      </StepForm>
    </>
  );
}

RevocationPage.propTypes = {
  stepHeader: PropTypes.exact({
    title: PropTypes.string,
    intro: PropTypes.string,
  }).isRequired,
  form: PropTypes.exact({
    action: PropTypes.string,
    csrfToken: PropTypes.string,
    showOverviewButton: PropTypes.bool,
  }).isRequired,
  fields: PropTypes.exact({
    idnr: fieldPropType,
    dob: fieldPropType,
  }).isRequired,
  waitingMomentActive: PropTypes.bool,
};

RevocationPage.defaultProps = {
  waitingMomentActive: false,
};
