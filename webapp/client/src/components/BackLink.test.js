import React from "react";
import { render, screen } from "@testing-library/react";
import BackLink from "./BackLink";

it("should render the link text", () => {
  render(<BackLink text="Back" url="/some/path" />);
  expect(screen.getByText("Back")).toBeInTheDocument();
});

it("should link to the URL", () => {
  render(<BackLink text="Back" url="/some/path" />);
  expect(screen.getByText("Back").closest("a")).toHaveAttribute(
    "href",
    expect.stringContaining("/some/path")
  );
});
