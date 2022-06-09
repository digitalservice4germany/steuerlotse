import React from "react";
import { useTranslation } from "react-i18next";
import FormSuccessHeader from "../components/FormSuccessHeader";

export default function NewsletterSuccessPage() {
  const { t } = useTranslation();
  const stepHeader = {
    title: t("newsletter.successPage.title"),
  };

  return <FormSuccessHeader {...stepHeader} />;
}
