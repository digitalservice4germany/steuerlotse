import React from "react";
import { render, screen } from "@testing-library/react";
import ContentPageBox from "./ContentPageBox";

function setup() {
  const MOCK_PROPS = {
    boxText: {
      headerOne: "Kann ich den Steuerlotsen für meine Steuererklärung nutzen?",
      headerTwo: "Wo finde ich mehr Informationen zum Steuerlotsen?",
    },

    anchor: {
      eligibility: {
        url: "/eligibility/step/marital_status?link_overview=False",
        text: "Fragebogen starten",
      },
      faq: {
        url: "/sofunktionierts",
        text: "Häufig gestellte Fragen",
      },
      contact: {
        url: "mailto:kontakt@steuerlotse-rente.de",
        text: "Kontaktieren Sie uns",
      },
    },
    plausibleDomain: "/plausibleDomain/path",
  };

  const utils = render(<ContentPageBox {...MOCK_PROPS} />);

  return { ...utils };
}

describe("ContentPageBox", () => {
  it("should render info box", () => {
    setup();

    const textOne = screen.getByText(
      "Kann ich den Steuerlotsen für meine Steuererklärung nutzen?"
    );
    const textTwo = screen.getByText(
      "Wo finde ich mehr Informationen zum Steuerlotsen?"
    );

    const eligibilityButtonAnchor = screen.getByText("Fragebogen starten");
    const faqButtonAnchor = screen.getByText("Häufig gestellte Fragen");
    const contactUsButtonAnchor = screen.getByText("Kontaktieren Sie uns");

    expect(textOne).toBeInTheDocument();
    expect(textTwo).toBeInTheDocument();
    expect(eligibilityButtonAnchor).toBeInTheDocument();
    expect(faqButtonAnchor).toBeInTheDocument();
    expect(contactUsButtonAnchor).toBeInTheDocument();

    expect(eligibilityButtonAnchor.closest("a")).toHaveAttribute(
      "href",
      "/eligibility/step/marital_status?link_overview=False"
    );
    expect(faqButtonAnchor.closest("a")).toHaveAttribute(
      "href",
      "/sofunktionierts"
    );
    expect(contactUsButtonAnchor.closest("a")).toHaveAttribute(
      "href",
      "mailto:kontakt@steuerlotse-rente.de"
    );
  });
});
