import PropTypes from "prop-types";
import React from "react";
import { Trans, useTranslation } from "react-i18next";
import FormHeaderParagraphs from "../components/FormHeaderParagraphs";
import StepHeaderButtons from "../components/StepHeaderButtons";
import StepNavButtons from "../components/StepNavButtons";

export default function NoPauschbetragPage({ stepHeader, prevUrl, nextUrl }) {
  const { t } = useTranslation();

  return (
    <>
      <StepHeaderButtons url={prevUrl} />
      <FormHeaderParagraphs
        title={stepHeader.title}
        intros={[
          t("lotse.noPauschbetrag.intro.p1"),
          <Trans
            t={t}
            i18nKey="lotse.noPauschbetrag.intro.p2"
            components={{
              bold: <b />,
            }}
          />,
        ]}
      />
      <StepNavButtons isForm={false} nextUrl={nextUrl} />
    </>
  );
}

NoPauschbetragPage.propTypes = {
  stepHeader: PropTypes.shape({
    title: PropTypes.string,
  }).isRequired,
  prevUrl: PropTypes.string.isRequired,
  nextUrl: PropTypes.string.isRequired,
};
