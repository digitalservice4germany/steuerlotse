import PropTypes from "prop-types";
import React from "react";
import { useTranslation } from "react-i18next";
import FormHeader from "../components/FormHeader";
import StepHeaderButtons from "../components/StepHeaderButtons";
import StepForm from "../components/StepForm";

export default function LogoutPage({ form }) {
  const { t } = useTranslation();
  const stepHeader = {
    title: t("form.logout.title"),
    intro: t("form.logout.intro"),
  };
  return (
    <>
      <StepHeaderButtons />
      <FormHeader {...stepHeader} />
      <StepForm {...form} nextButtonLabel={t("form.logout.button")} />
    </>
  );
}

LogoutPage.propTypes = {
  form: PropTypes.exact({
    action: PropTypes.string,
    csrfToken: PropTypes.string,
    showOverviewButton: PropTypes.bool,
    nextButtonLabel: PropTypes.string,
  }).isRequired,
};
