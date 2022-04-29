import React from "react";
import { render, screen } from "@testing-library/react";
import { within } from "@testing-library/dom";
import DisabilityCostsInfoPage from "./DisabilityCostsInfoPage";

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
  const utils = render(<DisabilityCostsInfoPage />);

  return { ...utils };
}

describe("DisabilityCostsInfoPage", () => {
  it("should render the DisabilityCostsInfoPage", () => {
    setup();

    const headline1 = screen.getByText("Kosten bei einer Behinderung");
    const headline2 = screen.getByText(
      "Wahl zwischen Pauschbetrag und Angabe Einzelkosten"
    );
    const headline3 = screen.getByText(
      "Pauschbetrag für Menschen mit Behinderung"
    );
    const headline4 = screen.getByText(
      "Einige Beispiele für Kosten aufgrund einer Behinderung"
    );
    const headline5 = screen.getByText("Die zumutbare Belastung");
    const headline6 = screen.getByText(
      "Die behinderungsbedingte Fahrtkostenpauschale"
    );
    const headline7 = screen.getByText("Nachweise");
    const headline8 = screen.getByText(
      "Weitere Ausgaben, die Sie absetzen können"
    );

    const text1 = screen.getByText(
      "Im Falle einer Behinderung oder Pflegebedürftigkeit können erhöhte Kosten für Medikamente und Betreuung anfallen",
      { exact: false }
    );

    expect(headline1).toBeInTheDocument();
    expect(headline2).toBeInTheDocument();
    expect(headline3).toBeInTheDocument();
    expect(headline4).toBeInTheDocument();
    expect(headline5).toBeInTheDocument();
    expect(headline6).toBeInTheDocument();
    expect(headline7).toBeInTheDocument();
    expect(headline8).toBeInTheDocument();
    expect(text1).toBeInTheDocument();
  });

  it("should render the list of Lump sum for people with disabilities on the DisabilityCostsInfoPage", () => {
    setup();

    const list = screen.getByRole("list", {
      name: "first-list",
    });
    const { getAllByRole } = within(list);
    const items = getAllByRole("listitem");

    expect(items.length).toBe(3);
  });

  it("should render the list of examples of disability costs on the DisabilityCostsInfoPage", () => {
    setup();

    const list = screen.getByRole("list", {
      name: "second-list",
    });
    const { getAllByRole } = within(list);
    const items = getAllByRole("listitem");

    expect(items.length).toBe(4);
  });

  it("should render the anchors list on the DisabilityCostsInfoPage", () => {
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
