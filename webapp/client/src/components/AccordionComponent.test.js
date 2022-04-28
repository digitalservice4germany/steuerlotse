import React from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import AccordionComponent from "./AccordionComponent";

const REQUIRED_PROPS = {
  title: "Accordion Title",
  items: [
    {
      title: "Item1 Title",
      detail: "Item1 Detail",
    },
    {
      title: "Item2 Title",
      detail: "Item2 Detail",
    },
  ],
};

function setup(optionalProps) {
  const utils = render(
    <AccordionComponent {...REQUIRED_PROPS} {...optionalProps} />
  );
  const firstItemHeader = screen.getByText("Item1 Title");
  const secondItemHeader = screen.getByText("Item2 Title");
  const user = userEvent.setup();

  return { ...utils, firstItemHeader, secondItemHeader, user };
}

describe("AccordionComponent", () => {
  it("should render first item", () => {
    setup();

    expect(screen.getByText(REQUIRED_PROPS.items[0].title)).toBeInTheDocument();
    expect(
      screen.getByText(REQUIRED_PROPS.items[0].detail)
    ).toBeInTheDocument();
  });

  it("should render second item", () => {
    setup();

    expect(screen.getByText(REQUIRED_PROPS.items[1].title)).toBeInTheDocument();
    expect(
      screen.getByText(REQUIRED_PROPS.items[0].detail)
    ).toBeInTheDocument();
  });
});
