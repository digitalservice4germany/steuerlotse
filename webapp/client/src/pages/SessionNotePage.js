import PropTypes from "prop-types";
import React from "react";
import { Trans, useTranslation } from "react-i18next";
import styled from "styled-components";
import FormHeader from "../components/FormHeader";
import StepForm from "../components/StepForm";
import StepHeaderButtons from "../components/StepHeaderButtons";
import listMarker from "../assets/icons/list_marker.svg";

const IntroList = styled.ul`
  margin-bottom: var(--spacing-06);

  &.form-list {
    list-style-image: url(${listMarker});
  }

  &.form-list li::before {
    vertical-align: text-top;
    height: 1px;
  }

  &.form-list li {
    margin-top: var(--spacing-02);
  }
`;

export default function SessionNotePage({ form, prevUrl }) {
  const { t } = useTranslation();
  const stepHeader = {
    title: t("lotse.sessionNote.title"),
  };
  const translationBold = function translationBold(key) {
    return <Trans t={t} i18nKey={key} components={{ bold: <b /> }} />;
  };

  return (
    <>
      <StepHeaderButtons url={prevUrl} />
      <FormHeader {...stepHeader} />
      <IntroList className="form-list">
        <li>{t("lotse.sessionNote.listItem1")}</li>
        <li>{translationBold("lotse.sessionNote.listItem2")}</li>
        <li>{translationBold("lotse.sessionNote.listItem3")}</li>
        <li>{t("lotse.sessionNote.listItem4")}</li>
      </IntroList>
      <StepForm {...form} />
    </>
  );
}

SessionNotePage.propTypes = {
  form: PropTypes.exact({
    action: PropTypes.string,
    csrfToken: PropTypes.string,
    showOverviewButton: PropTypes.bool,
    nextButtonLabel: PropTypes.string,
  }).isRequired,
  prevUrl: PropTypes.string.isRequired,
};
