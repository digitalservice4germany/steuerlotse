import React from "react";
import { render, screen } from "@testing-library/react";
import FormHeaderParagraphs from "./FormHeaderParagraphs";

it("should render the title", () => {
  render(<FormHeaderParagraphs title="MyTitle" />);
  expect(screen.getByText("MyTitle")).toBeInTheDocument();
});

it("should render one intro if provided", () => {
  render(
    <FormHeaderParagraphs
      title="MyTitle"
      intros={["All good things come to those who wait"]}
    />
  );
  expect(screen.getByText(/all good things/i)).toBeInTheDocument();
});

it("should render two intros if provided", () => {
  render(
    <FormHeaderParagraphs
      title="MyTitle"
      intros={["All good things come to those who wait", "Violet Fane"]}
    />
  );
  expect(screen.getByText(/all good things/i)).toBeInTheDocument();
  expect(screen.getByText(/Violet Fane/i)).toBeInTheDocument();
});
