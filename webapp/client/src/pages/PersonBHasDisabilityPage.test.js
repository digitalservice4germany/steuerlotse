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
        personBHasDisability: {
          value: "yes",
          errors: [],
        },
      },
      prevUrl: "prevUrl",
    };

    render(<PersonBHasDisabilityPage {...props} />);
  });

  it("should render selected value yes", () => {
    expect(screen.queryAllByRole("radio")[0].checked).toBe(true);
    expect(screen.queryAllByRole("radio")[1].checked).toBe(false);
  });

  it("should render yes and no input", () => {
    expect(screen.getByText("Ja")).toBeInTheDocument();
    expect(screen.getByText("Nein")).toBeInTheDocument();
  });

  it("should render prev url link", () => {
    expect(screen.queryAllByRole("link")[0]).toBeInTheDocument();
    expect(screen.queryAllByRole("link")[0].href).toEqual(
      expect.stringContaining(props.prevUrl)
    );
  });

  describe("PersonBHasDisabilityPage no disability", () => {
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
          personBHasDisability: {
            value: "no",
            errors: [],
          },
        },
        prevUrl: "prevUrl",
      };

      render(<PersonBHasDisabilityPage {...props} />);
    });

    it("should render selected value no", () => {
      expect(screen.queryAllByRole("radio")[0].checked).toBe(false);
      expect(screen.queryAllByRole("radio")[1].checked).toBe(true);
    });
  });
});
