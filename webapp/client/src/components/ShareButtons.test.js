import React from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import ShareButtons from "./ShareButtons";

describe("ShareIcons no plausible", () => {
  const MOCK_PROPS_DEFAULT = {
    promoteUrl: "www.google.com",
    shareText: "Hey such an amazing search machine",
    mailSubject: "Did you know it already?",
    sourcePage: "ShareIcons.test",
  };

  beforeEach(() => {
    render(<ShareButtons {...MOCK_PROPS_DEFAULT} />);
  });

  it("should render facebook button", () => {
    expect(screen.getByText("Auf Facebook teilen")).toBeInTheDocument();
  });

  it("should render email button", () => {
    expect(screen.getByText("E-Mail schreiben")).toBeInTheDocument();
  });

  it("should render copy button", () => {
    expect(screen.getByText("Link kopieren")).toBeInTheDocument();
  });

  it("should not render whatsapp button", () => {
    expect(screen.queryByText("In Whatsapp senden")).not.toBeInTheDocument();
  });
});

describe("ShareIcons with plausible", () => {
  const user = userEvent.setup();
  const MOCK_PROPS_PLAUSIBLE = {
    promoteUrl: "www.google.com",
    shareText: "Hey such an amazing search machine",
    mailSubject: "Did you know it already?",
    sourcePage: "ShareIcons.test",
    plausibleDomain: "http://localhost:3000",
  };

  beforeEach(() => {
    window.plausible = jest.fn();
    render(<ShareButtons {...MOCK_PROPS_PLAUSIBLE} />);
  });

  it("should add plausible goal for facebook icon", async () => {
    await user.click(screen.getByText("Auf Facebook teilen"));

    expect(window.plausible).toHaveBeenCalledWith("Facebook icon clicked", {
      method: MOCK_PROPS_PLAUSIBLE.sourcePage,
    });
  });

  it("should add plausible goal for email icon", async () => {
    await user.click(screen.getByText("E-Mail schreiben"));

    expect(window.plausible).toHaveBeenCalledWith("Email icon clicked", {
      method: MOCK_PROPS_PLAUSIBLE.sourcePage,
    });
  });
});
