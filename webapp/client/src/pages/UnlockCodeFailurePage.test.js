import React from "react";
import { render, screen } from "@testing-library/react";
import UnlockCodeFailurePage from "./UnlockCodeFailurePage";

const MOCK_PROPS = {
  prevUrl: "/some/prev/path",
};
const EXPECTED_HEADER = {
  title: "Registrierung fehlgeschlagen.",
};

const EXPECTED_TEXT = {
  title: "Mögliche Ursachen:",
};
describe("UnlockCodeFailurePage", () => {
  it("should render step header texts", () => {
    render(<UnlockCodeFailurePage {...MOCK_PROPS} />);
    expect(screen.getByText(EXPECTED_HEADER.title)).toBeInTheDocument();
  });

  it("should render possible reasons for failure", () => {
    render(<UnlockCodeFailurePage {...MOCK_PROPS} />);
    expect(screen.getByText(EXPECTED_TEXT.title)).toBeInTheDocument();
  });

  it("should link to the previous page", () => {
    render(<UnlockCodeFailurePage {...MOCK_PROPS} />);
    expect(screen.getByText("Zurück").closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(MOCK_PROPS.prevUrl)
    );
  });
});
