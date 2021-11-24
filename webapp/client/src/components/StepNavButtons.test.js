import React from "react";
import { render, screen } from "@testing-library/react";
import StepNavButtons from "./StepNavButtons";

describe("a StepNavButtons without props", () => {
  beforeEach(() => {
    render(<StepNavButtons />);
  });

  it("should render a button with the default button text", () => {
    expect(screen.getByText("Weiter")).toBeInTheDocument();
    expect(screen.getByText("Weiter").tagName).toEqual("BUTTON");
  });

  it("should not render an overview link", () => {
    expect(screen.queryByText("Zurück zur Übersicht")).not.toBeInTheDocument();
  });
});

describe("a StepNavButtons with a nextButtonLabel", () => {
  beforeEach(() => {
    render(<StepNavButtons nextButtonLabel="neeeeeext" />);
  });

  it("should render a button with the custom button text", () => {
    expect(screen.getByText("neeeeeext")).toBeInTheDocument();
  });
});

describe("a StepNavButtons with an overview button", () => {
  beforeEach(() => {
    render(<StepNavButtons showOverviewButton />);
  });

  it("should render a button to go to the overview", () => {
    expect(screen.getByText("Zurück zur Übersicht")).toBeInTheDocument();
    expect(screen.getByText("Zurück zur Übersicht").tagName).toEqual("BUTTON");
  });
});

describe("a StepNavButtons with an explanatoryButtonText", () => {
  beforeEach(() => {
    render(<StepNavButtons explanatoryButtonText="some text" />);
  });

  it("should render the explanatory button text", () => {
    expect(screen.getByText(/some text/)).toBeInTheDocument();
  });
});
