import React from "react";
import { render, screen } from "@testing-library/react";
import RetirementPage from "./RetirementPage";

jest.mock("../components/AccordionComponent.js", () => ({
  __esModule: true,
  default: function AccordionComponent() {
    return <div>Accordion Component</div>;
  },
}));

function setup() {
  const utils = render(<RetirementPage />);

  return { ...utils };
}

const REQUIRED_PROPS = {
  howItWorksLink: "/sofunktionierts",
  helpPageLink: "/hilfebereich",
};

describe("Retirement Page", () => {
  it("should render the Retirement Page", () => {
    setup();

    const EXPECTED_HEADER = {
      title: "Der Steuerlotse geht in Rente",
    };

    const headline = screen.getByText(EXPECTED_HEADER.title);

    expect(headline).toBeInTheDocument();
  });

  it("should link to how it works page", () => {
    setup();
    const howItWorksButton = screen.getByText(
      "So funktioniert der Steuerlotse"
    );
    expect(howItWorksButton.closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(REQUIRED_PROPS.howItWorksLink)
    );
  });

  it("should link to the help page", () => {
    setup();
    const helpPagesButton = screen.getByText("Zum Hilfebereich");
    expect(helpPagesButton.closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(REQUIRED_PROPS.helpPageLink)
    );
  });

  it("should render the AccordionComponent", () => {
    setup();
    expect(screen.getAllByText("Accordion Component")).toHaveLength(1);
  });
});
