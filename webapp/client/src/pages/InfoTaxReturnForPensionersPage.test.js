import React from "react";
import { render, screen } from "@testing-library/react";
import InfoTaxReturnForPensionersPage from "./InfoTaxReturnForPensionersPage";

const MOCK_PROPS = {
  plausibleDomain: "/plausibleDomain/path",
  url: "/eligibility/step/marital_status?link_overview=False",
  contactUsUrl: "mailto:kontakt@steuerlotse-rente.de",
  howItWorksLink: "/sofunktionierts",
};

describe("InfoTaxReturnForPensionersPage", () => {
  it("should render the InfoTaxReturnForPensionersPage component", () => {
    render(<InfoTaxReturnForPensionersPage {...MOCK_PROPS} />);
  });

  beforeEach(() => {
    render(<InfoTaxReturnForPensionersPage {...MOCK_PROPS} />);
  });

  it("should render Start Questionnaire button with Link", () => {
    expect(screen.getByText("Fragebogen starten")).toBeInTheDocument();
    expect(screen.getByText("Fragebogen starten").closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(MOCK_PROPS.url)
    );
  });

  it("should render Contact Us button with Link", () => {
    expect(screen.getByText("Kontaktieren Sie uns")).toBeInTheDocument();
    expect(
      screen.getByText("Kontaktieren Sie uns").closest("a")
    ).toHaveAttribute("href", expect.stringContaining(MOCK_PROPS.contactUsUrl));
  });

  it("should render more information tax guide button", () => {
    expect(screen.getByText("Häufig gestellte Fragen")).toBeInTheDocument();
    expect(
      screen.getByText("Häufig gestellte Fragen").closest("a")
    ).toHaveAttribute(
      "href",
      expect.stringContaining(MOCK_PROPS.howItWorksLink)
    );
  });
});
