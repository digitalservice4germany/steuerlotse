import PropTypes from "prop-types";
import React from "react";
import { useTranslation, Trans } from "react-i18next";
import styled from "styled-components";
import StepHeaderButtons from "../components/StepHeaderButtons";
import FormFailureHeader from "../components/FormFailureHeader";
import retirementDates from "../lib/retirementDate";

const FailureReasonsHeadline = styled.h2`
  &.unlock-code-failure-reasons-headline {
    margin-top: var(--spacing-09);
    margin-bottom: var(--spacing-03);
  }
`;
export default function RevocationFailurePage({ prevUrl }) {
  const { t } = useTranslation();
  const stepHeader = {
    title: t("revocation.failure.header.title"),
  };

  function trans(key) {
    return (
      <Trans
        t={t}
        i18nKey={key}
        components={{
          registrationLink: (
            // eslint-disable-next-line jsx-a11y/anchor-has-content
            <a href="/unlock_code_request/step/data_input?link_overview=False" />
          ),
        }}
        values={{
          dateTwo: retirementDates.dateTwo,
          dateOne: retirementDates.dateOne,
        }}
      />
    );
  }

  return (
    <>
      <StepHeaderButtons url={prevUrl} />
      <FormFailureHeader {...stepHeader} />
      <FailureReasonsHeadline className="unlock-code-failure-reasons-headline">
        {t("revocation.failure.header.reason.title")}
      </FailureReasonsHeadline>
      <ol>
        <li>{trans("revocation.failure.header.reason.one")}</li>
        <li>{trans("revocation.failure.header.reason.two")}</li>
      </ol>
    </>
  );
}

RevocationFailurePage.propTypes = {
  prevUrl: PropTypes.string.isRequired,
};
