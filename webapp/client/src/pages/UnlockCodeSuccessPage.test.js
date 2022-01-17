import React from "react";
import { render, screen } from "@testing-library/react";
import UnlockCodeSuccessPage from "./UnlockCodeSuccessPage";

const MOCK_PROPS = {
  prevUrl: "/some/prev/path",
  steuerErklaerungLink: "/some/link/path",
  vorbereitungsHilfeLink: "/some/link/path",
};
const EXPECTED_HEADER = {
  title: "Ihre Registrierung war erfolgreich!",
  intro:
    "Wir haben Ihren Antrag an Ihre Finanzverwaltung weitergeleitet. Sie können mit Ihrer Steuererklärung beginnen, sobald Sie Ihren Freischaltcode erhalten haben. Es kann bis zu zwei Wochen dauern, bis Sie Ihren Brief erhalten.",
};

describe("UnlockCodeSuccessPage", () => {
  it("should render step header texts", () => {
    render(<UnlockCodeSuccessPage {...MOCK_PROPS} />);
    expect(screen.getByText(EXPECTED_HEADER.title)).toBeInTheDocument();
    expect(screen.getByText(EXPECTED_HEADER.intro)).toBeInTheDocument();
  });

  it("should link to the previous page", () => {
    render(<UnlockCodeSuccessPage {...MOCK_PROPS} />);
    expect(screen.getByText("Zurück").closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(MOCK_PROPS.prevUrl)
    );
  });

  it("should link to download in text", () => {
    render(<UnlockCodeSuccessPage {...MOCK_PROPS} />);
    expect(screen.getByText("Vorbereitungshilfe").closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(MOCK_PROPS.vorbereitungsHilfeLink)
    );
  });

  it("should link to download on anchor button", () => {
    render(<UnlockCodeSuccessPage {...MOCK_PROPS} />);
    expect(
      screen.getByText("Vorbereitungshilfe herunterladen").closest("a")
    ).toHaveAttribute(
      "href",
      expect.stringContaining(MOCK_PROPS.vorbereitungsHilfeLink)
    );
  });
});
