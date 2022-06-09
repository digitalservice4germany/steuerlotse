import { t } from "i18next";
import { Trans } from "react-i18next";

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
          <a href="/eligibility/step/tax_year?link_overview=False" />
        ),
        registrationLink: (
          // eslint-disable-next-line jsx-a11y/anchor-has-content
          <a href="/unlock_code_request/step/data_input?link_overview=False" />
        ),
        activationLink: (
          // eslint-disable-next-line jsx-a11y/anchor-has-content
          <a href="/unlock_code_activation/step/data_input?link_overview=False" />
        ),
        shareLink: (
          // eslint-disable-next-line jsx-a11y/anchor-has-content
          <a href="/vereinfachte-steuererklärung-für-rentner" />
        ),
        digitalServiceLink: (
          // eslint-disable-next-line jsx-a11y/anchor-has-content
          <a href="https://digitalservice.bund.de/" />
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
        simplifiedPaperFormLink: (
          // eslint-disable-next-line jsx-a11y/anchor-has-content
          <a href="https://www.bundesfinanzministerium.de/Content/DE/Standardartikel/Themen/Steuern/Steuerliche_Themengebiete/Altersvorsorge/2019-04-29-Laendervordruck-vereinfachte-veranlagung-rentner.html" />
        ),
      }}
    />
  );
}
const faqAnchorList = [
  {
    title: t("LandingPage.Accordion.Item1.title"),
    detail: trans("LandingPage.Accordion.Item1.detail"),
  },
  {
    title: t("LandingPage.Accordion.Item2.title"),
    detail: (
      <div>
        <p>{t("LandingPage.Accordion.Item2.detail")}</p>
        <ul>
          <li>{trans("LandingPage.Accordion.Item2.listItem1")}</li>
          <li>{trans("LandingPage.Accordion.Item2.listItem2")}</li>
          <li>{t("LandingPage.Accordion.Item2.listItem3")}</li>
          <li>{trans("LandingPage.Accordion.Item2.listItem4")}</li>
        </ul>
      </div>
    ),
  },
  {
    title: t("LandingPage.Accordion.Item3.title"),
    detail: trans("LandingPage.Accordion.Item3.detail"),
  },
  {
    title: t("LandingPage.Accordion.Item4.title"),
    detail: (
      <div>
        <p>{t("LandingPage.Accordion.Item4.detailOne")}</p>
        <ul>
          <li>{t("LandingPage.Accordion.Item4.listItem1")}</li>
          <li>{t("LandingPage.Accordion.Item4.listItem2")}</li>
          <li>{t("LandingPage.Accordion.Item4.listItem3")}</li>
          <li>{t("LandingPage.Accordion.Item4.listItem4")}</li>
        </ul>
        <p>{trans("LandingPage.Accordion.Item4.detailTwo")}</p>
      </div>
    ),
  },
  {
    title: t("LandingPage.Accordion.Item5.title"),
    detail: t("LandingPage.Accordion.Item5.detail"),
  },
  {
    title: t("LandingPage.Accordion.Item6.title"),
    detail: t("LandingPage.Accordion.Item6.detail"),
  },
  {
    title: t("LandingPage.Accordion.Item7.title"),
    detail: trans("LandingPage.Accordion.Item7.detail"),
  },
  {
    title: t("LandingPage.Accordion.Item8.title"),
    detail: trans("LandingPage.Accordion.Item8.detail"),
  },
];

export default faqAnchorList;
