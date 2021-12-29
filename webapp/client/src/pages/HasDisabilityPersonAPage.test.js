import React from "react";
import { render, screen } from "@testing-library/react";
import HasDisabilityPersonAPage from "./HasDisabilityPersonAPage";
import { Default as StepFormDefault } from "../stories/StepForm.stories";

describe("HasDisabilityPersonAPage for single person", () => {
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

    render(<HasDisabilityPersonAPage {...props} />);
  });

  it("should render intro_single when numOfUser is 1", () => {
    expect(screen.queryByText(/Person A/)).not.toBeInTheDocument();
  });
});

describe("HasDisabilityPersonAPage for joint taxes", () => {
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

    render(<HasDisabilityPersonAPage {...props} />);
  });

  it("should render intro_person_a when numUsers is 2", () => {
    expect(screen.queryByText(/Person A/)).toBeInTheDocument();
  });
});
