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
  const user = userEvent.setup();

  return { ...utils, button: buttonText, user };
}

describe("AnchorButton", () => {
  it("should render the button text", () => {
    setup();

    expect(screen.getByText(REQUIRED_PROPS.text)).toBeInTheDocument();
  });

  it("should have a href attribute", () => {
    const { button } = setup();

    expect(button.closest("a")).toHaveAttribute(
      "href",
      expect.stringContaining(REQUIRED_PROPS.url)
    );
  });

  it("should not have a download attribute if isDownloadLink is false", () => {
    const { button } = setup({
      isDownloadLink: false,
    });

    expect(button.closest("a")).not.toHaveAttribute("download");
  });

  it("should have a download attribute if isDownloadLink is true", () => {
    const { button } = setup({
      isDownloadLink: true,
    });

    expect(button.closest("a")).toHaveAttribute("download");
  });
});

describe("AnchorButton with plausible", () => {
  it("should call plausible with goal", async () => {
    const { button, user } = setup({
      plausibleDomain: "domain/some/link/path",
      plausibleGoal: "plausible_goal",
    });
    const EXPECTED_PLAUSIBLE_GOAL = "plausible_goal";

    window.plausible = jest.fn();

    await user.click(button);

    expect(window.plausible).toHaveBeenCalledWith(EXPECTED_PLAUSIBLE_GOAL, {
      props: undefined,
    });
  });

  it("should call plausible with goal and props", async () => {
    const { button, user } = setup({
      plausibleDomain: "domain/some/link/path",
      plausibleGoal: "plausible_goal",
      plausibleProps: { method: "plausible_props" },
    });
    const EXPECTED_PLAUSIBLE_GOAL = "plausible_goal";
    const EXPECTED_PLAUSIBLE_PROPS = { props: { method: "plausible_props" } };

    window.plausible = jest.fn();

    await user.click(button);

    expect(window.plausible).toHaveBeenCalledWith(
      EXPECTED_PLAUSIBLE_GOAL,
      EXPECTED_PLAUSIBLE_PROPS
    );
  });

  it("should not call plausible without domain given", async () => {
    const { button, user } = setup();

    window.plausible = jest.fn();

    await user.click(button);

    expect(window.plausible).not.toHaveBeenCalled();
  });
});
