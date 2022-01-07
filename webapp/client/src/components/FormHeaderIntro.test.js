import React from "react";
import { render, screen } from "@testing-library/react";
import FormHeaderIntro from "./FormHeaderIntro";

it("should render one intro if provided", () => {
  render(
    <FormHeaderIntro paragraphs={["All good things come to those who wait"]} />
  );
  expect(screen.getByText(/all good things/i)).toBeInTheDocument();
});

it("should render two paragraphs if provided", () => {
  render(
    <FormHeaderIntro
      paragraphs={["All good things come to those who wait", "Violet Fane"]}
    />
  );
  expect(screen.getByText(/all good things/i)).toBeInTheDocument();
  expect(screen.getByText(/Violet Fane/i)).toBeInTheDocument();
});
