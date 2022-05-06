import PropTypes from "prop-types";
import React from "react";
import { useTranslation } from "react-i18next";
import StepHeaderButtons from "../components/StepHeaderButtons";
import FormSuccessHeader from "../components/FormSuccessHeader";
import SuccessStepsInfoBox from "../components/successStepsInfoBox";
import OneIcon from "../assets/icons/Icon-1.svg";
import TwoIcon from "../assets/icons/Icon-2.svg";
import ThreeIcon from "../assets/icons/Icon-3.svg";
// import addPlausibleGoal from "../lib/helpers";

export default function UnlockCodeSuccessPage({
  prevUrl,
  vorbereitungsHilfeLink,
  plausibleDomain,
}) {
  const { t } = useTranslation();
  const stepHeader = {
    title: t("register.success.next-steps.header.title"),
  };

  const anchorInfo = {
    text: t("register.success.next-steps.howItContinues.step-1.buttonText"),
    url: vorbereitungsHilfeLink,
  };

  const image = {
    src: "../../images/Img_Brief_1024.jpg",
  };

  return (
    <>
      <StepHeaderButtons url={prevUrl} />
      <FormSuccessHeader {...stepHeader} />
      <h2 className="mt-5">
        {t("register.success.next-steps.howItContinues.heading")}
      </h2>
      <SuccessStepsInfoBox
        header={t("register.success.next-steps.howItContinues.step-1.heading")}
        text={t("register.success.next-steps.howItContinues.step-1.text")}
        anchor={anchorInfo}
        plausibleDomain={plausibleDomain}
        icon={OneIcon}
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
