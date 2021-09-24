import React from "react";
import { render, screen } from "@testing-library/react";
import FormFieldScaffolding from "./FormFieldScaffolding";

describe("FormFieldScaffolding", () => {
  let props;

  beforeEach(() => {
    props = {
      fieldName: "foo",
      render: () => {},
      labelComponent: <>my label</>,
    };
  });

  it("should show the label by default", () => {
    render(<FormFieldScaffolding {...props} />);
    expect(screen.getByText("my label")).toBeInTheDocument();
  });

  it("should hide the label if hideLabel is set", () => {
    render(<FormFieldScaffolding {...props} hideLabel />);
    expect(screen.queryByText("my label")).not.toBeInTheDocument();
  });

  describe("with errors", () => {
    beforeEach(() => {
      props.errors = ["something wrong"];
    });

    it("should show errors by default", () => {
      render(<FormFieldScaffolding {...props} />);
      expect(screen.getByText("something wrong")).toBeInTheDocument();
    });

    it("should hide errors if hideErrors is set", () => {
      render(<FormFieldScaffolding {...props} hideErrors />);
      expect(screen.queryByText("something wrong")).not.toBeInTheDocument();
    });
  });
});
