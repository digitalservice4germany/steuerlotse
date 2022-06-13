import React from "react";
import { render, screen } from "@testing-library/react";
import InfoTaxReturnForPensionersPage from "./InfoTaxReturnForPensionersPage";

jest.mock("../components/InfoBox", () => ({
  __esModule: true,
  default: function InfoBox() {
    return <div>InfoBox</div>;
  },
}));

jest.mock("../components/SuccessStepsInfoBox", () => ({
  __esModule: true,
  default: function SuccessStepsInfoBox() {
    return <div>Steps Info Box</div>;
  },
}));

function setup() {
  const MOCK_PROPS = {
    plausibleDomain: "/plausibleDomain/path",
  };
  const utils = render(<InfoTaxReturnForPensionersPage {...MOCK_PROPS} />);

  return { ...utils };
}

describe("InfoTaxReturnForPensionersPage", () => {
  it("should render the InfoTaxReturnForPensionersPage page", () => {
    setup();

    const headline1 = screen.getByText(
      "Vereinfachte Steuererklärung für Rentner — wie Sie in wenigen Minuten Ihre Steuererklärung kostenlos online machen können"
    );
    const headline2 = screen.getByText(
      "Die vereinfachte Steuererklärung wurde speziell für Menschen im Ruhestand entwickelt"
    );
    const headline3 = screen.getByText(
      "Wie finde ich heraus, ob ich als Rentner steuerpflichtig bin?"
    );
    const headline4 = screen.getByText(
      "So funktioniert der Steuerlotse für Rente und Pension"
    );

    expect(headline1).toBeInTheDocument();
    expect(headline2).toBeInTheDocument();
    expect(headline3).toBeInTheDocument();
    expect(headline4).toBeInTheDocument();
  });

  it("should render the ContentPageBox component", () => {
    setup();

    expect(screen.getByText("InfoBox")).toBeInTheDocument();
  });

  it("should render the SuccessStepsInfoBox component", () => {
    setup();

    expect(screen.getByText("Steps Info Box")).toBeInTheDocument();
  });
});
