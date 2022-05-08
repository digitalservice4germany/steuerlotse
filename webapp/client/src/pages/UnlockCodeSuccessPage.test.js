import React from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import UnlockCodeSuccessPage from "./UnlockCodeSuccessPage";

const REQUIRED_PROPS = {
  prevUrl: "/some/prev/path",
  vorbereitungsHilfeLink: "/some/link/path",
};

function setup(optionalProps) {
  const utils = render(
    <UnlockCodeSuccessPage {...REQUIRED_PROPS} {...optionalProps} />
  );
  const downloadButton = screen.getByText("Vorbereitungshilfe speichern");
  const zurueckButton = screen.getByText("Zurück");
  const user = userEvent.setup();

  return { ...utils, downloadButton, zurueckButton, user };
}

describe("UnlockCodeSuccessPage", () => {
  it("should render step header texts", () => {
    setup();

    const EXPECTED_HEADER = {
      title:
        "Ihr Freischaltcode wurde bei Ihrem Finanzamt beantragt und wird Ihnen per Post zugeschickt.",
    };

    expect(screen.getByText(EXPECTED_HEADER.title)).toBeInTheDocument();
  });

  it("should link to the previous page", () => {
    const { zurueckButton } = setup();

    expect(zurueckButton.closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(REQUIRED_PROPS.prevUrl)
    );
  });

  it("should link to download on anchor button", () => {
    const { downloadButton } = setup();

    expect(downloadButton.closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(REQUIRED_PROPS.vorbereitungsHilfeLink)
    );
  });
});
