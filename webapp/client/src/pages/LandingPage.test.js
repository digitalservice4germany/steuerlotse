import React from "react";
import { render, screen } from "@testing-library/react";
import LandingPage from "./LandingPage";

jest.mock("../components/CardsComponent.js", () => ({
  __esModule: true,
  default: function CardsComponent() {
    return <div>Cards Component</div>;
  },
}));

jest.mock("../components/AccordionComponent.js", () => ({
  __esModule: true,
  default: function AccordionComponent() {
    return <div>Accordion Component</div>;
  },
}));

function setup() {
  const utils = render(<LandingPage />);

  return { ...utils };
}

describe("Landing Page", () => {
  it("should render the Landing Page", () => {
    setup();

    const headline = screen.getByText(
      "Die vereinfachte Steuererklärung für Menschen im Ruhestand"
    );
    const text = screen.getByText(
      "Mit dem Steuerlotsen können Sie Ihre Steuererklärung für das Steuerjahr 2021 einfach und ohne besonderes Vorwissen online machen."
    );
    const text2 = screen.queryByText(
      "Möchten Sie wissen, ob Sie den Steuerlotsen nutzen können?"
    );

    expect(headline).toBeInTheDocument();
    expect(text).toBeInTheDocument();
    expect(text2).not.toBeInTheDocument();
  });

  it("should render the Cards component", () => {
    setup();

    expect(screen.getByText("Cards Component")).toBeInTheDocument();
  });

  it("should render the Accordion component", () => {
    setup();

    expect(screen.getByText("Accordion Component")).toBeInTheDocument();
  });
});
