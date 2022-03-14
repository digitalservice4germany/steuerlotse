import React from "react";
import { render, screen } from "@testing-library/react";
import ShareIcons from "./ShareIcons";
import userEvent from "@testing-library/user-event";

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

describe("ShareIcons with plausible", () => {
  const MOCK_PROPS_PLAUSIBLE = {
    promoteUrl: "www.google.com",
    shareText: "Hey such an amazing search machine",
    mailSubject: "Did you know it already?",
    sourcePage: "ShareIcons.test",
    plausibleDomain: "http://localhost:3000",
  };

  beforeEach(() => {
    window.plausible = jest.fn().mockReturnValue({ plausible: jest.fn() });
    render(<ShareIcons {...MOCK_PROPS_PLAUSIBLE} />);
  });

  it("should add plausible goal for facebook icon", () => {
    userEvent.click(screen.getByLabelText("facebook"));
    expect(window.plausible).toHaveBeenCalledWith("Facebook icon clicked", {
      method: MOCK_PROPS_PLAUSIBLE.sourcePage,
    });
  });

  it("should add plausible goal for email icon", () => {
    userEvent.click(screen.getByLabelText("email"));
    expect(window.plausible).toHaveBeenCalledWith("Email icon clicked", {
      method: MOCK_PROPS_PLAUSIBLE.sourcePage,
    });
  });
});
