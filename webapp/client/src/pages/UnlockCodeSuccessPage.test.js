import React from "react";
import { render, screen } from "@testing-library/react";
import UnlockCodeSuccessPage from "./UnlockCodeSuccessPage";

const MOCK_PROPS = {
  stepHeader: {
    title: "Title",
    intro: "Intro",
  },
  prevUrl: "/some/prev/path",
  nextUrl: "/some/next/path",
  downloadUrl: "/some/download/path",
};

describe("UnlockCodeSuccessPage", () => {
  it("should render step header texts", () => {
    render(<UnlockCodeSuccessPage {...MOCK_PROPS} />);
    expect(screen.getByText(MOCK_PROPS.stepHeader.title)).toBeInTheDocument();
    expect(screen.getByText(MOCK_PROPS.stepHeader.intro)).toBeInTheDocument();
  });

  it("should link to the previous page", () => {
    render(<UnlockCodeSuccessPage {...MOCK_PROPS} />);
    expect(screen.getByText("Zurück").closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(MOCK_PROPS.prevUrl)
    );
  });

  it("should link to the next page", () => {
    render(<UnlockCodeSuccessPage {...MOCK_PROPS} />);
    expect(screen.getByText("Weiter").closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(MOCK_PROPS.nextUrl)
    );
  });

  it("should link to download", () => {
    render(<UnlockCodeSuccessPage {...MOCK_PROPS} />);
    expect(
      screen.getByText("Vorbereitungshilfe herunterladen").closest("a")
    ).toHaveAttribute("href", expect.stringContaining(MOCK_PROPS.downloadUrl));
  });
});
