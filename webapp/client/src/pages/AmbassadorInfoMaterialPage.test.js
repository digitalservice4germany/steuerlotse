import React from "react";
import { render, screen } from "@testing-library/react";
import AmbassadorInfoMaterialPage from "./AmbassadorInfoMaterialPage";

const MOCK_PROPS = {
  plausibleDomain: "/plausibleDomain/path",
  downloadBroschureUrl: "/download_informationsbroschure_pdf",
  downloadFlyerUrl: "/download_steuerlotsen_flyer.pdf",
  PlayerUrl: "https://www.youtube.com/watch?v=vP--fwSWtLE",
};

describe("AmbassadorInfoMaterialPage", () => {
  it("should render the AmbassadorInfoMaterialPage component", () => {
    render(<AmbassadorInfoMaterialPage {...MOCK_PROPS} />);
  });

  beforeEach(() => {
    render(<AmbassadorInfoMaterialPage {...MOCK_PROPS} />);
  });

  it("should render InfoBroshure Download button with Link", () => {
    expect(
      screen.getByText("Informationsbroschüre (PDF) speichern")
    ).toBeInTheDocument();
    expect(
      screen.getByText("Informationsbroschüre (PDF) speichern").closest("a")
    ).toHaveAttribute(
      "href",
      expect.stringContaining(MOCK_PROPS.downloadBroschureUrl)
    );
  });

  it("should render Steuerlotse Flyer Download button with Link", () => {
    expect(
      screen.getByText("Steuerlotsen-Flyer (PDF) speichern")
    ).toBeInTheDocument();
    expect(
      screen.getByText("Steuerlotsen-Flyer (PDF) speichern").closest("a")
    ).toHaveAttribute(
      "href",
      expect.stringContaining(MOCK_PROPS.downloadFlyerUrl)
    );
  });

  it("should render Player Button with Link", () => {
    expect(screen.getByText("Auf Youtube abspielen")).toBeInTheDocument();
    expect(
      screen.getByText("Auf Youtube abspielen").closest("a")
    ).toHaveAttribute("href", expect.stringContaining(MOCK_PROPS.PlayerUrl));
  });
});
