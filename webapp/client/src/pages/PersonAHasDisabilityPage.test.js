import React from "react";
import { render, screen } from "@testing-library/react";
import PersonAHasDisabilityPage from "./PersonAHasDisabilityPage";
import { Default as StepFormDefault } from "../stories/StepForm.stories";

describe("PersonAHasDisabilityPage", () => {
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
        personA_hasDisability: {
          value: "yes",
          errors: [],
        },
      },
      prevUrl: "prevUrl",
      numOfUsers: 1,
    };
  });

  it("should render selected value yes", () => {
    render(<PersonAHasDisabilityPage {...props} />);

    expect(screen.queryAllByRole("radio")[0].checked).toBe(true);
    expect(screen.queryAllByRole("radio")[1].checked).toBe(false);
  });

  it("should render selected value no", () => {
    props.fields.personA_hasDisability.value = "no";

    render(<PersonAHasDisabilityPage {...props} />);

    expect(screen.queryAllByRole("radio")[0].checked).toBe(false);
    expect(screen.queryAllByRole("radio")[1].checked).toBe(true);
  });

  it("should render yes and no input", () => {
    render(<PersonAHasDisabilityPage {...props} />);

    expect(screen.getByText("Ja")).toBeInTheDocument();
    expect(screen.getByText("Nein")).toBeInTheDocument();
  });

  it("should render prev url link", () => {
    render(<PersonAHasDisabilityPage {...props} />);

    expect(screen.queryAllByRole("link")[0]).toBeInTheDocument();
    expect(screen.queryAllByRole("link")[0].href).toEqual(
      expect.stringContaining(props.prevUrl)
    );
  });

  it("should render intro_1 when numOfUser is 1", () => {
    render(<PersonAHasDisabilityPage {...props} />);

    expect(screen.queryByText(/Person A/)).not.toBeInTheDocument();
  });

  it("should render intro_2 when numOfUser is 2", () => {
    props.numOfUsers = 2;
    render(<PersonAHasDisabilityPage {...props} />);

    expect(screen.queryByText(/Person A/)).toBeInTheDocument();
  });
});
