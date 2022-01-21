import React from "react";
import { render, screen } from "@testing-library/react";
import UnlockCodeFailurePage from "./UnlockCodeFailurePage";

const MOCK_PROPS = {
  prevUrl: "/some/prev/path",
};
const EXPECTED_HEADER = {
  title: "Registrierung fehlgeschlagen. Bitte prüfen Sie Ihre Angaben.",
  intro:
    "Haben Sie sich vielleicht bereits registriert? In diesem Fall können Sie sich nicht erneut registrieren und bekommen einen Brief mit Ihrem persönlichen Freischaltcode von Ihrer Finanzverwaltung zugeschickt.",
};

describe("UnlockCodeFailurePage", () => {
  it("should render step header texts", () => {
    render(<UnlockCodeFailurePage {...MOCK_PROPS} />);
    expect(screen.getByText(EXPECTED_HEADER.title)).toBeInTheDocument();
    expect(screen.getByText(EXPECTED_HEADER.intro)).toBeInTheDocument();
  });

  it("should link to the previous page", () => {
    render(<UnlockCodeFailurePage {...MOCK_PROPS} />);
    expect(screen.getByText("Zurück").closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(MOCK_PROPS.prevUrl)
    );
  });
});
