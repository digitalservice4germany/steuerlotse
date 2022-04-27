import React from "react";
import { render, screen } from "@testing-library/react";
import { within } from "@testing-library/dom";
import FuneralExpensesInfoPage from "./FuneralExpensesInfoPage";

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
  const utils = render(<FuneralExpensesInfoPage />);

  return { ...utils };
}

describe("FuneralExpensesInfoPage", () => {
  it("should render FuneralExpensesInfoPage", () => {
    setup();

    const headline1 = screen.getByText("Bestattungskosten");
    const headline2 = screen.getByText(
      "Beispiele für absetzbare Bestattungskosten"
    );
    const headline3 = screen.getByText("Nicht absetzbare Bestattungskosten");
    const headline4 = screen.getByText("Die zumutbare Belastung");
    const headline5 = screen.getByText(
      "Weitere Ausgaben, die Sie absetzen können"
    );
    const text1 = screen.getByText(
      "Bestattungskosten zählen zur Kategorie der außergewöhnlichen Belastungen",
      { exact: false }
    );

    expect(headline1).toBeInTheDocument();
    expect(headline2).toBeInTheDocument();
    expect(headline3).toBeInTheDocument();
    expect(headline4).toBeInTheDocument();
    expect(headline5).toBeInTheDocument();
    expect(text1).toBeInTheDocument();
  });

  it("should render the list of FuneralExpensesInfoPage", () => {
    setup();

    const list = screen.getByRole("list", {
      name: "simple-list",
    });
    const { getAllByRole } = within(list);
    const items = getAllByRole("listitem");

    expect(items.length).toBe(3);
  });

  it("should render the second list of FuneralExpensesInfoPage", () => {
    setup();

    const list = screen.getByRole("list", {
      name: "simple-list-second",
    });
    const { getAllByRole } = within(list);
    const items = getAllByRole("listitem");

    expect(items.length).toBe(4);
  });

  it("should render the anchor list of FuneralExpensesInfoPage", () => {
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
