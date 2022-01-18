import React from "react";
import { render, screen } from "@testing-library/react";
import RevocationFailureStepPage from "./RevocationFailurePage";

const MOCK_PROPS = {
  prevUrl: "/some/prev/path",
};
const EXPECTED_HEADER = {
  title: "Stornierung fehlgeschlagen. Bitte prüfen Sie Ihre Angaben.",
  intro:
    "Sind Sie vielleicht noch nicht bei uns registriert? In diesem Fall können Sie Ihren Freischaltcode nicht stornieren. Haben Sie Ihre Steuererklärung bereits erfolgreich verschickt? Dann haben wir Ihren Freischaltcode automatisiert storniert und Sie müssen nichts weiter tun.",
};

describe("RevocationFailureStepPage", () => {
  it("should render step header texts", () => {
    render(<RevocationFailureStepPage {...MOCK_PROPS} />);
    expect(screen.getByText(EXPECTED_HEADER.title)).toBeInTheDocument();
    expect(screen.getByText(EXPECTED_HEADER.intro)).toBeInTheDocument();
  });

  it("should link to the previous page", () => {
    render(<RevocationFailureStepPage {...MOCK_PROPS} />);
    expect(screen.getByText("Zurück").closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(MOCK_PROPS.prevUrl)
    );
  });
});
