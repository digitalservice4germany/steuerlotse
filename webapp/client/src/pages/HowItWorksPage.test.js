import React from "react";
import { render, screen } from "@testing-library/react";
import HowItWorksPage from "./HowItWorksPage";

jest.mock("../components/HowItWorksComponent.js", () => ({
  __esModule: true,
  default: function HowItWorksComponent() {
    return <div>HowItWorksComponent</div>;
  },
}));

const REQUIRED_PROPS = {
  youtubeLink: "https://www.youtube.com/watch?v=vP--fwSWtLE",
  startNowLink: "/eligibility/step/welcome?link_overview=False",
  helpPageLink: "/",
};

function setup() {
  const utils = render(<HowItWorksPage />);

  return { ...utils };
}

describe("HowItWorks Page", () => {
  it("should render the HowItWorks Page", () => {
    setup();

    const EXPECTED_HEADER = {
      title: "So funktioniert’s",
      intro:
        "Sie können Ihre Steuererklärung für sich alleine oder gemeinsam als Paar für das Jahr 2021 machen. Voraussetzung ist unter anderem, dass Sie Rente oder Pension beziehen, aber keine Zusatzeinkünfte haben, die Sie noch versteuern müssen.",
    };

    const headline = screen.getByText(EXPECTED_HEADER.title);
    const intro = screen.getByText(EXPECTED_HEADER.intro);
    const headline2 = screen.getByText(
      "Schritt-für-Schritt Anleitung (Erklärvideo)"
    );

    expect(headline).toBeInTheDocument();
    expect(headline2).toBeInTheDocument();
    expect(intro).toBeInTheDocument();
  });

  it("should link to the youtube page", () => {
    setup();
    const youtubeButton = screen.getByText("Auf Youtube abspielen");
    expect(youtubeButton.closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(REQUIRED_PROPS.youtubeLink)
    );
  });

  it("should link to the start now", () => {
    setup();
    const startNowButton = screen.getByText("Jetzt starten");
    expect(startNowButton.closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(REQUIRED_PROPS.startNowLink)
    );
  });

  it("should link to the help page", () => {
    setup();
    const helppageButton = screen.getByText("Zum Hilfebereich");
    expect(helppageButton.closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(REQUIRED_PROPS.helpPageLink)
    );
  });

  it("should render the HowItWorksComponent", () => {
    setup();
    expect(screen.getAllByText("HowItWorksComponent")).toHaveLength(7);
  });
});
