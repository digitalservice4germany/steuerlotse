import React from "react";
import { render, screen } from "@testing-library/react";
import { within } from "@testing-library/dom";
import PensionExpensesInfoPage from "./PensionExpensesInfoPage";

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
  const utils = render(<PensionExpensesInfoPage />);

  return { ...utils };
}

describe("PensionExpensesInfoPage", () => {
  it("should render the PensionExpensesInfoPage", () => {
    setup();

    const headline1 = screen.getByText("Vorsorgeaufwendungen");
    const headline2 = screen.getByText(
      "Beispiele für absetzbare Versicherungen als Vorsorgeaufwendungen"
    );
    const headline3 = screen.getByText("Nicht absetzbare Versicherungen");
    const headline4 = screen.getByText(
      "Weitere Ausgaben, die Sie absetzen können"
    );
    const text1 = screen.getByText(
      "Viele Versicherungen, mit denen Sie für Ihre Zukunft vorsorgen, können Sie von der Steuer absetzen",
      { exact: false }
    );

    expect(headline1).toBeInTheDocument();
    expect(headline2).toBeInTheDocument();
    expect(headline3).toBeInTheDocument();
    expect(headline4).toBeInTheDocument();
    expect(text1).toBeInTheDocument();
  });

  it("should render the list of deductable insurance on the PensionExpensesInfoPage", () => {
    setup();

    const list = screen.getByRole("list", {
      name: "first-list",
    });
    const { getAllByRole } = within(list);
    const items = getAllByRole("listitem");

    expect(items.length).toBe(6);
  });

  it("should render the list of non-deductable insurance on the PensionExpensesInfoPage", () => {
    setup();

    const list = screen.getByRole("list", {
      name: "second-list",
    });
    const { getAllByRole } = within(list);
    const items = getAllByRole("listitem");

    expect(items.length).toBe(4);
  });

  it("should render the anchor list of PensionExpensesInfoPage", () => {
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
