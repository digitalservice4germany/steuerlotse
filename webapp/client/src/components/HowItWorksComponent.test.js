import React from "react";
import { render, screen } from "@testing-library/react";
import HowItWorksComponent from "./HowItWorksComponent";

describe("HowItWorksComponent", () => {
  const MOCK_PROPS_DEFAULT = {
    heading: "Registrieren Sie sich unverbindlich",
    text: "Wenn Sie die Steuererklärung gemeinsam als Paar machen möchten, reicht es aus, wenn sich eine Person registriert.",
    image: {
      src: "../../images/imageName.jpg",
      srcSet: "../../images/imageName.jpg 1000w",
      alt: "test",
    },
    icon: {
      iconSrc: "../../images/imageName.jpg",
      altText: "Beispielbild der letzten Briefseite mit Freischaltcode",
    },
  };

  beforeEach(() => {
    render(<HowItWorksComponent {...MOCK_PROPS_DEFAULT} />);
  });

  it("should render the HowItWorksComponent", () => {
    expect(
      screen.getByText("Registrieren Sie sich unverbindlich")
    ).toBeInTheDocument();
    expect(
      screen.getByText(
        "Wenn Sie die Steuererklärung gemeinsam als Paar machen möchten, reicht es aus, wenn sich eine Person registriert."
      )
    ).toBeInTheDocument();
    expect(
      screen
        .getByAltText("Beispielbild der letzten Briefseite mit Freischaltcode")
        .closest("img")
    ).toHaveAttribute("src", "../../images/imageName.jpg");
  });
});
