import React from "react";
import { render, screen } from "@testing-library/react";
import DetailsSeparated from "./DetailsSeparated";

describe("DetailsSeparated with single paragraph", () => {
  beforeEach(() => {
    render(
      <DetailsSeparated title="title" detailsId="my-id">
        <p>content paragraph</p>
      </DetailsSeparated>
    );
  });

  it("should render the title", () => {
    expect(screen.getByText("title")).toBeInTheDocument();
  });

  it("should render paragraphs", () => {
    expect(screen.getByText("content paragraph").nodeName).toEqual("P");
  });
});

describe("DetailsSeparated with content paragraphs and list items", () => {
  beforeEach(() => {
    render(
      <DetailsSeparated title="title" detailsId="some-id">
        {[
          <p key={0}>content paragraph</p>,
          <ul key={1}>
            <li>list item</li>
          </ul>,
        ]}
      </DetailsSeparated>
    );
  });

  it("should render list items", () => {
    expect(screen.getByText("list item").nodeName).toEqual("LI");
  });
});
