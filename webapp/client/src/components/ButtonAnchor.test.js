import React from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import ButtonAnchor from "./ButtonAnchor";

const { Text, Icon } = ButtonAnchor;

const REQUIRED_PROPS = {
  children: "anchor text",
  url: "url/some/link/path",
};

function setup(optionalProps) {
  const utils = render(<ButtonAnchor {...REQUIRED_PROPS} {...optionalProps} />);
  const user = userEvent.setup();

  return { ...utils, user };
}

function ChildComponent() {
  return <div>Child Element</div>;
}

describe("ButtonAnchor", () => {
  it("should render a default anchor button with text and href", () => {
    setup();
    const buttonAnchor = screen.getByText("anchor text");

    expect(buttonAnchor).toBeInTheDocument();
    expect(buttonAnchor).toHaveAttribute("href", REQUIRED_PROPS.url);
  });

  it("should render a outline anchor button", () => {
    setup({
      variant: "outline",
    });
    const buttonAnchor = screen.getByText("anchor text");

    expect(buttonAnchor).toHaveClass("outline");
  });

  it("should render a narrow anchor button", () => {
    setup({
      style: "narrow",
    });
    const buttonAnchor = screen.getByText("anchor text");

    expect(buttonAnchor).toHaveClass("narrow");
  });

  it("should render a high anchor button", () => {
    setup({
      style: "high",
    });
    const buttonAnchor = screen.getByText("anchor text");

    expect(buttonAnchor).toHaveClass("high");
  });

  it("should render a default anchor button with component as text children", () => {
    setup({
      children: (
        <Text>
          <ChildComponent />
        </Text>
      ),
    });

    expect(screen.getByText("Child Element")).toBeInTheDocument();
  });

  it("should render a default anchor button with component as icon children", () => {
    setup({
      children: (
        <Icon>
          <ChildComponent />
        </Icon>
      ),
    });

    expect(screen.getByText("Child Element")).toBeInTheDocument();
  });

  it("should not have a download attribute if download is false", () => {
    setup({
      download: false,
    });
    const buttonAnchor = screen.getByText("anchor text");

    expect(buttonAnchor.closest("a")).not.toHaveAttribute("download");
  });

  it("should have a download attribute if download is true", () => {
    setup({
      download: true,
    });
    const buttonAnchor = screen.getByText("anchor text");

    expect(buttonAnchor.closest("a")).toHaveAttribute("download");
  });

  it("should call a click handler", async () => {
    let isClicked = false;

    const foo = {
      clicked() {
        isClicked = true;
      },
    };
    const spy = jest.spyOn(foo, "clicked");
    const { button, user } = setup({
      onClick: foo.clicked(),
    });

    await user.click(button);

    expect(spy).toHaveBeenCalled();

    expect(isClicked).toBe(true);

    spy.mockRestore();
  });
});
