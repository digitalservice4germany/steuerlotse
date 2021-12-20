import React from "react";
import { render, screen } from "@testing-library/react";
import PauschbetragPersonBPage from "./PauschbetragPersonBPage";
import { Default as StepFormDefault } from "../stories/StepForm.stories";

let props = {
  stepHeader: {
    title: "Title",
    intro: "Intro",
  },
  form: {
    ...StepFormDefault.args,
  },
  fields: {
    personBWantsPauschbetrag: {
      selectedValue: undefined,
      options: [
        {
          value: "yes",
          displayName: "Ja",
        },
        {
          value: "no",
          displayName: "Nein",
        },
      ],
      errors: [],
    },
  },
  prevUrl: "/some/prev/path",
};

describe("With default props", () => {
  beforeEach(() => {
    render(<PauschbetragPersonBPage {...props} />);
  });

  it("should render step title text", () => {
    expect(screen.getByText("Title")).toBeInTheDocument();
  });

  it("should ignore step intro text", () => {
    expect(screen.queryByText("Intro")).not.toBeInTheDocument();
  });

  it("should render field", () => {
    expect(screen.getByLabelText("Ja")).toBeInTheDocument();
    expect(screen.getByLabelText("Nein")).toBeInTheDocument();
  });

  it("should link to the previous page", () => {
    expect(screen.getByText("Zurück").closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining("/some/prev/path")
    );
  });
});
