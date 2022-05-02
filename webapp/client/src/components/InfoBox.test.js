import React from "react";
import { render, screen } from "@testing-library/react";
import InfoBox from "./InfoBox";

function setup() {
  const MOCK_PROPS = {
    boxHeadline:
      "Sie sind vorbereitet und haben Ihren Freischaltcode erhalten?",
    boxText:
      "Wenn Sie den Brief mit Ihrem Freischaltcode erhalten haben, starten Sie mit Ihrer Steuererklärung.",
    anchor: {
      url: "/unlock_code_request/step/data_input?link_overview=False",
      text: "Jetzt anmelden",
    },
  };

  const utils = render(<InfoBox {...MOCK_PROPS} />);

  return { ...utils };
}

describe("InfoBox", () => {
  it("should render info box", () => {
    setup();

    const headline = screen.getByText(
      "Sie sind vorbereitet und haben Ihren Freischaltcode erhalten?"
    );
    const text = screen.getByText(
      "Wenn Sie den Brief mit Ihrem Freischaltcode erhalten haben, starten Sie mit Ihrer Steuererklärung."
    );
    const buttonAnchor = screen.getByText("Jetzt anmelden");
    const altImg = screen.getByAltText("Tablets mit Webapp des Steuerlotsen");

    expect(headline).toBeInTheDocument();
    expect(text).toBeInTheDocument();
    expect(buttonAnchor).toBeInTheDocument();
    expect(buttonAnchor.closest("a")).toHaveAttribute(
      "href",
      "/unlock_code_request/step/data_input?link_overview=False"
    );
    expect(altImg).toBeInTheDocument();
  });
});
