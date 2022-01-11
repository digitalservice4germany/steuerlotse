import React from "react";
import { render, screen } from "@testing-library/react";
import PauschbetragPage from "./PauschbetragPage";
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
    requestsPauschbetrag: {
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
      name: "requests_pauschbretrag",
    },
  },
  pauschbetrag: "2400",
  prevUrl: "/some/prev/path",
};

describe("With default props", () => {
  beforeEach(() => {
    render(<PauschbetragPage {...props} />);
  });

  it("should render step title text", () => {
    expect(screen.getByText("Title")).toBeInTheDocument();
  });

  it("should ignore field option texts", () => {
    expect(screen.queryByLabelText("Ja")).not.toBeInTheDocument();
    expect(screen.queryByLabelText("Nein")).not.toBeInTheDocument();
  });

  it("should render fields", () => {
    expect(screen.getByDisplayValue("yes")).toBeInTheDocument();
    expect(screen.getByDisplayValue("no")).toBeInTheDocument();
  });

  it("should show pauschbetrag value in option yes text", () => {
    expect(
      screen.getByLabelText(
        `Pauschbetrag in Höhe von ${props.pauschbetrag} Euro beantragen`
      )
    ).toHaveAttribute("value", "yes");
  });

  it("should link to the previous page", () => {
    expect(screen.getByText("Zurück").closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining("/some/prev/path")
    );
  });
});

describe("With yes preselected", () => {
  beforeEach(() => {
    let yesProps = {
      ...props,
      fields: {
        requestsPauschbetrag: {
          selectedValue: "yes",
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
          name: "requests_pauschbretrag",
        },
      },
    };
    render(<PauschbetragPage {...yesProps} />);
  });
  it("should render selected value yes", () => {
    expect(screen.getByDisplayValue("yes").checked).toBe(true);
    expect(screen.getByDisplayValue("no").checked).toBe(false);
  });
});

describe("With no preselected", () => {
  beforeEach(() => {
    let noProps = {
      ...props,
      fields: {
        requestsPauschbetrag: {
          selectedValue: "no",
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
          name: "requests_pauschbretrag",
        },
      },
    };
    render(<PauschbetragPage {...noProps} />);
  });
  it("should render selected value no", () => {
    expect(screen.getByDisplayValue("yes").checked).toBe(false);
    expect(screen.getByDisplayValue("no").checked).toBe(true);
  });
});
