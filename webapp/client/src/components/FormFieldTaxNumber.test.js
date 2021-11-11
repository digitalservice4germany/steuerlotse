import React from "react";
import { render, screen } from "@testing-library/react";
import { fireEvent } from "@testing-library/dom";
import userEvent from "@testing-library/user-event";
import FormFieldTaxNumber from "./FormFieldTaxNumber";

describe("FormFieldTaxNumber is split", () => {
  let props;
  const exampleInput = "exampleInput";

  beforeEach(() => {
    props = {
      fieldName: "fooName",
      fieldId: "fooId",
      label: {
        text: "foo",
        exampleInput: exampleInput,
      },
      errors: [],
      values: [],
      isSplit: true,
    };
    render(<FormFieldTaxNumber {...props} />);
  });

  it("Show three input fields", () => {
    expect(screen.getAllByRole("textbox")).toHaveLength(3);
  });

  it("Do not show example input", () => {
    expect(screen.queryByText("exampleInput")).toBeNull();
  });

  describe("Type 12 characters into each input", () => {
    const input_characters = "123456789012";

    beforeEach(() => {
      userEvent.type(screen.getAllByRole("textbox")[0], input_characters);
      userEvent.type(screen.getAllByRole("textbox")[1], input_characters);
      userEvent.type(screen.getAllByRole("textbox")[2], input_characters);
    });

    it("First input contains only first 3 characters", () => {
      expect(screen.getAllByRole("textbox")[0]).toHaveValue(
        input_characters.slice(0, 3)
      );
    });

    it("First input contains only first 4 characters", () => {
      expect(screen.getAllByRole("textbox")[1]).toHaveValue(
        input_characters.slice(0, 4)
      );
    });

    it("First input contains only first 4 characters", () => {
      expect(screen.getAllByRole("textbox")[2]).toHaveValue(
        input_characters.slice(0, 4)
      );
    });
  });

  describe("When pressing tab", () => {
    beforeEach(() => {
      userEvent.tab();
    });

    it("Set focus on first input field", () => {
      expect(screen.getAllByRole("textbox")[0]).toHaveFocus();
    });

    describe("When typing", () => {
      const input_characters = "123456789012";

      beforeEach(() => {
        userEvent.keyboard(input_characters);
      });

      it("Enter letters into first input field", () => {
        expect(screen.getAllByRole("textbox")[0]).toHaveValue(
          input_characters.slice(0, 3)
        );
      });
    });

    it("Set focus on second input field after second tab", () => {
      userEvent.tab();
      expect(screen.getAllByRole("textbox")[1]).toHaveFocus();
    });

    it("Set focus on third input field after third tab", () => {
      userEvent.tab();
      userEvent.tab();
      expect(screen.getAllByRole("textbox")[2]).toHaveFocus();
    });
  });
});

describe("FormFieldTaxNumber is not split", () => {
  let props;
  const exampleInput = "exampleInput";

  beforeEach(() => {
    props = {
      fieldName: "fooName",
      fieldId: "fooId",
      label: {
        text: "foo",
        exampleInput: exampleInput,
      },
      errors: [],
      values: [],
      isSplit: false,
    };
    render(<FormFieldTaxNumber {...props} />);
  });

  it("Show only one input field", () => {
    expect(screen.getAllByRole("textbox")).toHaveLength(1);
  });

  it("show example input", () => {
    expect(screen.queryByText("exampleInput")).toBeNull();
  });

  describe("Type 12 characters into input", () => {
    const input_characters = "123456789012";

    beforeEach(() => {
      userEvent.type(screen.getByRole("textbox"), input_characters);
    });

    it("Input contains only first 11 characters", () => {
      expect(screen.getByRole("textbox")).toHaveValue(
        input_characters.slice(0, 11)
      );
    });
  });

  describe("When pressing tab", () => {
    beforeEach(() => {
      userEvent.tab();
    });

    it("Set focus on input field", () => {
      expect(screen.getByRole("textbox")).toHaveFocus();
    });

    describe("When typing", () => {
      const input_characters = "123456789012";

      beforeEach(() => {
        userEvent.keyboard(input_characters);
      });

      it("Enter letters into input field", () => {
        expect(screen.getByRole("textbox")).toHaveValue(
          input_characters.slice(0, 11)
        );
      });
    });
  });
});
