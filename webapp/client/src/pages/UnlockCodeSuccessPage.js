import PropTypes from "prop-types";
import React from "react";
import { useTranslation } from "react-i18next";
import styled from "styled-components";
import StepHeaderButtons from "../components/StepHeaderButtons";
import FormSuccessHeader from "../components/FormSuccessHeader";
import SuccessStepsInfoBox from "../components/successStepsInfoBox";
import OneIcon from "../assets/icons/Icon-1.svg";
import TwoIcon from "../assets/icons/Icon-2.svg";
import ThreeIcon from "../assets/icons/Icon-3.svg";

export default function UnlockCodeSuccessPage({
  prevUrl,
  vorbereitungsHilfeLink,
  plausibleDomain,
}) {
  const { t } = useTranslation();
  const stepHeader = {
    title: t("register.success.next-steps.header.title"),
  };

  const Header = styled.h1`
    font-size: var(--text-3xl);

    @media (max-width: 768px) {
      font-size: var(--text-2xl);
    }
  `;

  const anchorInfo = {
    text: t("register.success.next-steps.howItContinues.step-1.buttonText"),
    url: vorbereitungsHilfeLink,
  };

  const image = {
    src: "../../images/Img_Brief_500.jpg",
    alt: "Beispielbild der letzten Briefseite mit Freischaltcode",
    srcSet:
      "../../images/Img_Brief_500.jpg 1155w ,  ../../images/Img_Brief_1024.jpg 2048w",
  };

  const plausibleGoal = "Vorbereitungshilfe";
  const plausiblePropsButton = {
    method: "CTA Vorbereitungshilfe herunterladen",
  };
  return (
    <>
      <StepHeaderButtons url={prevUrl} />
      <FormSuccessHeader {...stepHeader} />
      <Header className="mt-5">
        {t("register.success.next-steps.howItContinues.heading")}
      </Header>
      <SuccessStepsInfoBox
        header={t("register.success.next-steps.howItContinues.step-1.heading")}
        text={t("register.success.next-steps.howItContinues.step-1.text")}
        anchor={anchorInfo}
        plausibleDomain={plausibleDomain}
        icon={OneIcon}
        plausibleGoal={plausibleGoal}
        plausiblePropsButton={plausiblePropsButton}
      />
      <SuccessStepsInfoBox
        header={t("register.success.next-steps.howItContinues.step-2.heading")}
        text={t("register.success.next-steps.howItContinues.step-2.text")}
        image={image}
        icon={TwoIcon}
      />
      <SuccessStepsInfoBox
        header={t("register.success.next-steps.howItContinues.step-3.heading")}
        text={t("register.success.next-steps.howItContinues.step-3.text")}
        icon={ThreeIcon}
      />
    </>
  );
}

UnlockCodeSuccessPage.propTypes = {
  prevUrl: PropTypes.string.isRequired,
  vorbereitungsHilfeLink: PropTypes.string.isRequired,
  plausibleDomain: PropTypes.string,
};

UnlockCodeSuccessPage.defaultProps = {
  plausibleDomain: null,
};
