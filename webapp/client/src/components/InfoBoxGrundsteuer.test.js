import React from "react";
import { render, screen } from "@testing-library/react";
import InfoBoxGrundsteuer from "./InfoBoxGrundsteuer";

function setup() {
  const MOCK_PROPS = {
    boxHeadline: "Weitere Steuerprodukte vom DigitalService",
    boxText:
      "Mit unserem weiteren Service können private Eigentümerinnen ihre Grundsteuererklärung einfach und kostenlos online abgeben!",
    anchor: {
      url: "https://www.grundsteuererklaerung-fuer-privateigentum.de/",
      text: "Zum Service",
    },
  };

  const utils = render(<InfoBoxGrundsteuer {...MOCK_PROPS} />);

  return { ...utils };
}

describe("InfoBoxGrundsteuer", () => {
  it("should render info box", () => {
    setup();

    const headline = screen.getByText(
      "Weitere Steuerprodukte vom DigitalService"
    );
    const text = screen.getByText(
      "Mit unserem weiteren Service können private Eigentümerinnen ihre Grundsteuererklärung einfach und kostenlos online abgeben!"
    );
    const buttonAnchor = screen.getByText("Zum Service");
    const altImg = screen.getByAltText("Tablet mit Webapp der Grundsteuer");

    expect(headline).toBeInTheDocument();
    expect(text).toBeInTheDocument();
    expect(buttonAnchor).toBeInTheDocument();
    expect(buttonAnchor.closest("a")).toHaveAttribute(
      "href",
      "https://www.grundsteuererklaerung-fuer-privateigentum.de/"
    );
    expect(altImg).toBeInTheDocument();
  });
});
