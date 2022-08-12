import { t } from "i18next";
import { Trans } from "react-i18next";
import React from "react";
import DisabledLink from "../components/DisableLink";

function toggleManually(event, section, elementIndex) {
  event.preventDefault();
  window.location = `#${section}`;
  document.getElementById(`button-${section}-${elementIndex}`).click();
}

function trans(key) {
  return (
    <Trans
      t={t}
      i18nKey={key}
      components={{
        // eslint-disable-next-line jsx-a11y/anchor-has-content
        downloadPreparationLink: <a href="/download_preparation" />,

        eligibilityLink: (
          // eslint-disable-next-line jsx-a11y/anchor-has-content
          <DisabledLink href="/eligibility/step/tax_year?link_overview=False" />
        ),
        registrationLink: (
          // eslint-disable-next-line jsx-a11y/anchor-has-content
          <a href="/unlock_code_request/step/data_input?link_overview=False" />
        ),
        activationLink: (
          // eslint-disable-next-line jsx-a11y/anchor-has-content
          <a href="/unlock_code_activation/step/data_input?link_overview=False" />
        ),
        bundesfinanzministeriumLink: (
          // eslint-disable-next-line jsx-a11y/anchor-has-content
          <a href="https://www.bundesfinanzministerium.de/Web/DE/Home/home.html" />
        ),
        grundsteuererklärungLink: (
          // eslint-disable-next-line jsx-a11y/anchor-has-content
          <a href="https://www.grundsteuererklaerung-fuer-privateigentum.de/" />
        ),
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
        taxOfficeSearch: (
          // eslint-disable-next-line jsx-a11y/anchor-has-content
          <a href="https://www.bzst.de/DE/Service/Behoerdenwegweiser/Finanzamtsuche/GemFa/finanzamtsuche_node.html" />
        ),
        codeRevocationLink: (
          // eslint-disable-next-line jsx-a11y/anchor-has-content
          <a href="/unlock_code_revocation/step/data_input?link_overview=False" />
        ),
        federalTaxOffice: (
          // eslint-disable-next-line jsx-a11y/anchor-has-content
          <a href="https://www.bzst.de/SiteGlobals/Kontaktformulare/DE/Steuerliche_IDNr/Mitteilung_IdNr/mitteilung_IdNr_node.html" />
        ),
        validity: (
          // eslint-disable-next-line jsx-a11y/anchor-has-content
          <a
            href="/hilfebereich#letterActivationCodeSection-2"
            onClick={(event) =>
              toggleManually(event, "letterActivationCodeSection", "2")
            }
          />
        ),
      }}
    />
  );
}

const accordionCanIUseSection = [
  {
    title: t("helpAreaPage.accordionCanIUseSection.item1.title"),
    detail: (
      <div>
        <p>{t("helpAreaPage.accordionCanIUseSection.item1.detail.one")}</p>
        <p>{t("helpAreaPage.accordionCanIUseSection.item1.detail.two")}</p>
        <p>
          {trans("helpAreaPage.accordionCanIUseSection.item1.detail.three")}
        </p>
      </div>
    ),
  },
  {
    title: t("helpAreaPage.accordionCanIUseSection.item2.title"),
    detail: (
      <div>
        <p>{t("helpAreaPage.accordionCanIUseSection.item2.detail.one")}</p>
        <ul>
          <li>
            {trans(
              "helpAreaPage.accordionCanIUseSection.item2.detail.listItemOne"
            )}
          </li>
          <li>
            {trans(
              "helpAreaPage.accordionCanIUseSection.item2.detail.listItemTwo"
            )}
          </li>
          <li>
            {trans(
              "helpAreaPage.accordionCanIUseSection.item2.detail.listItemThree"
            )}
          </li>
        </ul>
      </div>
    ),
  },
  {
    title: t("helpAreaPage.accordionCanIUseSection.item3.title"),
    detail: trans("helpAreaPage.accordionCanIUseSection.item3.detail"),
  },
  {
    title: t("helpAreaPage.accordionCanIUseSection.item4.title"),
    detail: (
      <div>
        <p>{t("helpAreaPage.accordionCanIUseSection.item4.detail.one")}</p>
        <p>{t("helpAreaPage.accordionCanIUseSection.item4.detail.two")}</p>
        <ul>
          <li>
            {trans(
              "helpAreaPage.accordionCanIUseSection.item4.detail.listItemOne"
            )}
          </li>
          <li>
            {trans(
              "helpAreaPage.accordionCanIUseSection.item4.detail.listItemTwo"
            )}
          </li>
          <li>
            {trans(
              "helpAreaPage.accordionCanIUseSection.item4.detail.listItemThree"
            )}
          </li>
          <li>
            {trans(
              "helpAreaPage.accordionCanIUseSection.item4.detail.listItemFour"
            )}
          </li>
          <li>
            {trans(
              "helpAreaPage.accordionCanIUseSection.item4.detail.listItemFive"
            )}
          </li>
          <li>
            {trans(
              "helpAreaPage.accordionCanIUseSection.item4.detail.listItemSix"
            )}
          </li>
          <li>
            {trans(
              "helpAreaPage.accordionCanIUseSection.item4.detail.listItemSeven"
            )}
          </li>
          <li>
            {trans(
              "helpAreaPage.accordionCanIUseSection.item4.detail.listItemEight"
            )}
          </li>
          <li>
            {trans(
              "helpAreaPage.accordionCanIUseSection.item4.detail.listItemNine"
            )}
          </li>
        </ul>
      </div>
    ),
  },
  {
    title: t("helpAreaPage.accordionCanIUseSection.item5.title"),
    detail: (
      <div>
        <p>{trans("helpAreaPage.accordionCanIUseSection.item5.detail.one")}</p>
        <p>{trans("helpAreaPage.accordionCanIUseSection.item5.detail.two")}</p>
      </div>
    ),
  },
  {
    title: t("helpAreaPage.accordionCanIUseSection.item6.title"),
    detail: (
      <div>
        <p>{trans("helpAreaPage.accordionCanIUseSection.item6.detail.one")}</p>
        <p>{trans("helpAreaPage.accordionCanIUseSection.item6.detail.two")}</p>
      </div>
    ),
  },
  {
    title: t("helpAreaPage.accordionCanIUseSection.item7.title"),
    detail: trans("helpAreaPage.accordionCanIUseSection.item7.detail"),
  },
  {
    title: t("helpAreaPage.accordionCanIUseSection.item8.title"),
    detail: (
      <div>
        <p>{trans("helpAreaPage.accordionCanIUseSection.item8.detail.one")}</p>
        <p>{trans("helpAreaPage.accordionCanIUseSection.item8.detail.two")}</p>
      </div>
    ),
  },
];

const letterActivationCodeSection = [
  {
    title: t("helpAreaPage.letterActivationCodeSection.item1.title"),
    detail: (
      <div>
        <p>
          {trans("helpAreaPage.letterActivationCodeSection.item1.detail.one")}
        </p>
        <p>
          {trans("helpAreaPage.letterActivationCodeSection.item1.detail.two")}
        </p>
        <p>
          {trans("helpAreaPage.letterActivationCodeSection.item1.detail.three")}
        </p>
      </div>
    ),
  },
  {
    title: t("helpAreaPage.letterActivationCodeSection.item2.title"),
    detail: trans("helpAreaPage.letterActivationCodeSection.item2.detail"),
  },
  {
    title: t("helpAreaPage.letterActivationCodeSection.item3.title"),
    detail: (
      <div>
        <p>
          {trans("helpAreaPage.letterActivationCodeSection.item3.detail.one")}
        </p>
        <p>
          {trans("helpAreaPage.letterActivationCodeSection.item3.detail.two")}
        </p>
        <p>
          {trans("helpAreaPage.letterActivationCodeSection.item3.detail.three")}
        </p>
      </div>
    ),
  },
  {
    title: t("helpAreaPage.letterActivationCodeSection.item4.title"),
    detail: trans("helpAreaPage.letterActivationCodeSection.item4.detail"),
  },
  {
    title: t("helpAreaPage.letterActivationCodeSection.item5.title"),
    detail: trans("helpAreaPage.letterActivationCodeSection.item5.detail"),
  },
];

const submitTaxReturnSection = [
  {
    title: t("helpAreaPage.submitTaxReturnSection.item1.title"),
    detail: (
      <div>
        <p>{trans("helpAreaPage.submitTaxReturnSection.item1.detail.one")}</p>
        <p>{trans("helpAreaPage.submitTaxReturnSection.item1.detail.two")}</p>
      </div>
    ),
  },
  {
    title: t("helpAreaPage.submitTaxReturnSection.item2.title"),
    detail: (
      <div>
        <p>{trans("helpAreaPage.submitTaxReturnSection.item2.detail.one")}</p>
        <p>{trans("helpAreaPage.submitTaxReturnSection.item2.detail.two")}</p>
      </div>
    ),
  },
  {
    title: t("helpAreaPage.submitTaxReturnSection.item3.title"),
    detail: (
      <div>
        <p>{trans("helpAreaPage.submitTaxReturnSection.item3.detail.one")}</p>
        <p>{trans("helpAreaPage.submitTaxReturnSection.item3.detail.two")}</p>
      </div>
    ),
  },
  {
    title: t("helpAreaPage.submitTaxReturnSection.item4.title"),
    detail: trans("helpAreaPage.submitTaxReturnSection.item4.detail"),
  },
  {
    title: t("helpAreaPage.submitTaxReturnSection.item5.title"),
    detail: (
      <div>
        <p>{trans("helpAreaPage.submitTaxReturnSection.item5.detail.one")}</p>
        <p>{trans("helpAreaPage.submitTaxReturnSection.item5.detail.two")}</p>
      </div>
    ),
  },
  {
    title: t("helpAreaPage.submitTaxReturnSection.item6.title"),
    detail: trans("helpAreaPage.submitTaxReturnSection.item6.detail"),
  },
];

const afterSubmissionSection = [
  {
    title: t("helpAreaPage.afterSubmissionSection.item1.title"),
    detail: t("helpAreaPage.afterSubmissionSection.item1.detail"),
  },
  {
    title: t("helpAreaPage.afterSubmissionSection.item2.title"),
    detail: (
      <div>
        <p>{t("helpAreaPage.afterSubmissionSection.item2.detail.one")}</p>
        <p>{t("helpAreaPage.afterSubmissionSection.item2.detail.two")}</p>
        <p>{t("helpAreaPage.afterSubmissionSection.item2.detail.three")}</p>
      </div>
    ),
  },
  {
    title: t("helpAreaPage.afterSubmissionSection.item3.title"),
    detail: t("helpAreaPage.afterSubmissionSection.item3.detail"),
  },
  {
    title: t("helpAreaPage.afterSubmissionSection.item4.title"),
    detail: (
      <div>
        <p>{t("helpAreaPage.afterSubmissionSection.item4.detail.one")}</p>
        <p>{t("helpAreaPage.afterSubmissionSection.item4.detail.two")}</p>
      </div>
    ),
  },
];

export {
  accordionCanIUseSection,
  letterActivationCodeSection,
  submitTaxReturnSection,
  afterSubmissionSection,
};
