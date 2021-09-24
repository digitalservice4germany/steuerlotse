import React from "react";
import { render, screen } from "@testing-library/react";
import FieldLabelScaffolding from "./FieldLabelScaffolding";

describe("FieldLabelScaffolding", () => {
  let container;
  let label;
  let details;

  function renderLabel() {
    container = render(
      <FieldLabelScaffolding
        fieldId="my-id"
        label={label}
        details={details}
        render={(innerContent) => <span>{innerContent}</span>}
      />
    ).container;
  }

  beforeEach(() => {
    label = {};
  });

  it("should render nothing by default", () => {
    renderLabel();
    expect(container).toBeEmptyDOMElement();
  });

  describe("with label text", () => {
    beforeEach(() => {
      label.text = "content";
    });

    it("should render the text", () => {
      renderLabel();
      expect(screen.getByText("content")).toBeInTheDocument();
    });

    describe("with help", () => {
      beforeEach(() => {
        label.help = "help";
      });

      it("should render a help button", () => {
        renderLabel();
        expect(screen.getByText("?")).toBeInTheDocument();
      });
    });

    describe("with exampleInput", () => {
      beforeEach(() => {
        label.exampleInput = "my example input";
      });

      it("should render the example input", () => {
        renderLabel();
        expect(screen.getByText("my example input")).toBeInTheDocument();
      });
    });

    describe("with details", () => {
      beforeEach(() => {
        details = { title: "details title", text: "details body" };
      });

      it("should render the details content", () => {
        renderLabel();
        expect(screen.getByText("details title")).toBeInTheDocument();
        expect(screen.getByText("details body")).toBeInTheDocument();
      });
    });
  });
});
