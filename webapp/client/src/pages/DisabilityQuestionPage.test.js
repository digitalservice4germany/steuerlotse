import React from "react";
import { render, screen } from "@testing-library/react";
import DisabilityQuestionPage from "./DisabilityQuestionPage";
import { Default as StepFormDefault } from "../stories/StepForm.stories";

describe("DisabilityQuestionPage", () => {
  let props;

  beforeEach(() => {
    props = {
      form: {
        ...StepFormDefault.args,
      },
      fields: {
        disabilityExists: "Yes",
      },
      errors: [],
      prevUrl: "prevUrl",
    };
  });

  it("should render selected value yes", () => {
    render(<DisabilityQuestionPage {...props} />);

    expect(screen.queryAllByRole("radio")[0].checked).toBe(true);
    expect(screen.queryAllByRole("radio")[1].checked).toBe(false);
  });

  it("should render selected value no", () => {
    props.fields.disabilityExists = "No";

    render(<DisabilityQuestionPage {...props} />);

    expect(screen.queryAllByRole("radio")[0].checked).toBe(false);
    expect(screen.queryAllByRole("radio")[1].checked).toBe(true);
  });

  it("should render yes and no input", () => {
    render(<DisabilityQuestionPage {...props} />);

    expect(screen.getByText("Ja")).toBeInTheDocument();
    expect(screen.getByText("Nein")).toBeInTheDocument();
  });

  it("should render prev url link", () => {
    render(<DisabilityQuestionPage {...props} />);

    expect(screen.queryAllByRole("link")[0]).toBeInTheDocument();
    expect(screen.queryAllByRole("link")[0].href).toEqual(
      expect.stringContaining(props.prevUrl)
    );
  });
});
