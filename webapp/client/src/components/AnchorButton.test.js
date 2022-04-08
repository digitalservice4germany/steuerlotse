import React from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import AnchorButton from "./AnchorButton";

const REQUIRED_PROPS = {
  text: "anchor text",
  url: "url/some/link/path",
};

function setup(optionalProps) {
  const utils = render(<AnchorButton {...REQUIRED_PROPS} {...optionalProps} />);
  const buttonText = screen.getByText("anchor text");

  return { ...utils, buttonText };
}

describe("AnchorButton", () => {
  it("should render the button text", () => {
    setup();

    expect(screen.getByText(REQUIRED_PROPS.text)).toBeInTheDocument();
  });

  it("should have a href attribute", () => {
    const { buttonText } = setup();

    expect(buttonText.closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(REQUIRED_PROPS.url)
    );
  });

  it("should not have a download attribute if isDownloadLink is false", () => {
    const { buttonText } = setup({
      isDownloadLink: false,
    });

    expect(buttonText.closest("a")).not.toHaveAttribute("download");
  });

  it("should have a download attribute if isDownloadLink is true", () => {
    const { buttonText } = setup({
      isDownloadLink: true,
    });

    expect(buttonText.closest("a")).toHaveAttribute("download");
  });
});

describe("AnchorButton with plausible", () => {
  it("should call plausible with goal", () => {
    const { buttonText } = setup({
      plausibleDomain: "domain/some/link/path",
      plausibleGoal: "plausible_goal",
    });
    const EXPECTED_PLAUSIBLE_GOAL = "plausible_goal";

    window.plausible = jest.fn().mockReturnValue({ plausible: jest.fn() });

    userEvent.click(buttonText);

    expect(window.plausible).toHaveBeenCalledWith(EXPECTED_PLAUSIBLE_GOAL, {
      props: undefined,
    });
  });

  it("should call plausible with goal and props", async () => {
    const { buttonText } = setup({
      plausibleDomain: "domain/some/link/path",
      plausibleGoal: "plausible_goal",
      plausibleProps: { method: "unlockCodeSuccess" },
    });
    const EXPECTED_PLAUSIBLE_GOAL = "plausible_goal";
    const EXPECTED_PLAUSIBLE_PROPS = { props: { method: "unlockCodeSuccess" } };

    window.plausible = jest.fn().mockReturnValue({ plausible: jest.fn() });

    await userEvent.click(buttonText);

    expect(window.plausible).toHaveBeenCalledWith(
      EXPECTED_PLAUSIBLE_GOAL,
      EXPECTED_PLAUSIBLE_PROPS
    );
  });

  it("should not call plausible without domain given", () => {
    const { buttonText } = setup();

    window.plausible = jest.fn().mockReturnValue({ plausible: jest.fn() });

    userEvent.click(buttonText);

    expect(window.plausible).not.toHaveBeenCalled();
  });
});
