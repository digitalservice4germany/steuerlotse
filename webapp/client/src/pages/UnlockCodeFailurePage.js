import PropTypes from "prop-types";
import React from "react";
import { useTranslation, Trans } from "react-i18next";
import styled from "styled-components";
import FormFailureHeader from "../components/FormFailureHeader";
import StepHeaderButtons from "../components/StepHeaderButtons";

const FailureReasonsHeadline = styled.h2`
  &.unlock-code-failure-reasons-headline {
    margin-top: var(--spacing-09);
    margin-bottom: var(--spacing-03);
  }
`;
export default function UnlockCodeFailurePage({ prevUrl }) {
  const { t } = useTranslation();
  const stepHeader = {
    title: t("register.failure.header.title"),
  };

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
          revocationLink: (
            // eslint-disable-next-line jsx-a11y/anchor-has-content
            <a href="/unlock_code_revocation/step/data_input" />
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
        {t("register.failure.reasons.title")}
      </FailureReasonsHeadline>
      <ol>
        <li>{trans("register.failure.reasons.one")}</li>
        <li>{trans("register.failure.reasons.two")}</li>
        <li>{trans("register.failure.reasons.three")}</li>
      </ol>
    </>
  );
}

UnlockCodeFailurePage.propTypes = {
  prevUrl: PropTypes.string.isRequired,
};
