import React from "react";
import { render, screen } from "@testing-library/react";
import ShareIcons from "./ShareIcons";

describe("ShareIcons no plausible", () => {
  const MOCK_PROPS_DEFAULT = {
    promoteUrl: "www.google.com",
    shareText: "Hey such an amazing search machine",
    mailSubject: "Did you know it already?",
    sourcePage: "ShareIcons.test",
  };

  beforeEach(() => {
    render(<ShareIcons {...MOCK_PROPS_DEFAULT} />);
  });

  it("should render facebook icon", () => {
    expect(screen.getByLabelText("facebook")).toBeInTheDocument();
  });

  it("should render email icon", () => {
    expect(screen.getByLabelText("email")).toBeInTheDocument();
  });

  it("should not render whatsapp icon", () => {
    expect(screen.queryByLabelText("whatsapp")).not.toBeInTheDocument();
  });
});
