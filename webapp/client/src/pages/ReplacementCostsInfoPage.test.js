import React from "react";
import { render, screen } from "@testing-library/react";
import { within } from "@testing-library/dom";
import ReplacementCostsInfoPage from "./ReplacementCostsInfoPage";

jest.mock("../components/InfoBox", () => ({
  __esModule: true,
  default: function InfoBox() {
    return <div>info box</div>;
  },
}));

jest.mock("../components/StepHeaderButtons", () => ({
  __esModule: true,
  default: function StepHeaderButtons() {
    return <div>StepHeaderButtons</div>;
  },
}));

function setup() {
  const utils = render(<ReplacementCostsInfoPage />);

  return { ...utils };
}

describe("ReplacementCostsInfoPage", () => {
  it("should render the ReplacementCostsInfoPage", () => {
    setup();

    const headline1 = screen.getByText("Wiederbeschaffungskosten");
    const headline2 = screen.getByText(
      "Was können sonstige außergewöhnliche Belastungen sein?"
    );
    const headline3 = screen.getByText("Die zumutbare Belastung");
    const headline4 = screen.getByText(
      "Weitere Ausgaben, die Sie absetzen können"
    );
    const text1 = screen.getByText(
      "Wiederbaschaffungskosten können unter anderem bei den sonstigen außergewöhnlichen Belastungen angegeben werden",
      { exact: false }
    );

    expect(headline1).toBeInTheDocument();
    expect(headline2).toBeInTheDocument();
    expect(headline3).toBeInTheDocument();
    expect(headline4).toBeInTheDocument();
    expect(text1).toBeInTheDocument();
  });

  it("should render the anchor list of ReplacementCostsInfoPage", () => {
    setup();

    const anchorList = screen.getByRole("list", {
      name: "anchor-list",
    });
    const { getAllByRole } = within(anchorList);
    const items = getAllByRole("listitem");
    expect(items.length).toBe(9);
  });

  it("should render the info box component", () => {
    setup();

    expect(screen.getByText("info box")).toBeInTheDocument();
  });

  it("should render the StepHeaderButtons component", () => {
    setup();

    expect(screen.getByText("StepHeaderButtons")).toBeInTheDocument();
  });
});
