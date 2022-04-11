import React from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import UnlockCodeSuccessPage from "./UnlockCodeSuccessPage";

const REQUIRED_PROPS = {
  prevUrl: "/some/prev/path",
  steuerErklaerungLink: "/some/link/path",
  vorbereitungsHilfeLink: "/some/link/path",
};

function setup(optionalProps) {
  const utils = render(
    <UnlockCodeSuccessPage {...REQUIRED_PROPS} {...optionalProps} />
  );
  const downloadAnchor = screen.getByText("Vorbereitungshilfe");
  const downloadButton = screen.getByText("Vorbereitungshilfe herunterladen");
  const zurueckButton = screen.getByText("Zurück");

  return { ...utils, downloadAnchor, downloadButton, zurueckButton };
}

describe("UnlockCodeSuccessPage", () => {
  it("should render step header texts", () => {
    setup();

    const EXPECTED_HEADER = {
      title: "Ihre Registrierung war erfolgreich!",
      intro:
        "Wir haben Ihren Antrag an Ihre Finanzverwaltung weitergeleitet. Sie können mit Ihrer Steuererklärung beginnen, sobald Sie Ihren Freischaltcode erhalten haben. Es kann bis zu zwei Wochen dauern, bis Sie Ihren Brief erhalten.",
    };

    expect(screen.getByText(EXPECTED_HEADER.title)).toBeInTheDocument();
    expect(screen.getByText(EXPECTED_HEADER.intro)).toBeInTheDocument();
  });

  it("should link to the previous page", () => {
    const { zurueckButton } = setup();

    expect(zurueckButton.closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(REQUIRED_PROPS.prevUrl)
    );
  });

  it("should link to download in text", () => {
    const { downloadAnchor } = setup();

    expect(downloadAnchor.closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(REQUIRED_PROPS.vorbereitungsHilfeLink)
    );
  });

  it("should link to download on anchor button", () => {
    const { downloadButton } = setup();

    expect(downloadButton.closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(REQUIRED_PROPS.vorbereitungsHilfeLink)
    );
  });

  it("should call plausible with name and props, when user clicks on download button", async () => {
    const { downloadButton } = setup({
      plausibleDomain: "http://localhost:3000",
    });

    const EXPECTED_PLAUSIBLE_GOAL = "Vorbereitungshilfe";
    const EXPECTED_PLAUSIBLE_PROPS = {
      props: { method: "CTA Vorbereitungshilfe herunterladen" },
    };

    window.plausible = jest.fn();

    await userEvent.click(downloadButton);

    expect(window.plausible).toHaveBeenCalledWith(
      EXPECTED_PLAUSIBLE_GOAL,
      EXPECTED_PLAUSIBLE_PROPS
    );
  });

  it("should call plausible with name and props, when user clicks on download link", async () => {
    const { downloadAnchor } = setup({
      plausibleDomain: "http://localhost:3000",
    });

    const EXPECTED_PLAUSIBLE_GOAL = "Vorbereitungshilfe";
    const EXPECTED_PLAUSIBLE_PROPS = {
      props: { method: "CTA Vorbereitungshilfe" },
    };

    window.plausible = jest.fn();

    await userEvent.click(downloadAnchor);

    expect(window.plausible).toHaveBeenCalledWith(
      EXPECTED_PLAUSIBLE_GOAL,
      EXPECTED_PLAUSIBLE_PROPS
    );
  });

  it("should not call plausible if no plausible domain given", async () => {
    const { downloadButton, downloadAnchor } = setup();

    window.plausible = jest.fn();

    await userEvent.click(downloadButton);

    expect(window.plausible).not.toHaveBeenCalled();

    await userEvent.click(downloadAnchor);

    expect(window.plausible).not.toHaveBeenCalled();
  });
});
