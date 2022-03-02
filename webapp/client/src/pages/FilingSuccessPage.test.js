import React from "react";
import { render, screen } from "@testing-library/react";
import { I18nextProvider } from "react-i18next";
import i18n from "i18next";
import FilingSuccessPage from "./FilingSuccessPage";

const MOCK_PROPS = {
  nextUrl: "/lotse/step/ack",
  transferTicket: "et0453tpo67bku056b0kx5waznjbo0r8",
  downloadUrl: "/download_pdf",
};

describe("FilingSuccessPage", () => {
  beforeEach(() => {
    render(<FilingSuccessPage {...MOCK_PROPS} />);
  });

  it("should render download a", () => {
    expect(
      screen.getByText("Übersicht speichern").closest("a")
    ).toHaveAttribute("href", expect.stringContaining(MOCK_PROPS.downloadUrl));
  });

  it("should render next button", () => {
    expect(screen.getByText("Weiter").closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(MOCK_PROPS.nextUrl)
    );
  });
});

describe("FilingSuccessPage translations", () => {
  const filingSuccessTexts =
    i18n.getDataByLanguage("de").translation.filingSuccess;

  beforeEach(() => {
    render(
      <I18nextProvider i18n={i18n}>
        <FilingSuccessPage {...MOCK_PROPS} />
      </I18nextProvider>
    );
  });

  it("should render title", () => {
    expect(screen.getByText(filingSuccessTexts.title)).toBeDefined();
  });

  it("should render intro", () => {
    expect(screen.getByText(filingSuccessTexts.intro)).toBeDefined();
  });

  it("should render transfer ticket heading", () => {
    expect(
      screen.getByText(filingSuccessTexts.transfer_ticket.heading)
    ).toBeDefined();
  });

  it('should render transfer ticket text"', () => {
    expect(
      screen.getByText(filingSuccessTexts.transfer_ticket.text)
    ).toBeDefined();
  });

  it('should render transfer ticket your"', () => {
    expect(
      screen.getByText(
        filingSuccessTexts.transfer_ticket.your +
          " " +
          MOCK_PROPS.transferTicket
      )
    ).toBeDefined();
  });

  it("should render pdf heading", () => {
    expect(screen.getByText(filingSuccessTexts.pdf.heading)).toBeDefined();
  });

  it("should render pdf text", () => {
    expect(screen.getByText(filingSuccessTexts.pdf.text)).toBeDefined();
  });

  it("should render pdf download", () => {
    expect(screen.getByText(filingSuccessTexts.pdf.download)).toBeDefined();
  });
});
