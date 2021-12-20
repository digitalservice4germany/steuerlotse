import React from "react";
import { render, screen } from "@testing-library/react";
import PersonBHasDisabilityPage from "./PersonBHasDisabilityPage";
import { Default as StepFormDefault } from "../stories/StepForm.stories";

describe("PersonBHasDisabilityPage", () => {
  let props;

  beforeEach(() => {
    props = {
      stepHeader: {
        title: "title",
      },
      form: {
        ...StepFormDefault.args,
      },
      fields: {
        personB_hasDisability: {
          value: "yes",
          errors: [],
        },
      },
      prevUrl: "prevUrl",
    };
  });

  it("should render selected value yes", () => {
    render(<PersonBHasDisabilityPage {...props} />);

    expect(screen.queryAllByRole("radio")[0].checked).toBe(true);
    expect(screen.queryAllByRole("radio")[1].checked).toBe(false);
  });

  it("should render selected value no", () => {
    props.fields.personB_hasDisability.value = "no";

    render(<PersonBHasDisabilityPage {...props} />);

    expect(screen.queryAllByRole("radio")[0].checked).toBe(false);
    expect(screen.queryAllByRole("radio")[1].checked).toBe(true);
  });

  it("should render yes and no input", () => {
    render(<PersonBHasDisabilityPage {...props} />);

    expect(screen.getByText("Ja")).toBeInTheDocument();
    expect(screen.getByText("Nein")).toBeInTheDocument();
  });

  it("should render prev url link", () => {
    render(<PersonBHasDisabilityPage {...props} />);

    expect(screen.queryAllByRole("link")[0]).toBeInTheDocument();
    expect(screen.queryAllByRole("link")[0].href).toEqual(
      expect.stringContaining(props.prevUrl)
    );
  });
});
