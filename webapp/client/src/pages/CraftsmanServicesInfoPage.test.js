import React from "react";
import { render, screen } from "@testing-library/react";
import { within } from "@testing-library/dom";
import MedicalExpensesInfoPage from "./MedicalExpensesInfoPage";
import CraftsmanServicesInfoPage from "./CraftsmanServicesInfoPage";

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
  const utils = render(<CraftsmanServicesInfoPage />);

  return { ...utils };
}

describe("CraftsmanServicesInfoPage", () => {
  it("should render CraftsmanServicesInfoPage", () => {
    setup();

    const headline1 = screen.getByText("Handwerkerleistungen");
    const headline2 = screen.getByText("Beispiele für Handwerkerleistungen");
    const headline3 = screen.getByText("Rechnungen und Zahlungsweg beachten");
    const headline5 = screen.getByText(
      "Weitere Ausgaben, die Sie absetzen können"
    );
    const text1 = screen.getByText(
      "Auch Kosten für Dienstleistungen im eigenen Haushalt oder Handwerkerleistungen im eigenen Haushalt können",
      { exact: false }
    );

    expect(headline1).toBeInTheDocument();
    expect(headline2).toBeInTheDocument();
    expect(headline3).toBeInTheDocument();
    expect(headline5).toBeInTheDocument();
    expect(text1).toBeInTheDocument();
  });

  it("should render the list of CraftsmanServicesInfoPage", () => {
    setup();

    const list = screen.getByRole("list", {
      name: "simple-list",
    });
    const { getAllByRole } = within(list);
    const items = getAllByRole("listitem");

    expect(items.length).toBe(9);
  });

  it("should render the anchor list of CraftsmanServicesInfoPage", () => {
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
