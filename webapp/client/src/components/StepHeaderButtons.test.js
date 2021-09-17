import React from "react";
import { render, screen } from "@testing-library/react";
import StepHeaderButtons from "./StepHeaderButtons";

it("should render a back link", () => {
  render(<StepHeaderButtons backLinkUrl="/back" backLinkText="return" />);
  expect(screen.getByText("return")).toBeInTheDocument();
});

it("should be empty if no backLinkUrl is given", () => {
  render(<StepHeaderButtons />);
  expect(screen.queryByText("return")).toBeNull();
});
