import React from "react";
import { render, screen } from "@testing-library/react";
import NewHerePage from "./NewHerePage";
import i18n from "i18next";
import { I18nextProvider } from "react-i18next";

describe("NewHerePage", () => {
  const newHereTexts = i18n.getDataByLanguage("de").translation.newHere;

  beforeEach(() => {
    render(
      <I18nextProvider i18n={i18n}>
        <NewHerePage />
      </I18nextProvider>
    );
  });

  it("should render title", () => {
    expect(screen.getByText(newHereTexts.title)).toBeDefined();
  });

  it("should render text1", () => {
    expect(screen.getByText(newHereTexts.text1)).toBeDefined();
  });

  it("should render button text", () => {
    expect(screen.getByText(newHereTexts.button)).toBeDefined();
  });

  it("button should link to einfachElster", () => {
    expect(screen.getByText(newHereTexts.button).closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(newHereTexts.url)
    );
  });

  it("button should link to retirement page", () => {
    expect(
      screen.getByText("„Ende des Steuerlotsen“").closest("a")
    ).toHaveAttribute("href", expect.stringContaining("/ende"));
  });
});
