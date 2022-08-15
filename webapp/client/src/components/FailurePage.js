import styled from "styled-components";
import PropTypes from "prop-types";
import React from "react";
import { Trans, useTranslation } from "react-i18next";
import StepHeaderButtons from "./StepHeaderButtons";
import FormFailureHeader from "./FormFailureHeader";

const FailureReasonsHeadline = styled.h2`
  &.unlock-code-failure-reasons-headline {
    margin-top: var(--spacing-09);
    margin-bottom: var(--spacing-03);
  }
`;

export default function FailurePage({ useCase, prevUrl }) {
  const { t } = useTranslation();
  const stepHeader = {
    title: t(`${useCase}.failure.title`),
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
        {t(`${useCase}.failure.causes.title`)}
      </FailureReasonsHeadline>
      <ol>
        {Object.values(
          t(`${useCase}.failure.causes.reasons`, { returnObjects: true })
        ).map((reason) => (
          <li>{trans(reason)}</li>
        ))}
      </ol>
    </>
  );
}

FailurePage.propTypes = {
  useCase: PropTypes.string.isRequired,
  prevUrl: PropTypes.string.isRequired,
};
