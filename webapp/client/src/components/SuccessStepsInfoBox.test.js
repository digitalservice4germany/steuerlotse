import React from "react";
import { render, screen } from "@testing-library/react";
import SuccessStepsInfoBox from "./SuccessStepsInfoBox";

describe("SuccessStepsInfoBox", () => {
  const MOCK_PROPS_DEFAULT = {
    header: "Vorbereiten und Belege sammeln",
    text: "Sie können sich auf Ihre Steuererklärung vorbereiten, bis Sie den Brief erhalten haben.",
    anchor: {
      url: "/unlock_code_request/step/data_input?link_overview=False",
      text: "Vorbereitungshilfe speichern",
    },
    image: {
      src: "../../images/imageName.jpg",
      srcSetLargeScreen: "../../images/Img_Brief_1024.png",
      srcSetSmallerScreen: "../../images/Img_Brief_500.png",
      alt: "Beispielbild der letzten Briefseite mit Freischaltcode",
    },
  };

  beforeEach(() => {
    render(<SuccessStepsInfoBox {...MOCK_PROPS_DEFAULT} />);
  });

  it("should render the StepsInfoBox", () => {
    expect(
      screen.getByText("Vorbereiten und Belege sammeln")
    ).toBeInTheDocument();
    expect(
      screen.getByText(
        "Sie können sich auf Ihre Steuererklärung vorbereiten, bis Sie den Brief erhalten haben."
      )
    ).toBeInTheDocument();
    expect(
      screen.getByText("Vorbereitungshilfe speichern")
    ).toBeInTheDocument();
    expect(
      screen.getByAltText(
        "Beispielbild der letzten Briefseite mit Freischaltcode"
      )
    ).toBeInTheDocument();

    expect(
      screen.getByText("Vorbereitungshilfe speichern").closest("a")
    ).toHaveAttribute(
      "href",
      "/unlock_code_request/step/data_input?link_overview=False"
    );

    expect(
      screen
        .getByAltText("Beispielbild der letzten Briefseite mit Freischaltcode")
        .closest("img")
    ).toHaveAttribute("src", "../../images/imageName.jpg");
  });
});
