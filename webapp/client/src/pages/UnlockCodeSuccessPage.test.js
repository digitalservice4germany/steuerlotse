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

describe("should call plausible with name and props, when user clicks on download button", () => {
  const user = userEvent.setup();
  const MOCK_PROPS_DEFAULT = {
    header: "Vorbereiten und Belege sammeln",
    text: "Sie können sich auf Ihre Steuererklärung vorbereiten, bis Sie den Brief erhalten haben.",
    anchor: {
      url: "/unlock_code_request/step/data_input?link_overview=False",
      text: "Vorbereitungshilfe speichern",
    },
    image: {
      src: "../../images/imageName.jpg",
      srcSet: "../../images/imageName.jpg 1000w",
      alt: "Beispielbild der letzten Briefseite mit Freischaltcode",
    },
    plausibleDomain: "http://localhost:3000",
  };

  beforeEach(() => {
    window.plausible = jest.fn();
    render(<UnlockCodeSuccessPage {...MOCK_PROPS_DEFAULT} />);
  });

  it("should add plausible goal for download button", async () => {
    await user.click(screen.getByText("Vorbereitungshilfe speichern"));
    const EXPECTED_PLAUSIBLE_GOAL = "Vorbereitungshilfe";
    const EXPECTED_PLAUSIBLE_PROPS = {
      props: { method: "CTA Vorbereitungshilfe herunterladen" },
    };
    expect(window.plausible).toHaveBeenCalledWith(
      EXPECTED_PLAUSIBLE_GOAL,
      EXPECTED_PLAUSIBLE_PROPS
    );
  });
});
