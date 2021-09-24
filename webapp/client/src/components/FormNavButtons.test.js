import React from "react";
import { render, screen } from "@testing-library/react";
import FormNavButtons from "./FormNavButtons";

describe("a FormNavButtons without props", () => {
  beforeEach(() => {
    render(<FormNavButtons />);
  });

  it("should render a button with the default button text", () => {
    expect(screen.getByText("Weiter")).toBeInTheDocument();
    expect(screen.getByText("Weiter").tagName).toEqual("BUTTON");
  });

  it("should not render an overview link", () => {
    expect(screen.queryByText("Zurück zur Übersicht")).not.toBeInTheDocument();
  });
});

describe("a FormNavButtons with a nextButtonLabel", () => {
  beforeEach(() => {
    render(<FormNavButtons nextButtonLabel="neeeeeext" />);
  });

  it("should render a button with the custom button text", () => {
    expect(screen.getByText("neeeeeext")).toBeInTheDocument();
  });
});

describe("a FormNavButtons with an overview button", () => {
  beforeEach(() => {
    render(<FormNavButtons showOverviewButton />);
  });

  it("should render a button to go to the overview", () => {
    expect(screen.getByText("Zurück zur Übersicht")).toBeInTheDocument();
    expect(screen.getByText("Zurück zur Übersicht").tagName).toEqual("BUTTON");
  });
});

describe("a FormNavButtons with an explanatoryButtonText", () => {
  beforeEach(() => {
    render(
      <FormNavButtons explanatoryButtonText="some text with <em>HTML tags</em>" />
    );
  });

  it("should render the explanatory button text", () => {
    expect(screen.getByText(/some text/)).toBeInTheDocument();
    expect(screen.getByText(/some text/).innerHTML).toEqual(
      "some text with <em>HTML tags</em>"
    );
  });
});
