import React from "react";
import { render, screen } from "@testing-library/react";
import UnlockCodeSuccessPage from "./UnlockCodeSuccessPage";

const MOCK_PROPS = {
  stepHeader: {
    title: "Title",
    intro: "Intro",
  },
  prevUrl: "/some/prev/path",
  downloadUrl: "/some/download/path",
  steuerErklaerungsLink: "/some/link/path",
  vorbereitungshilfeLink: "/some/link/path",
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

  it("should link to download in text", () => {
    render(<UnlockCodeSuccessPage {...MOCK_PROPS} />);
    expect(screen.getByText("Vorbereitungshilfe").closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(MOCK_PROPS.vorbereitungshilfeLink)
    );
  });

  it("should link to download on anchor button", () => {
    render(<UnlockCodeSuccessPage {...MOCK_PROPS} />);
    expect(
      screen.getByText("Vorbereitungshilfe herunterladen").closest("a")
    ).toHaveAttribute("href", expect.stringContaining(MOCK_PROPS.downloadUrl));
  });
});
