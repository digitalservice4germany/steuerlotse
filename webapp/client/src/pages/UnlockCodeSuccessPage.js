import PropTypes from "prop-types";
import React from "react";
import { Trans, useTranslation } from "react-i18next";
import StepHeaderButtons from "../components/StepHeaderButtons";
import FormSuccessHeader from "../components/FormSuccessHeader";
import AnchorButton from "../components/AnchorButton";

export default function UnlockCodeSuccessPage({
  prevUrl,
  steuerErklaerungLink,
  vorbereitungsHilfeLink,
}) {
  const { t } = useTranslation();
  const stepHeader = {
    title: t("register.success.next-steps.header.title"),
    intro: t("register.success.next-steps.header.intro"),
  };

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
              vorbereitungsHilfeLink: <a href={vorbereitungsHilfeLink} />,
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
              steuerErklaerungLink: <a href={steuerErklaerungLink} />,
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
      <AnchorButton
        url={vorbereitungsHilfeLink}
        text={t("register.success.preparation.anchor")}
        isDownloadLink={true}
      />
    </>
  );
}

UnlockCodeSuccessPage.propTypes = {
  prevUrl: PropTypes.string.isRequired,
  steuerErklaerungLink: PropTypes.string.isRequired,
  vorbereitungsHilfeLink: PropTypes.string.isRequired,
};
