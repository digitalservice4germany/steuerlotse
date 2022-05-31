import { t } from "i18next";

const anchorList = [
  {
    text: t("ContentPagesAnchors.Vorsorgeaufwendungen.text"),
    url: "/vorbereiten/vorsorgeaufwendungen",
  },
  {
    text: t("ContentPagesAnchors.Krankheitskosten.text"),
    url: "/vorbereiten/krankheitskosten",
  },
  {
    text: t("ContentPagesAnchors.Pflegekosten.text"),
    url: "/vorbereiten/pflegekosten",
  },
  {
    text: t("ContentPagesAnchors.Behinderung.text"),
    url: "/vorbereiten/angaben-bei-behinderung",
  },
  {
    text: t("ContentPagesAnchors.Bestattungskosten.text"),
    url: "/vorbereiten/bestattungskosten",
  },
  {
    text: t("ContentPagesAnchors.Belastungen.text"),
    url: "/vorbereiten/wiederbeschaffungskosten",
  },
  {
    text: t("ContentPagesAnchors.Dienstleistungen.text"),
    url: "/vorbereiten/haushaltsnahe-dienstleistungen",
  },
  {
    text: t("ContentPagesAnchors.Handwerkerleistungen.text"),
    url: "/vorbereiten/handwerkerleistungen",
  },
  {
    text: t("ContentPagesAnchors.Spenden.text"),
    url: "/vorbereiten/spenden-und-mitgliedsbeitraege",
  },
  {
    text: t("ContentPagesAnchors.Kirchensteuer.text"),
    url: "/vorbereiten/kirchensteuer",
  },
];

const anchorBack = {
  text: t("anchorBackUebersicht.text"),
  url: "/vorbereiten",
};

const anchorRegister = {
  headline: t("InfoBox.heading"),
  text: t("anchorButton.anmelden.text"),
  url: "/unlock_code_request/step/data_input?link_overview=False",
};

const anchorPrufen = {
  text: t("CheckNowInfoBox.button"),
  headline: t("CheckNowInfoBox.heading"),
  url: "/eligibility/step/tax_year?link_overview=False",
};

export { anchorList, anchorBack, anchorRegister, anchorPrufen };
