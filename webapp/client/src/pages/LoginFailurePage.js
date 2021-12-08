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

export default function LoginFailurePage({
  stepHeader,
  prevUrl,
  registrationLink,
  revocationLink,
}) {
  const { t } = useTranslation();
  return (
    <>
      <StepHeaderButtons url={prevUrl} />
      <FormFailureHeader {...stepHeader} />
      <FailureReasonsHeadline className="unlock-code-failure-reasons-headline">
        {t("unlockCodeActivation.failure.causes.title")}
      </FailureReasonsHeadline>
      <ol>
        <li>{t("unlockCodeActivation.failure.causes.reasons1")}</li>
        <li>
          <Trans
            t={t}
            i18nKey="unlockCodeActivation.failure.causes.reasons2"
            components={{
              // The anchors get content in the translation file
              // eslint-disable-next-line jsx-a11y/anchor-has-content
              registrationLink: <a href={registrationLink} />,
            }}
          />
        </li>
        <li>
          <Trans
            t={t}
            i18nKey="unlockCodeActivation.failure.causes.reasons3"
            components={{
              // eslint-disable-next-line jsx-a11y/anchor-has-content
              registrationLink: <a href={registrationLink} />,
              // eslint-disable-next-line jsx-a11y/anchor-has-content
              revocationLink: <a href={revocationLink} />,
            }}
          />
        </li>
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
