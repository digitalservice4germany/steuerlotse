import React from "react";
import { render, screen } from "@testing-library/react";
import { within } from "@testing-library/dom";
import KrankheitsKostenInfoPage from "./KrankheitsKostenInfoPage";

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

const REQUIRED_PROPS = {
  fscRequestUrl: "url/some/link/path",
};

function setup() {
  const utils = render(<KrankheitsKostenInfoPage {...REQUIRED_PROPS} />);

  return { ...utils };
}

describe("KrankheitsKostenInfoPage", () => {
  it("should render KrankheitsKostenInfoPage", () => {
    setup();

    const headline1 = screen.getByText("Krankheitskosten");
    const headline2 = screen.getByText(
      "Beispiele für absetzbare Krankheitskosten"
    );
    const headline3 = screen.getByText("Nachweise");
    const headline4 = screen.getByText("Die zumutbare Belastung");
    const text1 = screen.getByText(
      "Krankheitskosten sind durch Krankheit verursachte besondere Kosten und gehören",
      { exact: false }
    );

    expect(headline1).toBeInTheDocument();
    expect(headline2).toBeInTheDocument();
    expect(headline3).toBeInTheDocument();
    expect(headline4).toBeInTheDocument();
    expect(text1).toBeInTheDocument();
  });

  it("should render the list of KrankheitsKostenInfoPage", () => {
    setup();

    const list = screen.getByRole("list", {
      name: "simple-list",
    });
    const { getAllByRole } = within(list);
    const items = getAllByRole("listitem");

    expect(items.length).toBe(6);
  });

  it("should render the anchor list of KrankheitsKostenInfoPage", () => {
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
