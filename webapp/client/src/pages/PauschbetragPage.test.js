import React from "react";
import { render, screen } from "@testing-library/react";
import PauschbetragPersonAPage from "./PauschbetragPersonAPage";
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
    personAWantsPauschbetrag: {
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
      name: "wants_pauschbretrag",
    },
  },
  prevUrl: "/some/prev/path",
};

describe("With default props", () => {
  beforeEach(() => {
    render(<PauschbetragPersonAPage {...props} />);
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
