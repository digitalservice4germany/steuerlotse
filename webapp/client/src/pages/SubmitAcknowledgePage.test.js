import React from "react";
import { render, screen } from "@testing-library/react";
import SubmitAcknowledgePage from "./SubmitAcknowledgePage";
import { I18nextProvider } from "react-i18next";
import i18n from "i18next";

const MOCK_PROPS = {
  prevUrl: "/some/prev/path",
  logoutUrl: "/some/link/path",
};

describe("SubmitAcknowledgePage", () => {
  it("should link to the previous page", () => {
    render(<SubmitAcknowledgePage {...MOCK_PROPS} />);
    expect(screen.getByText("Zurück").closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(MOCK_PROPS.prevUrl)
    );
  });

  it("should link to logout in text", () => {
    render(<SubmitAcknowledgePage {...MOCK_PROPS} />);
    expect(screen.getByText("Abmelden").closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(MOCK_PROPS.logoutUrl)
    );
  });
});

describe("SubmitAcknowledgePage translations", () => {
  let c;

  const submitAcknowledge =
    i18n.getDataByLanguage("de").translation.submitAcknowledge;

  beforeEach(() => {
    c = render(
      <I18nextProvider i18n={i18n}>
        <SubmitAcknowledgePage {...MOCK_PROPS} />
      </I18nextProvider>
    );
  });

  it("should render step header texts", () => {
    expect(c.getByText(submitAcknowledge.successMessage)).toBeDefined();
  });

  it("should render next steps header", () => {
    expect(c.getByText(submitAcknowledge["next-steps"].heading)).toBeDefined();
  });

  it("should render next steps text", () => {
    expect(c.getByText(submitAcknowledge["next-steps"].text)).toBeDefined();
  });

  it("should render recommend header", () => {
    expect(c.getByText(submitAcknowledge.recommend.heading)).toBeDefined();
  });

  it("should render recommend text", () => {
    expect(c.getByText(submitAcknowledge.recommend.text)).toBeDefined();
  });

  it("should render logout header", () => {
    expect(c.getByText(submitAcknowledge.logout.heading)).toBeDefined();
  });

  it("should render logout text", () => {
    expect(c.getByText(submitAcknowledge.logout.text)).toBeDefined();
  });
});
