import PropTypes from "prop-types";
import React from "react";
import { Trans, useTranslation } from "react-i18next";
import styled from "styled-components";
import StepHeaderButtons from "../components/StepHeaderButtons";
import FormSuccessHeader from "../components/FormSuccessHeader";
import SuccessStepsInfoBox from "../components/SuccessStepsInfoBox";
import OneIcon from "../assets/icons/Icon-1.svg";
import TwoIcon from "../assets/icons/Icon-2.svg";
import ThreeIcon from "../assets/icons/Icon-3.svg";
import NewsletterRegisterBox from "../components/NewsletterRegisterBox";
import { toggleManually } from "../lib/helpers";
import retirementDates from "../lib/retirementDate";

export default function UnlockCodeSuccessPage({
  prevUrl,
  vorbereitungsHilfeLink,
  plausibleDomain,
  dataPrivacyLink,
  csrfToken,
}) {
  const { t } = useTranslation();
  const stepHeader = {
    title: t("register.success.next-steps.header.title"),
  };

  const Header = styled.h2`
    font-size: var(--text-3xl);

    @media (max-width: 768px) {
      font-size: var(--text-2xl);
    }

    @media (max-width: 568px) {
      font-size: var(--text-xla);
    }
  `;

  const anchorInfo = {
    text: t("register.success.next-steps.howItContinues.step-1.buttonText"),
    url: vorbereitungsHilfeLink,
  };

  const image = {
    src: "../../images/Img_Brief_500.png",
    alt: "Beispielbild der letzten Briefseite mit Freischaltcode",
    srcSetLargeScreen: "../../images/Img_Brief_1024.png",
    srcSetSmallerScreen: "../../images/Img_Brief_500.png",
  };

  const IconOne = {
    iconSrc: OneIcon,
    altText: t("register.icons.iconOne.altText"),
  };
  const IconTwo = {
    iconSrc: TwoIcon,
    altText: t("register.icons.iconTwo.altText"),
  };
  const IconThree = {
    iconSrc: ThreeIcon,
    altText: t("register.icons.iconThree.altText"),
  };

  const plausibleGoal = "Vorbereitungshilfe";
  const emailPlausibleGoal = "E-Mails abonnieren";
  const plausiblePropsButton = {
    method: "CTA Vorbereitungshilfe herunterladen",
  };

  function trans(key) {
    return (
      <Trans
        t={t}
        i18nKey={key}
        components={{
          vorbereitenLink: (
            // eslint-disable-next-line jsx-a11y/anchor-has-content
            <a href="/vorbereiten" rel="noreferrer" target="_blank" />
          ),
          validity: (
            // eslint-disable-next-line jsx-a11y/anchor-has-content, jsx-a11y/anchor-is-valid
            <a
              href="#"
              onClick={(event) =>
                toggleManually(event, true, "letterActivationCodeSection", "2")
              }
            />
          ),
        }}
        values={{
          dateTwo: retirementDates.dateTwo,
          dateOne: retirementDates.dateOne,
        }}
      />
    );
  }

  const text = (
    <>
      <p>{t("register.success.next-steps.howItContinues.step-3.textOne")}</p>
      <p>
        {trans("register.success.next-steps.howItContinues.step-3.textTwo")}
      </p>
      <p>
        {trans("register.success.next-steps.howItContinues.step-3.textThree")}
      </p>
    </>
  );

  const imageDescription = (
    <>
      <p>
        {t(
          "register.success.next-steps.howItContinues.step-2.imageDescriptionOne"
        )}
      </p>
      <p>
        {t(
          "register.success.next-steps.howItContinues.step-2.imageDescriptionTwo"
        )}
      </p>
    </>
  );

  return (
    <>
      <StepHeaderButtons url={prevUrl} />
      <FormSuccessHeader {...stepHeader} />
      <Header className="mt-5">
        {t("register.success.next-steps.howItContinues.heading")}
      </Header>
      <SuccessStepsInfoBox
        header={t("register.success.next-steps.howItContinues.step-1.heading")}
        text={trans("register.success.next-steps.howItContinues.step-1.text")}
        anchor={anchorInfo}
        plausibleDomain={plausibleDomain}
        icon={IconOne}
        plausibleGoal={plausibleGoal}
        plausiblePropsButton={plausiblePropsButton}
      />
      <SuccessStepsInfoBox
        header={t("register.success.next-steps.howItContinues.step-2.heading")}
        text={t("register.success.next-steps.howItContinues.step-2.text")}
        image={image}
        icon={IconTwo}
        imageDescription={imageDescription}
      />
      <SuccessStepsInfoBox
        header={t("register.success.next-steps.howItContinues.step-3.heading")}
        text={text}
        icon={IconThree}
        textOnly
      />
      <NewsletterRegisterBox
        dataPrivacyLink={dataPrivacyLink}
        csrfToken={csrfToken}
        plausibleDomain={plausibleDomain}
        plausibleGoal={emailPlausibleGoal}
      />
    </>
  );
}

UnlockCodeSuccessPage.propTypes = {
  prevUrl: PropTypes.string.isRequired,
  vorbereitungsHilfeLink: PropTypes.string.isRequired,
  plausibleDomain: PropTypes.string,
  dataPrivacyLink: PropTypes.string.isRequired,
  csrfToken: PropTypes.string.isRequired,
};

UnlockCodeSuccessPage.defaultProps = {
  plausibleDomain: null,
};
