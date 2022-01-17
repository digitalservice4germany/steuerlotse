import React from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import FormFieldTaxNumber from "./FormFieldTaxNumber";

describe("FormFieldTaxNumber has splitType_0", () => {
  let props;
  const exampleInput = "exampleInput";

  beforeEach(() => {
    props = {
      fieldName: "fooName",
      fieldId: "fooId",
      label: {
        text: "foo",
        exampleInput,
      },
      errors: [],
      values: [],
      splitType: "splitType_0",
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
    const inputCharacters = "123456789012";

    beforeEach(() => {
      userEvent.type(screen.getAllByRole("textbox")[0], inputCharacters);
      userEvent.type(screen.getAllByRole("textbox")[1], inputCharacters);
      userEvent.type(screen.getAllByRole("textbox")[2], inputCharacters);
    });

    it("First input should only contain first 2 characters", () => {
      expect(screen.getAllByRole("textbox")[0]).toHaveValue(
        inputCharacters.slice(0, 2)
      );
    });

    it("Second input should only contain first 3 characters", () => {
      expect(screen.getAllByRole("textbox")[1]).toHaveValue(
        inputCharacters.slice(0, 3)
      );
    });

    it("Third input should only contain first 5 characters", () => {
      expect(screen.getAllByRole("textbox")[2]).toHaveValue(
        inputCharacters.slice(0, 5)
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
      const inputCharacters = "123456789012";

      beforeEach(() => {
        userEvent.keyboard(inputCharacters);
      });

      it("Should enter letters into first input field", () => {
        expect(screen.getAllByRole("textbox")[0]).toHaveValue(
          inputCharacters.slice(0, 2)
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

describe("FormFieldTaxNumber has splitType_1", () => {
  let props;
  const exampleInput = "exampleInput";

  beforeEach(() => {
    props = {
      fieldName: "fooName",
      fieldId: "fooId",
      label: {
        text: "foo",
        exampleInput,
      },
      errors: [],
      values: [],
      splitType: "splitType_1",
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
    const inputCharacters = "123456789012";

    beforeEach(() => {
      userEvent.type(screen.getAllByRole("textbox")[0], inputCharacters);
      userEvent.type(screen.getAllByRole("textbox")[1], inputCharacters);
      userEvent.type(screen.getAllByRole("textbox")[2], inputCharacters);
    });

    it("First input should only contain first 3 characters", () => {
      expect(screen.getAllByRole("textbox")[0]).toHaveValue(
        inputCharacters.slice(0, 3)
      );
    });

    it("Second input should only contain first 3 characters", () => {
      expect(screen.getAllByRole("textbox")[1]).toHaveValue(
        inputCharacters.slice(0, 3)
      );
    });

    it("Third input should only contain first 5 characters", () => {
      expect(screen.getAllByRole("textbox")[2]).toHaveValue(
        inputCharacters.slice(0, 5)
      );
    });
  });
});

describe("FormFieldTaxNumber has splitType_2", () => {
  let props;
  const exampleInput = "exampleInput";

  beforeEach(() => {
    props = {
      fieldName: "fooName",
      fieldId: "fooId",
      label: {
        text: "foo",
        exampleInput,
      },
      errors: [],
      values: [],
      splitType: "splitType_2",
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
    const inputCharacters = "123456789012";

    beforeEach(() => {
      userEvent.type(screen.getAllByRole("textbox")[0], inputCharacters);
      userEvent.type(screen.getAllByRole("textbox")[1], inputCharacters);
      userEvent.type(screen.getAllByRole("textbox")[2], inputCharacters);
    });

    it("First input should only contain first 3 characters", () => {
      expect(screen.getAllByRole("textbox")[0]).toHaveValue(
        inputCharacters.slice(0, 3)
      );
    });

    it("Second input should only contain first 4 characters", () => {
      expect(screen.getAllByRole("textbox")[1]).toHaveValue(
        inputCharacters.slice(0, 4)
      );
    });

    it("Third input should only contain first 4 characters", () => {
      expect(screen.getAllByRole("textbox")[2]).toHaveValue(
        inputCharacters.slice(0, 4)
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
        exampleInput,
      },
      errors: [],
      values: [],
      splitType: "splitType_notSplit",
    };
    render(<FormFieldTaxNumber {...props} />);
  });

  it("Should set no maxLength attribute", () => {
    expect(screen.getByRole("textbox").hasOwnProperty("maxLength")).toBe(false);
  });

  it("Should only show one input field", () => {
    expect(screen.getAllByRole("textbox")).toHaveLength(1);
  });

  it("Should show example input", () => {
    expect(screen.queryByText("exampleInput")).toBeNull();
  });

  describe("When typing 12 characters into input", () => {
    const inputCharacters = "123456789012";

    beforeEach(() => {
      userEvent.type(screen.getByRole("textbox"), inputCharacters);
    });

    it("Input should contain all 12 characters", () => {
      expect(screen.getByRole("textbox")).toHaveValue(inputCharacters);
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
      const inputCharacters = "123456789012";

      beforeEach(() => {
        userEvent.keyboard(inputCharacters);
      });

      it("Should enter letters into input field", () => {
        expect(screen.getByRole("textbox")).toHaveValue(inputCharacters);
      });
    });
  });
});

describe("FormFieldTaxNumber with some values already set", () => {
  let props;
  const inputTaxNumber = ["198", "", "0010"];

  beforeEach(() => {
    props = {
      fieldName: "fooName",
      fieldId: "fooId",
      label: {
        text: "foo",
        exampleInput: "fooExampleInput",
      },
      errors: [],
      values: inputTaxNumber,
      splitType: "splitType_2",
    };
    render(<FormFieldTaxNumber {...props} />);
  });

  it("Should set the values into the correct inputs", () => {
    expect(screen.getAllByRole("textbox")[0]).toHaveValue(inputTaxNumber[0]);
    expect(screen.getAllByRole("textbox")[1]).toHaveValue(inputTaxNumber[1]);
    expect(screen.getAllByRole("textbox")[2]).toHaveValue(inputTaxNumber[2]);
  });
});
