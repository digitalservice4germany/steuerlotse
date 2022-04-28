import React from "react";
import { render, screen } from "@testing-library/react";
import { within } from "@testing-library/dom";
import HouseholdServicesInfoPage from "./HouseholdServicesInfoPage";

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
  const utils = render(<HouseholdServicesInfoPage />);

  return { ...utils };
}

describe("HouseholdServicesInfoPage", () => {
  it("should render HouseholdServicesInfoPage", () => {
    setup();

    const headline1 = screen.getByText("Haushaltsnahe Dienstleistungen");
    const headline2 = screen.getByText(
      "Beispiele für Haushaltsnahe Dienstleistungen"
    );
    const headline3 = screen.getByText(
      "Haushaltsnahe Dienstleistungen aus der Nebenkostenabrechnung"
    );
    const headline4 = screen.getByText(
      "Weitere Ausgaben, die Sie absetzen können"
    );
    const text1 = screen.getByText(
      "Auch Kosten für Dienstleistungen im eigenen Haushalt können zu Steuerermäßigungen führen",
      { exact: false }
    );

    expect(headline1).toBeInTheDocument();
    expect(headline2).toBeInTheDocument();
    expect(headline3).toBeInTheDocument();
    expect(headline4).toBeInTheDocument();
    expect(text1).toBeInTheDocument();
  });

  it("should render the list of Household Services on the HouseholdServicesInfoPage", () => {
    setup();

    const list = screen.getByRole("list", {
      name: "simple-list",
    });
    const { getAllByRole } = within(list);
    const items = getAllByRole("listitem");

    expect(items.length).toBe(8);
  });

  it("should render the anchor list of HouseholdServicesInfoPage", () => {
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
