import React from "react";
import { render, screen } from "@testing-library/react";
import PersonAHasDisabilityPage from "./PersonAHasDisabilityPage";
import { Default as StepFormDefault } from "../stories/StepForm.stories";

describe("PersonAHasDisabilityPage for single person", () => {
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
        personAHasDisability: {
          value: "yes",
          errors: [],
        },
      },
      prevUrl: "prevUrl",
      numUsers: 1,
    };

    render(<PersonAHasDisabilityPage {...props} />);
  });

  it("should render selected value yes", () => {
    expect(screen.getByDisplayValue("yes").checked).toBe(true);
    expect(screen.getByDisplayValue("no").checked).toBe(false);
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

  it("should render intro_single when numOfUser is 1", () => {
    expect(screen.queryByText(/Person A/)).not.toBeInTheDocument();
  });
});

describe("PersonAHasDisabilityPage no disability", () => {
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
        personAHasDisability: {
          value: "no",
          errors: [],
        },
      },
      prevUrl: "prevUrl",
      numUsers: 1,
    };

    render(<PersonAHasDisabilityPage {...props} />);
  });

  it("should render selected value no", () => {
    expect(screen.getByDisplayValue("yes").checked).toBe(false);
    expect(screen.getByDisplayValue("no").checked).toBe(true);
  });
});

describe("PersonAHasDisabilityPage for joint taxes", () => {
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
        personAHasDisability: {
          value: "yes",
          errors: [],
        },
      },
      prevUrl: "prevUrl",
      numUsers: 2,
    };

    render(<PersonAHasDisabilityPage {...props} />);
  });

  it("should render intro_person_a when numUsers is 2", () => {
    expect(screen.queryByText(/Person A/)).toBeInTheDocument();
  });
});
