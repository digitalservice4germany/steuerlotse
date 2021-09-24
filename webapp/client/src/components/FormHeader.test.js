import React from "react";
import { render, screen } from "@testing-library/react";
import FormHeader from "./FormHeader";

it("should render the title", () => {
  render(<FormHeader title="MyTitle" />);
  expect(screen.getByText("MyTitle")).toBeInTheDocument();
});

it("should render the intro if provided", () => {
  render(
    <FormHeader
      title="MyTitle"
      intro="All good things come to those who wait"
    />
  );
  expect(screen.getByText(/all good things/i)).toBeInTheDocument();
});

it("should not render the intro if hideIntro is truthy", () => {
  render(
    <FormHeader
      title="MyTitle"
      intro="All good things come to those who wait"
      hideIntro
    />
  );
  expect(screen.queryByText(/all good things/i)).toBeNull();
});
