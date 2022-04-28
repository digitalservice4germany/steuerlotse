import { t } from "i18next";

const anchorList = [
  {
    text: t("ContentPagesAnchors.Krankheitskosten.text"),
    url: "/krankheitskosten",
  },
  {
    text: t("ContentPagesAnchors.Vorsorgeaufwendungen.text"),
    url: "/vorsorgeaufwendungen",
  },
  {
    text: t("ContentPagesAnchors.Pflegekosten.text"),
    url: "/pflegekosten",
  },
  {
    text: t("ContentPagesAnchors.Behinderung.text"),
    url: "/kosten-aufgrund-einer-behinderung",
  },
  {
    text: t("ContentPagesAnchors.Bestattungskosten.text"),
    url: "/bestattungskosten",
  },
  {
    text: t("ContentPagesAnchors.Belastungen.text"),
    url: "/wiederbeschaffungskosten",
  },
  {
    text: t("ContentPagesAnchors.Dienstleistungen.text"),
    url: "/#",
  },
  {
    text: t("ContentPagesAnchors.Handwerkerleistungen.text"),
    url: "/#",
  },
  {
    text: t("ContentPagesAnchors.Spenden.text"),
    url: "/#",
  },
  {
    text: t("ContentPagesAnchors.Kirchensteuer.text"),
    url: "/#",
  },
];

const anchorBack = {
  text: t("anchorBackUebersicht.text"),
  url: "/#",
};

const anchorRegister = {
  text: t("anchorButton.anmelden.text"),
  url: "/unlock_code_request/step/data_input?link_overview=False",
};

export { anchorList, anchorBack, anchorRegister };
