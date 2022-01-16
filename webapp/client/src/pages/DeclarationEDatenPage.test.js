import React from "react";
import { render, screen } from "@testing-library/react";
import DeclarationEDatenPage from "./DeclarationEDatenPage";
import { Default as StepFormDefault } from "../stories/StepForm.stories";

import { configure } from "@testing-library/dom";
configure({ testIdAttribute: "id" });

const defaultProps = {
  stepHeader: {
    title: "Title",
  },
  form: {
    ...StepFormDefault.args,
  },
  fields: {
    declarationEdaten: {
      checked: false,
      errors: [],
    },
  },
};

describe("DeclarationEDatenPage default", () => {
  let renderContainer;

  beforeEach(() => {
    renderContainer = render(<DeclarationEDatenPage {...defaultProps} />);
  });

  it("should render step title text", () => {
    expect(screen.getByText("Title")).toBeInTheDocument();
  });

  it("should render checked value false", () => {
    expect(screen.getByTestId("declaration_edaten").checked).toBe(false);
  });
});

const checkedProps = {
  stepHeader: {
    title: "title",
  },
  form: {
    ...StepFormDefault.args,
  },
  fields: {
    declarationEdaten: {
      checked: true,
      errors: [],
    },
  },
};

describe("With checked checkbox", () => {
  beforeEach(() => {
    render(<DeclarationEDatenPage {...checkedProps} />);
  });

  it("should render checked value true", () => {
    expect(screen.getByTestId("declaration_edaten").checked).toBe(true);
  });
});

const errorProps = {
  stepHeader: {
    title: "title",
  },
  form: {
    ...StepFormDefault.args,
  },
  fields: {
    declarationEdaten: {
      checked: false,
      errors: ["Error1"],
    },
  },
};

describe("With error value", () => {
  beforeEach(() => {
    render(<DeclarationEDatenPage {...errorProps} />);
  });

  it("should render error value", () => {
    expect(screen.getByText("Error1")).toBeInTheDocument();
  });
});
