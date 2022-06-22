import React from "react";
import { render, screen } from "@testing-library/react";
import AmbassadorInfoMaterialPage from "./AmbassadorInfoMaterialPage";

const MOCK_PROPS = {
  plausibleDomain: "/plausibleDomain/path",
  downloadBroschureUrl: "/download_informationsbroschure_pdf",
  downloadFlyerUrl: "/download_steuerlotsen_flyer.pdf",
  contactUsUrl: "mailto:kontakt@steuerlotse-rente.de",
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
      screen.getByText("Informationsbroschüre speichern [PDF]")
    ).toBeInTheDocument();
    expect(
      screen.getByText("Informationsbroschüre speichern [PDF]").closest("a")
    ).toHaveAttribute(
      "href",
      expect.stringContaining(MOCK_PROPS.downloadBroschureUrl)
    );
  });

  it("should render Steuerlotse Flyer Download button with Link", () => {
    expect(
      screen.getByText("Flyer zum Steuerlotsen speichern [PDF]")
    ).toBeInTheDocument();
    expect(
      screen.getByText("Flyer zum Steuerlotsen speichern [PDF]").closest("a")
    ).toHaveAttribute(
      "href",
      expect.stringContaining(MOCK_PROPS.downloadFlyerUrl)
    );
  });

  it("should render Contact Us Button with Link", () => {
    expect(screen.getByText("Schreiben Sie uns")).toBeInTheDocument();
    expect(screen.getByText("Schreiben Sie uns").closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(MOCK_PROPS.contactUsUrl)
    );
  });
});
