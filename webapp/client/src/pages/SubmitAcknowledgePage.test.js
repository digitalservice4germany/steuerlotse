import React from "react";
import { render, screen } from "@testing-library/react";
import SubmitAcknowledgePage from "./SubmitAcknowledgePage";

const MOCK_PROPS = {
  prevUrl: "/some/prev/path",
  logoutUrl: "/some/link/path",
};

const EXPECTED_HEADER = {
  title: "Herzlichen Glückwunsch! Sie sind mit Ihrer Steuererklärung fertig!",
};

describe("SubmitAcknowledgePage", () => {
  it("should render step header texts", () => {
    render(<SubmitAcknowledgePage {...MOCK_PROPS} />);
    expect(screen.getByText(EXPECTED_HEADER.title)).toBeInTheDocument();
  });

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
