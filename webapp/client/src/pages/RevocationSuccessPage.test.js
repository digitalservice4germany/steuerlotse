import React from "react";
import { render, screen } from "@testing-library/react";
import RevocationSuccessPage from "./RevocationSuccessPage";

const props = {
  stepHeader: {
    title: "Title",
    intro: "Intro",
  },
  prevUrl: "/some/prev/path",
  nextUrl: "/some/next/path",
};

it("should render step header texts", () => {
  render(<RevocationSuccessPage {...props} />);
  expect(screen.getByText("Title")).toBeInTheDocument();
  expect(screen.getByText("Intro")).toBeInTheDocument();
});

it("should link to the previous page", () => {
  render(<RevocationSuccessPage {...props} />);
  expect(screen.getByText("Zurück").closest("a")).toHaveAttribute(
    "href",
    expect.stringContaining("/some/prev/path")
  );
});

it("should link to the next page", () => {
  render(<RevocationSuccessPage {...props} />);
  expect(screen.getByText("Weiter").closest("a")).toHaveAttribute(
    "href",
    expect.stringContaining("/some/next/path")
  );
});
