import React from "react";
import { render, screen } from "@testing-library/react";
import { within } from "@testing-library/dom";
import MerkzeichenPersonAPage from "./MerkzeichenPersonAPage";
import { Default as StepFormDefault } from "../stories/StepForm.stories";

describe("MerkzeichenPersonAPage default", () => {
  let props = {
    stepHeader: {
      title: "Title",
      intro: "Intro",
    },
    form: {
      ...StepFormDefault.args,
    },
    fields: {
      personAHasPflegegrad: {
        value: "",
        errors: [],
      },
      personADisabilityDegree: {
        value: "",
        errors: [],
      },
      personAHasMerkzeichenH: {
        checked: false,
        errors: [],
      },
      personAHasMerkzeichenG: {
        checked: false,
        errors: [],
      },
      personAHasMerkzeichenBl: {
        checked: false,
        errors: [],
      },
      personAHasMerkzeichenTbl: {
        checked: false,
        errors: [],
      },
      personAHasMerkzeichenAg: {
        checked: false,
        errors: [],
      },
    },
    prevUrl: "/some/prev/path",
  };

  beforeEach(() => {
    render(<MerkzeichenPersonAPage {...props} />);
  });

  it("should render step header texts", () => {
    expect(screen.getByText("Title")).toBeInTheDocument();
    expect(screen.getByText("Intro")).toBeInTheDocument();
  });

  it("should render pflegegrad field", () => {
    const fieldset = screen.getByRole("group", { name: /Pflegegrad/ });
    expect(within(fieldset).getByLabelText("Ja")).toBeInTheDocument();
    expect(within(fieldset).getByLabelText("Nein")).toBeInTheDocument();
  });

  it("should render disability degree field", () => {
    expect(
      screen.getByLabelText("Grad der Behinderung", { exact: false })
    ).toBeInTheDocument();
  });

  it("should show merkzeichen within fieldset", () => {
    const fieldset = screen.getByRole("group", { name: "Merkzeichen" });
    expect(
      within(fieldset).getByLabelText("Merkzeichen G")
    ).toBeInTheDocument();
    expect(
      within(fieldset).getByLabelText("Merkzeichen aG")
    ).toBeInTheDocument();
    expect(
      within(fieldset).getByLabelText("Merkzeichen Bl")
    ).toBeInTheDocument();
    expect(
      within(fieldset).getByLabelText("Merkzeichen TBl")
    ).toBeInTheDocument();
    expect(
      within(fieldset).getByLabelText("Merkzeichen H")
    ).toBeInTheDocument();
  });

  it("should link to the previous page", () => {
    expect(screen.getByText("Zurück").closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining("/some/prev/path")
    );
  });
});
