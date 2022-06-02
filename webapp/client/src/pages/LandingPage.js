import React from "react";
import { t } from "i18next";
import AccordionComponent from "../components/AccordionComponent";
import faqAnchorList from "../lib/faqAnchors";

export default function LandingPage() {
  return (
    <div>
      <div>Section one</div>
      <div>cards</div>
      <AccordionComponent
        title={t("vorbereitenOverview.Accordion.heading")}
        items={faqAnchorList}
      />
    </div>
  );
}
