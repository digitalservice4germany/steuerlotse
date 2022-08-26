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
        howItWorksLink: (
          // eslint-disable-next-line jsx-a11y/anchor-has-content
          <a href="/sofunktionierts" />
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

const accordionRetirementPage = [
  {
    title: t("retirementPage.accordion.file2021TaxReturn.title"),
    detail: trans("retirementPage.accordion.file2021TaxReturn.detail"),
  },
  {
    title: t("retirementPage.accordion.taxReturnDeadline.title"),
    detail: (
      <div>
        <p>{trans("retirementPage.accordion.taxReturnDeadline.detailOne")}</p>
        <p>{trans("retirementPage.accordion.taxReturnDeadline.detailTwo")}</p>
      </div>
    ),
  },
  {
    title: t("retirementPage.accordion.file2022Registration.title"),
    detail: trans("retirementPage.accordion.file2022Registration.detail"),
  },
  {
    title: t("retirementPage.accordion.alternatives.title"),
    detail: (
      <div>
        <p>{trans("retirementPage.accordion.alternatives.detailOne")}</p>
        <p>{trans("retirementPage.accordion.alternatives.detailTwo")}</p>
      </div>
    ),
  },
  {
    title: t("retirementPage.accordion.whatHappensToData.title"),
    detail: (
      <div>
        <p>{trans("retirementPage.accordion.whatHappensToData.detailOne")}</p>
        <p>{t("retirementPage.accordion.whatHappensToData.detailTwo")}</p>
        <p>{t("retirementPage.accordion.whatHappensToData.detailThre")}</p>
        <p>{trans("retirementPage.accordion.whatHappensToData.detailFour")}</p>
      </div>
    ),
  },
];

export default accordionRetirementPage;
