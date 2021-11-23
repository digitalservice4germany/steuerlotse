import React from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import FormFieldTaxNumber from "./FormFieldTaxNumber";

describe("FormFieldTaxNumber has splitType 0", () => {
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
      splitType: "0",
    };
    render(<FormFieldTaxNumber {...props} />);
  });

  it("Should show three input fields", () => {
    expect(screen.getAllByRole("textbox")).toHaveLength(3);
  });

  it("Should not show example input", () => {
    expect(screen.queryByText("exampleInput")).toBeNull();
  });

  describe("When typing 12 characters into each input", () => {
    const input_characters = "123456789012";

    beforeEach(() => {
      userEvent.type(screen.getAllByRole("textbox")[0], input_characters);
      userEvent.type(screen.getAllByRole("textbox")[1], input_characters);
      userEvent.type(screen.getAllByRole("textbox")[2], input_characters);
    });

    it("First input should only contain first 2 characters", () => {
      expect(screen.getAllByRole("textbox")[0]).toHaveValue(
        input_characters.slice(0, 2)
      );
    });

    it("Second input should only contain first 3 characters", () => {
      expect(screen.getAllByRole("textbox")[1]).toHaveValue(
        input_characters.slice(0, 3)
      );
    });

    it("Third input should only contain first 5 characters", () => {
      expect(screen.getAllByRole("textbox")[2]).toHaveValue(
        input_characters.slice(0, 5)
      );
    });
  });

  describe("When pressing tab", () => {
    beforeEach(() => {
      userEvent.tab();
    });

    it("Should focus on first input field", () => {
      expect(screen.getAllByRole("textbox")[0]).toHaveFocus();
    });

    describe("When typing", () => {
      const input_characters = "123456789012";

      beforeEach(() => {
        userEvent.keyboard(input_characters);
      });

      it("Should enter letters into first input field", () => {
        expect(screen.getAllByRole("textbox")[0]).toHaveValue(
          input_characters.slice(0, 2)
        );
      });
    });

    it("Should set focus on second input field after second tab", () => {
      userEvent.tab();
      expect(screen.getAllByRole("textbox")[1]).toHaveFocus();
    });

    it("Should set focus on third input field after third tab", () => {
      userEvent.tab();
      userEvent.tab();
      expect(screen.getAllByRole("textbox")[2]).toHaveFocus();
    });
  });
});

describe("FormFieldTaxNumber has splitType 1", () => {
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
      splitType: "1",
    };
    render(<FormFieldTaxNumber {...props} />);
  });

  it("Should show three input fields", () => {
    expect(screen.getAllByRole("textbox")).toHaveLength(3);
  });

  it("Should not show example input", () => {
    expect(screen.queryByText("exampleInput")).toBeNull();
  });

  describe("When typing 12 characters into each input", () => {
    const input_characters = "123456789012";

    beforeEach(() => {
      userEvent.type(screen.getAllByRole("textbox")[0], input_characters);
      userEvent.type(screen.getAllByRole("textbox")[1], input_characters);
      userEvent.type(screen.getAllByRole("textbox")[2], input_characters);
    });

    it("First input should only contain first 3 characters", () => {
      expect(screen.getAllByRole("textbox")[0]).toHaveValue(
        input_characters.slice(0, 3)
      );
    });

    it("Second input should only contain first 3 characters", () => {
      expect(screen.getAllByRole("textbox")[1]).toHaveValue(
        input_characters.slice(0, 3)
      );
    });

    it("Third input should only contain first 5 characters", () => {
      expect(screen.getAllByRole("textbox")[2]).toHaveValue(
        input_characters.slice(0, 5)
      );
    });
  });
});

describe("FormFieldTaxNumber has splitType 2", () => {
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
      splitType: "2",
    };
    render(<FormFieldTaxNumber {...props} />);
  });

  it("Should show three input fields", () => {
    expect(screen.getAllByRole("textbox")).toHaveLength(3);
  });

  it("Should not show example input", () => {
    expect(screen.queryByText("exampleInput")).toBeNull();
  });

  describe("When typing 12 characters into each input", () => {
    const input_characters = "123456789012";

    beforeEach(() => {
      userEvent.type(screen.getAllByRole("textbox")[0], input_characters);
      userEvent.type(screen.getAllByRole("textbox")[1], input_characters);
      userEvent.type(screen.getAllByRole("textbox")[2], input_characters);
    });

    it("First input should only contain first 3 characters", () => {
      expect(screen.getAllByRole("textbox")[0]).toHaveValue(
        input_characters.slice(0, 3)
      );
    });

    it("Second input should only contain first 4 characters", () => {
      expect(screen.getAllByRole("textbox")[1]).toHaveValue(
        input_characters.slice(0, 4)
      );
    });

    it("Third input should only contain first 4 characters", () => {
      expect(screen.getAllByRole("textbox")[2]).toHaveValue(
        input_characters.slice(0, 4)
      );
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
      splitType: "3",
    };
    render(<FormFieldTaxNumber {...props} />);
  });

  it("Should only show one input field", () => {
    expect(screen.getAllByRole("textbox")).toHaveLength(1);
  });

  it("Should show example input", () => {
    expect(screen.queryByText("exampleInput")).toBeNull();
  });

  describe("When typing 12 characters into input", () => {
    const input_characters = "123456789012";

    beforeEach(() => {
      userEvent.type(screen.getByRole("textbox"), input_characters);
    });

    it("Input should contain only first 11 characters", () => {
      expect(screen.getByRole("textbox")).toHaveValue(
        input_characters.slice(0, 11)
      );
    });
  });

  describe("When pressing tab", () => {
    beforeEach(() => {
      userEvent.tab();
    });

    it("Should set focus on input field", () => {
      expect(screen.getByRole("textbox")).toHaveFocus();
    });

    describe("When typing", () => {
      const input_characters = "123456789012";

      beforeEach(() => {
        userEvent.keyboard(input_characters);
      });

      it("Should enter letters into input field", () => {
        expect(screen.getByRole("textbox")).toHaveValue(
          input_characters.slice(0, 11)
        );
      });
    });
  });
});
