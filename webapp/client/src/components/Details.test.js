import React from "react";
import { render, screen } from "@testing-library/react";
import Details from "./Details";

describe("Details with content paragraphs", () => {
  beforeEach(() => {
    render(
      <Details title="title" detailsId="my-id">
        {{
          paragraphs: ["content paragraph"],
        }}
      </Details>
    );
  });

  it("should render the title", () => {
    expect(screen.getByText("title")).toBeInTheDocument();
  });

  it("should render paragraphs", () => {
    expect(screen.getByText("content paragraph").nodeName).toEqual("P");
  });
});

describe("Details with content paragraphs and list items", () => {
  beforeEach(() => {
    render(
      <Details title="title" detailsId="some-id">
        {{
          paragraphs: ["content paragraph"],
          listItems: ["list item"],
        }}
      </Details>
    );
  });

  it("should render list items", () => {
    expect(screen.getByText("list item").nodeName).toEqual("LI");
  });
});
