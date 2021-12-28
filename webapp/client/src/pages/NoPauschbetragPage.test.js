import React from "react";
import { render, screen } from "@testing-library/react";
import NoPauschbetragPage from "./NoPauschbetragPage";
import { Default as StepFormDefault } from "../stories/StepForm.stories";

let props = {
  stepHeader: {
    title: "Title",
    intro: "Intro",
  },
  prevUrl: "/some/prev/path",
  nextUrl: "/some/next/path",
};

it("should render step header title", () => {
  render(<NoPauschbetragPage {...props} />);
  expect(screen.getByText("Title")).toBeInTheDocument();
});

it("should ignore step header intro", () => {
  render(<NoPauschbetragPage {...props} />);
  expect(screen.queryByText("Intro")).not.toBeInTheDocument();
});

it("should link to the previous page", () => {
  render(<NoPauschbetragPage {...props} />);
  expect(screen.getByText("Zurück").closest("a")).toHaveAttribute(
    "href",
    expect.stringContaining("/some/prev/path")
  );
});

it("should link to the next page", () => {
  render(<NoPauschbetragPage {...props} />);
  expect(screen.getByText("Weiter").closest("a")).toHaveAttribute(
    "href",
    expect.stringContaining("/some/next/path")
  );
});
