import React from "react";
import { render, screen } from "@testing-library/react";
import RevocationFailureStepPage from "./RevocationFailurePage";

const MOCK_PROPS = {
  prevUrl: "/some/prev/path",
};
const EXPECTED_HEADER = {
  title: "Stornierung fehlgeschlagen",
};

const EXPECTED_TEXT = {
  title: "Mögliche Ursachen:",
};

describe("RevocationFailureStepPage", () => {
  it("should render step header texts", () => {
    render(<RevocationFailureStepPage {...MOCK_PROPS} />);
    expect(screen.getByText(EXPECTED_HEADER.title)).toBeInTheDocument();
  });

  it("should render possible causes", () => {
    render(<RevocationFailureStepPage {...MOCK_PROPS} />);
    expect(screen.getByText(EXPECTED_TEXT.title)).toBeInTheDocument();
  });

  it("should link to the previous page", () => {
    render(<RevocationFailureStepPage {...MOCK_PROPS} />);
    expect(screen.getByText("Zurück").closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(MOCK_PROPS.prevUrl)
    );
  });
});
