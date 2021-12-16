import React from "react";
import { render, screen } from "@testing-library/react";
import DisabilityQuestionPage from "./DisabilityQuestionPage";
import { Default as StepFormDefault } from "../stories/StepForm.stories";

describe("DisabilityQuestionPage", () => {
  let props;

  beforeEach(() => {
    props = {
      stepHeader: {
        title: "stepHeader.title",
        intro: "stepHeader.intro",
      },
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

  it("should render step header texts", () => {
    render(<DisabilityQuestionPage {...props} />);

    expect(screen.queryByText("stepHeader.title")).toBeInTheDocument();
    expect(screen.queryByText("stepHeader.intro")).toBeInTheDocument();
  });

  it("should render step yes value", () => {
    render(<DisabilityQuestionPage {...props} />);

    expect(screen.queryAllByRole("radio")[0].checked).toBe(true);
    expect(screen.queryAllByRole("radio")[1].checked).toBe(false);
  });

  it("should render step no value", () => {
    props.fields.disabilityExists = "No";

    render(<DisabilityQuestionPage {...props} />);

    expect(screen.queryAllByRole("radio")[0].checked).toBe(false);
    expect(screen.queryAllByRole("radio")[1].checked).toBe(true);
  });

  it("should render yes no input", () => {
    render(<DisabilityQuestionPage {...props} />);

    expect(screen.getByText("Ja")).toBeInTheDocument();
    expect(screen.getByText("Nein")).toBeInTheDocument();
  });

  it("should render yes no input", () => {
    render(<DisabilityQuestionPage {...props} />);

    expect(screen.queryAllByRole("link")[0]).toBeInTheDocument();
    expect(screen.queryAllByRole("link")[0].href).toEqual(
      expect.stringContaining(props.prevUrl)
    );
  });
});
