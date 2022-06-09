import React from "react";
import { render, screen } from "@testing-library/react";
import NewsletterSuccessPage from "./NewsletterSuccessPage";

const EXPECTED_HEADER = {
  title:
    "Vielen Dank für Ihre Bestätigung! Sie erhalten nun E-Mails vom Steuerlotsen.",
};

describe("NewsletterSuccessPage", () => {
  it("should render step title text", () => {
    render(<NewsletterSuccessPage />);
    expect(screen.getByText(EXPECTED_HEADER.title)).toBeInTheDocument();
  });
});
