import PropTypes from "prop-types";
import React from "react";
import { Trans, useTranslation } from "react-i18next";
import styled from "styled-components";
import FormFailureHeader from "../components/FormFailureHeader";
import StepHeaderButtons from "../components/StepHeaderButtons";

const FailureReasonsHeadline = styled.h2`
  &.unlock-code-failure-reasons-headline {
    margin-top: var(--spacing-09);
    margin-bottom: var(--spacing-03);
  }
`;

export default function LoginFailurePage({ stepHeader, prevUrl }) {
  const { t } = useTranslation();

  function trans(key) {
    return (
      <Trans
        t={t}
        i18nKey={key}
        components={{
          eligibilityLink: (
            // eslint-disable-next-line jsx-a11y/anchor-has-content
            <a href="/unlock_code_request/step/data_input" />
          ),
          einfachElster: (
            // eslint-disable-next-line jsx-a11y/anchor-has-content
            <a href="https://einfach.elster.de/erklaerung/ui/" />
          ),
        }}
      />
    );
  }

  return (
    <>
      <StepHeaderButtons url={prevUrl} />
      <FormFailureHeader {...stepHeader} />
      <FailureReasonsHeadline className="unlock-code-failure-reasons-headline">
        {t("unlockCodeActivation.failure.causes.title")}
      </FailureReasonsHeadline>
      <ol>
        <li>{trans("unlockCodeActivation.failure.causes.reasons1")}</li>
        <li>{trans("unlockCodeActivation.failure.causes.reasons2")}</li>
        <li>{trans("unlockCodeActivation.failure.causes.reasons3")}</li>
      </ol>
    </>
  );
}

LoginFailurePage.propTypes = {
  stepHeader: PropTypes.exact({
    title: PropTypes.string,
    intro: PropTypes.string,
  }).isRequired,
  prevUrl: PropTypes.string.isRequired,
  registrationLink: PropTypes.string.isRequired,
  revocationLink: PropTypes.string.isRequired,
};
