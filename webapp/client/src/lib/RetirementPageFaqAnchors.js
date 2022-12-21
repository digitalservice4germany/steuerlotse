import { t } from "i18next";
import { Trans } from "react-i18next";
import React from "react";
import retirementDates from "./retirementDate";

function trans(key) {
  return (
    <Trans
      t={t}
      i18nKey={key}
      components={{
        // eslint-disable-next-line jsx-a11y/anchor-has-content
        downloadPreparationLink: <a href="/download_preparation" />,

        elsterLink: (
          // eslint-disable-next-line jsx-a11y/anchor-has-content
          <a href="https://www.elster.de/eportal/login/softpse" />
        ),
        einfachElsterLink: (
          // eslint-disable-next-line jsx-a11y/anchor-has-content
          <a href="https://einfach.elster.de/erklaerung/ui/" />
        ),
        simplifiedPaperFormLink: (
          // eslint-disable-next-line jsx-a11y/anchor-has-content
          <a href="https://www.bundesfinanzministerium.de/Content/DE/Standardartikel/Themen/Steuern/Steuerliche_Themengebiete/Altersvorsorge/2019-04-29-Laendervordruck-vereinfachte-veranlagung-rentner.html" />
        ),
        dataPrivacyLink: (
          // eslint-disable-next-line jsx-a11y/anchor-has-content
          <a href="/datenschutz" />
        ),
        validity: (
          // eslint-disable-next-line jsx-a11y/anchor-has-content
          <a href="/hilfebereich#letterActivationCodeSection-2" />
        ),
      }}
      values={{
        dateTwo: retirementDates.dateTwo,
        dateOne: retirementDates.dateOne,
      }}
    />
  );
}

const accordionRetirementPage = Object.keys(
  t("retirementPage.accordion.elements", { returnObjects: true })
).map((k) => {
  const values = t("retirementPage.accordion.elements", {
    returnObjects: true,
  })[k];
  if (typeof values.detail === "string") {
    return {
      title: values.title,
      detail: trans(`retirementPage.accordion.elements.${k}.detail`),
    };
  }
  return {
    title: values.title,
    detail: (
      <div>
        {values.detail.map((newk) => (
          <p>{trans(newk)}</p>
        ))}
      </div>
    ),
  };
});

export default accordionRetirementPage;
