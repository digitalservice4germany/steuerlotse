import React from "react";
import { render, screen } from "@testing-library/react";
import { within } from "@testing-library/dom";
import DonationInfoPage from "./DonationInfoPage";

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
  const utils = render(<DonationInfoPage />);

  return { ...utils };
}

describe("DonationInfoPage", () => {
  it("should render DonationInfoPage", () => {
    setup();

    const headline1 = screen.getByText("Spenden und Mitgliedsbeiträge");
    const headline2 = screen.getByText(
      "Spenden und Beiträge für steuerbegünstigte Zwecke"
    );
    const headline3 = screen.getByText("Spenden an politische Parteien");
    const headline4 = screen.getByText("Nachweise");

    const headline5 = screen.getByText(
      "Weitere Ausgaben, die Sie absetzen können"
    );
    const text1 = screen.getByText(
      "Spenden und Mitgliedsbeiträge können als Sonderausgaben abgesetzt werden. Wir erklären, wie Sie Spenden absetzen können.",
      { exact: false }
    );

    expect(headline1).toBeInTheDocument();
    expect(headline2).toBeInTheDocument();
    expect(headline3).toBeInTheDocument();
    expect(headline4).toBeInTheDocument();
    expect(headline5).toBeInTheDocument();
    expect(text1).toBeInTheDocument();
  });

  it("should render the list of DonationInfoPage", () => {
    setup();

    const list = screen.getByRole("list", {
      name: "simple-list",
    });
    const { getAllByRole } = within(list);
    const items = getAllByRole("listitem");

    expect(items.length).toBe(5);
  });

  it("should render the 2th list of DonationInfoPage", () => {
    setup();

    const list = screen.getByRole("list", {
      name: "simple-list-second",
    });
    const { getAllByRole } = within(list);
    const items = getAllByRole("listitem");

    expect(items.length).toBe(5);
  });

  it("should render the anchor list of DonationInfoPage", () => {
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
