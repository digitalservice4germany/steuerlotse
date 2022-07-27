import React from "react";
import { render, screen } from "@testing-library/react";
import HelpAreaPage from "./HelpAreaPage";

jest.mock("../components/AccordionComponent.js", () => ({
  __esModule: true,
  default: function AccordionComponent() {
    return <div>Accordion Component</div>;
  },
}));

const REQUIRED_PROPS = {
  mailTo: "mailto:kontakt@steuerlotse-rente.de",
};

function setup() {
  const utils = render(<HelpAreaPage />);

  return { ...utils };
}

describe("HelpAreaPage Page", () => {
  it("should render the HelpAreaPage Page", () => {
    setup();

    const EXPECTED_HEADER = {
      title: "Hilfebereich",
    };

    const headline = screen.getByText(EXPECTED_HEADER.title);

    const headline2 = screen.getByText("Kann ich den Steuerlotsen nutzen?");

    expect(headline).toBeInTheDocument();
    expect(headline2).toBeInTheDocument();
  });

  it("should link to open mail app", () => {
    setup();
    const contactUsButton = screen.getByText("Schreiben Sie uns");
    expect(contactUsButton.closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(REQUIRED_PROPS.mailTo)
    );
  });

  it("should render the AccordionComponent", () => {
    setup();
    expect(screen.getAllByText("Accordion Component")).toHaveLength(4);
  });
});
