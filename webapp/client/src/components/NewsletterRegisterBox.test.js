import React from "react";
import { render, screen } from "@testing-library/react";
import i18n from "i18next";
import { I18nextProvider } from "react-i18next";
import NewsletterRegisterBox from "./NewsletterRegisterBox";

const DEFAULT_PROPS = {
  dataPrivacyLink: "/some-link",
};

describe("NewsletterRegisterBox translations", () => {
  const newsletterTexts = i18n.getDataByLanguage("de").translation.newsletter;

  beforeEach(() => {
    render(
      <I18nextProvider i18n={i18n}>
        <NewsletterRegisterBox {...DEFAULT_PROPS} />
      </I18nextProvider>
    );
  });

  it("should render headline", () => {
    expect(screen.getByText(newsletterTexts.headline)).toBeDefined();
  });

  it("should render text", () => {
    expect(screen.getByText(newsletterTexts.text)).toBeDefined();
  });

  it("should render field email label", () => {
    expect(screen.getByText(newsletterTexts.fieldEmail.label)).toBeDefined();
  });

  it("should render button label", () => {
    expect(screen.getByText(newsletterTexts.button.label)).toBeDefined();
  });
});

describe("NewsletterSuccessPage", () => {
  beforeEach(() => {
    render(<NewsletterRegisterBox {...DEFAULT_PROPS} />);
  });

  it("should render field", () => {
    expect(screen.getByLabelText("Ihre E-Mail Adresse")).toBeInTheDocument();
  });

  it("button should link to the URL", () => {
    expect(
      screen.getByText("Datenschutzerklärung").closest("a")
    ).toHaveAttribute(
      "href",
      expect.stringContaining(DEFAULT_PROPS.dataPrivacyLink)
    );
  });
});
