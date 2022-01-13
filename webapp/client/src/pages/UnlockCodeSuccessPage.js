import PropTypes from "prop-types";
import React from "react";
import { Trans, useTranslation } from "react-i18next";
import StepHeaderButtons from "../components/StepHeaderButtons";
import FormSuccessHeader from "../components/FormSuccessHeader";
import DownloadLink from "../components/DownloadLink";

export default function UnlockCodeSuccessPage({
  stepHeader,
  prevUrl,
  downloadUrl,
  steuerErklaerungsLink,
  vorbereitungshilfeLink,
}) {
  const { t } = useTranslation();

  return (
    <>
      <StepHeaderButtons url={prevUrl} />
      <FormSuccessHeader {...stepHeader} />
      <h2 className="mt-5">{t("register.success.next-steps.heading")}</h2>
      <ol>
        <li>
          <Trans
            t={t}
            i18nKey="register.success.next-steps.step-1"
            components={{
              bold: <b />,
            }}
          />
        </li>
        <li>
          <Trans
            t={t}
            i18nKey="register.success.next-steps.step-2"
            components={{
              // The anchors get content in the translation file
              // eslint-disable-next-line jsx-a11y/anchor-has-content
              vorbereitungshilfeLink: <a href={vorbereitungshilfeLink} />,
            }}
          />
        </li>
        <li>{t("register.success.next-steps.step-3")}</li>
        <li>
          <Trans
            t={t}
            i18nKey="register.success.next-steps.step-4"
            components={{
              // The anchors get content in the translation file
              // eslint-disable-next-line jsx-a11y/anchor-has-content
              steuerErklaerungsLink: <a href={steuerErklaerungsLink} />,
            }}
          />
        </li>
      </ol>

      <h2 className="mt-5">{t("register.success.letter.heading")}</h2>
      <p>{t("register.success.letter.intro")}</p>
      <img
        className="w-50"
        src="/images/elster_letter_example.png"
        alt="elster_letter"
      />

      <h2 className="mt-5">{t("register.success.preparation.heading")}</h2>
      <p>{t("register.success.preparation.intro")}</p>
      <DownloadLink
        url={downloadUrl}
        text={t("register.success.preparation.button")}
      />
    </>
  );
}

UnlockCodeSuccessPage.propTypes = {
  stepHeader: PropTypes.exact({
    title: PropTypes.string,
    intro: PropTypes.string,
  }).isRequired,
  prevUrl: PropTypes.string.isRequired,
  downloadUrl: PropTypes.string.isRequired,
  steuerErklaerungsLink: PropTypes.string.isRequired,
  vorbereitungshilfeLink: PropTypes.string.isRequired,
};
