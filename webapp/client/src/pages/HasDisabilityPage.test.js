import React from "react";
import { render, screen } from "@testing-library/react";
import HasDisabilityPage from "./HasDisabilityPage";
import { Default as StepFormDefault } from "../stories/StepForm.stories";

describe("HasDisabilityPage for single person", () => {
  let props;

  beforeEach(() => {
    props = {
      stepHeader: {
        title: "title",
      },
      headerIntro: "Intro",
      form: {
        ...StepFormDefault.args,
      },
      fields: {
        hasDisability: {
          value: "yes",
          errors: [],
          name: "has_disability",
        },
      },
      prevUrl: "prevUrl",
      numUsers: 1,
    };

    render(<HasDisabilityPage {...props} />);
  });

  it("should render title", () => {
    expect(screen.getByText("title")).toBeInTheDocument();
  });

  it("should render headerIntro", () => {
    expect(screen.getByText("Intro")).toBeInTheDocument();
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
});

describe("HasDisabilityPage no disability", () => {
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
        hasDisability: {
          value: "no",
          errors: [],
          name: "has_disability",
        },
      },
      prevUrl: "prevUrl",
      numUsers: 1,
    };

    render(<HasDisabilityPage {...props} />);
  });

  it("should render selected value no", () => {
    expect(screen.queryAllByRole("radio")[0].checked).toBe(false);
    expect(screen.queryAllByRole("radio")[1].checked).toBe(true);
  });
});
