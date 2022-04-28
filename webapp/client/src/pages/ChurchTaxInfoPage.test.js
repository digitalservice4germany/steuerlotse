import React from "react";
import { render, screen } from "@testing-library/react";
import { within } from "@testing-library/dom";
import ChurchTaxInfoPage from "./ChurchTaxInfoPage";

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
  const utils = render(<ChurchTaxInfoPage />);

  return { ...utils };
}

describe("ChurchTaxInfoPage", () => {
  it("should render ChurchTaxInfoPage", () => {
    setup();

    const headline1 = screen.getByText("Kirchensteuer");
    const headline2 = screen.getByText("Geleistete Zahlungen");
    const headline3 = screen.getByText("Erhaltene Erstattungen");
    const headline5 = screen.getByText(
      "Weitere Ausgaben, die Sie absetzen können"
    );
    const text1 = screen.getByText(
      "Sie können zum einen die Summe Ihrer im letzten Jahr gezahlten Kirchensteuer angeben.",
      { exact: false }
    );
    const text2 = screen.getByText(
      "Zahlen Sie Steuern für eine Religionsgemeinschaft, können Sie diese als Sonderausgabe absetzen",
      { exact: false }
    );
    const text3 = screen.getByText(
      "Haben Sie im letzten Jahr zu viel gezahlte Kirchensteuer erstattet bekommen, kann dies ebenfalls angegeben",
      { exact: false }
    );

    expect(headline1).toBeInTheDocument();
    expect(headline2).toBeInTheDocument();
    expect(headline3).toBeInTheDocument();
    expect(headline5).toBeInTheDocument();
    expect(text1).toBeInTheDocument();
    expect(text2).toBeInTheDocument();
    expect(text3).toBeInTheDocument();
  });

  it("should render the anchor list of ChurchTaxInfoPage", () => {
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
