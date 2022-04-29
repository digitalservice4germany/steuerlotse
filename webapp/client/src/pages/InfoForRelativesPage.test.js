import React from "react";
import { render, screen } from "@testing-library/react";
import { within } from "@testing-library/dom";
import InfoForRelativesPage from "./InfoForRelativesPage";

jest.mock("../components/InfoBox", () => ({
  __esModule: true,
  default: function InfoBox() {
    return <div>info box</div>;
  },
}));

function setup() {
  const utils = render(<InfoForRelativesPage />);

  return { ...utils };
}

describe("InfoForRelativesPage", () => {
  it("should render InfoForRelativesPage", () => {
    setup();

    const headline1 = screen.getByText(
      "Hilfestellung für Angehörige bei der Steuererklärung"
    );
    const headline2 = screen.getByText(
      "Wem Sie helfen dürfen und wer Ihnen helfen darf:"
    );
    const headline3 = screen.getByText(
      "Wer nicht bei der Steuererklärunge helfen darf"
    );
    const text1 = screen.getByText(
      "Wir erklären Ihnen, wer helfen darf und wer nicht. Dass sich Angehörige ohne Bezahlung gegenseitig bei der Steuererklärung helfen, erlaubt sogar das sonst so strenge Steuerberatungsgesetz",
      { exact: false }
    );

    expect(headline1).toBeInTheDocument();
    expect(headline2).toBeInTheDocument();
    expect(headline3).toBeInTheDocument();
    expect(text1).toBeInTheDocument();
  });

  it("should render the list of InfoForRelativesPage", () => {
    setup();

    const list = screen.getByRole("list", {
      name: "simple-list",
    });
    const { getAllByRole } = within(list);
    const items = getAllByRole("listitem");

    expect(items.length).toBe(9);
  });

  it("should render the info box component", () => {
    setup();

    expect(screen.getByText("info box")).toBeInTheDocument();
  });
});
