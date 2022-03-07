import React from "react";
import { render, screen } from "@testing-library/react";
import { I18nextProvider } from "react-i18next";
import i18n from "i18next";
import FilingFailurePage from "./FilingFailurePage";

describe("FilingFailurePage", () => {
  beforeEach(() => {
    render(<FilingFailurePage />);
  });

  it("should render red cross icon", () => {
    expect(screen.getByText("failure_icon.svg").closest("svg")).toBeDefined();
  });

  it("should set correct alt text", () => {
    expect(
      screen.queryByAltText("Weißes Kreuzzeichen auf rotem Kreis")
    ).toBeDefined();
  });

  it("should render text us button", () => {
    expect(screen.getByText("Schreiben Sie uns").closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining("mailto:kontakt@steuerlotse-rente.de")
    );
  });
});

describe("FilingFailurePage translations", () => {
  const filingFailureTexts =
    i18n.getDataByLanguage("de").translation.filing.failure;

  beforeEach(() => {
    render(
      <I18nextProvider i18n={i18n}>
        <FilingFailurePage />
      </I18nextProvider>
    );
  });

  it("should render title", () => {
    expect(screen.getByText(filingFailureTexts.alert.title)).toBeDefined();
  });

  it("should render next step heading", () => {
    expect(screen.getByText(filingFailureTexts.nextStep.heading)).toBeDefined();
  });

  it("should render a element", () => {
    expect(
      screen.getByText("kontakt@steuerlotse-rente.de").closest("a")
    ).toHaveAttribute(
      "href",
      expect.stringContaining("mailto:kontakt@steuerlotse-rente.de")
    );
  });

  it("should render button text", () => {
    expect(screen.getByText(filingFailureTexts.textUs)).toBeDefined();
  });
});
