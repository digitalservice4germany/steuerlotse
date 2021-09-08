import React from "react";
import { render, screen } from "@testing-library/react";
import FormNavButtons from "./FormNavButtons";

describe("a FormNavButtons without props", () => {
  beforeEach(() => {
    render(<FormNavButtons />);
  });

  it("should render a button with the default button text", () => {
    expect(screen.getByText("form.next")).toBeInTheDocument();
    expect(screen.getByText("form.next").tagName).toEqual("BUTTON");
  });

  it("should not render an overview link", () => {
    expect(screen.queryByText("form.back_to_overview")).not.toBeInTheDocument();
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
    render(<FormNavButtons overviewButton={true} />);
  });

  it("should render a button to go to the overview", () => {
    expect(screen.getByText("form.back_to_overview")).toBeInTheDocument();
    expect(screen.getByText("form.back_to_overview").tagName).toEqual("BUTTON");
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
