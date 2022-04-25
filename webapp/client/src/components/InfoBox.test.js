import React from "react";
import { render, screen } from "@testing-library/react";
import InfoBox from "./InfoBox";

const REQUIRED_PROPS = {
  fscRequestUrl: "url/some/link/path",
};

function setup(optionalProps) {
  const utils = render(<InfoBox {...REQUIRED_PROPS} {...optionalProps} />);

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
    const altImg = screen.getByAltText("teaser img");

    expect(headline).toBeInTheDocument();
    expect(text).toBeInTheDocument();
    expect(buttonAnchor).toBeInTheDocument();
    expect(buttonAnchor.closest("a")).toHaveAttribute(
      "href",
      REQUIRED_PROPS.fscRequestUrl
    );
    expect(altImg).toBeInTheDocument();
  });
});
