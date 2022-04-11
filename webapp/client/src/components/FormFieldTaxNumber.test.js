import React from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import FormFieldTaxNumber from "./FormFieldTaxNumber";

describe("FormFieldTaxNumber has splitType_0", () => {
  let props;
  const exampleInput = "exampleInput";
  const user = userEvent.setup();

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

  it("should set focus on second input field after pressing tab two times", async () => {
    await user.tab();
    await user.tab();

    expect(screen.getAllByRole("textbox")[1]).toHaveFocus();
  });

  it("should set focus on third input field after pressing tab three times", async () => {
    await user.tab();
    await user.tab();
    await user.tab();

    expect(screen.getAllByRole("textbox")[2]).toHaveFocus();
  });

  describe("When typing 12 characters into each input", () => {
    const inputCharacters = "123456789012";

    it("should only contain first 2 characters in first input", async () => {
      await user.type(screen.getAllByRole("textbox")[0], inputCharacters);
      await user.type(screen.getAllByRole("textbox")[1], inputCharacters);
      await user.type(screen.getAllByRole("textbox")[2], inputCharacters);

      expect(screen.getAllByRole("textbox")[0]).toHaveValue(
        inputCharacters.slice(0, 2)
      );
    });

    it("should only contain first 3 characters in second input", async () => {
      await user.type(screen.getAllByRole("textbox")[0], inputCharacters);
      await user.type(screen.getAllByRole("textbox")[1], inputCharacters);
      await user.type(screen.getAllByRole("textbox")[2], inputCharacters);

      expect(screen.getAllByRole("textbox")[1]).toHaveValue(
        inputCharacters.slice(0, 3)
      );
    });

    it("should only contain first 5 characters in third input", async () => {
      await user.type(screen.getAllByRole("textbox")[0], inputCharacters);
      await user.type(screen.getAllByRole("textbox")[1], inputCharacters);
      await user.type(screen.getAllByRole("textbox")[2], inputCharacters);

      expect(screen.getAllByRole("textbox")[2]).toHaveValue(
        inputCharacters.slice(0, 5)
      );
    });
  });

  describe("When pressing tab", () => {
    it("should set focus on first input field", async () => {
      await user.tab();

      expect(screen.getAllByRole("textbox")[0]).toHaveFocus();
    });

    it("Should enter letters into first input field", async () => {
      const inputCharacters = "123456789012";

      await user.tab();
      await user.keyboard(inputCharacters);

      expect(screen.getAllByRole("textbox")[0]).toHaveValue(
        inputCharacters.slice(0, 2)
      );
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

  it("should show three input fields", () => {
    expect(screen.getAllByRole("textbox")).toHaveLength(3);
  });

  it("should not show example input", () => {
    expect(screen.queryByText("exampleInput")).toBeNull();
  });

  describe("When typing 12 characters into each input", () => {
    const inputCharacters = "123456789012";
    const user = userEvent.setup();

    it("should only contain first 3 characters in first input", async () => {
      await user.type(screen.getAllByRole("textbox")[0], inputCharacters);
      await user.type(screen.getAllByRole("textbox")[1], inputCharacters);
      await user.type(screen.getAllByRole("textbox")[2], inputCharacters);

      expect(screen.getAllByRole("textbox")[0]).toHaveValue(
        inputCharacters.slice(0, 3)
      );
    });

    it("should only contain first 2 characters in second input", async () => {
      await user.type(screen.getAllByRole("textbox")[0], inputCharacters);
      await user.type(screen.getAllByRole("textbox")[1], inputCharacters);
      await user.type(screen.getAllByRole("textbox")[2], inputCharacters);

      expect(screen.getAllByRole("textbox")[1]).toHaveValue(
        inputCharacters.slice(0, 3)
      );
    });

    it("Third input should only contain first 5 characters", async () => {
      await user.type(screen.getAllByRole("textbox")[0], inputCharacters);
      await user.type(screen.getAllByRole("textbox")[1], inputCharacters);
      await user.type(screen.getAllByRole("textbox")[2], inputCharacters);

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
    const user = userEvent.setup();

    it("should only contain first 3 characters in first input", async () => {
      await user.type(screen.getAllByRole("textbox")[0], inputCharacters);
      await user.type(screen.getAllByRole("textbox")[1], inputCharacters);
      await user.type(screen.getAllByRole("textbox")[2], inputCharacters);

      expect(screen.getAllByRole("textbox")[0]).toHaveValue(
        inputCharacters.slice(0, 3)
      );
    });

    it("should only contain first 4 characters in second input", async () => {
      await user.type(screen.getAllByRole("textbox")[0], inputCharacters);
      await user.type(screen.getAllByRole("textbox")[1], inputCharacters);
      await user.type(screen.getAllByRole("textbox")[2], inputCharacters);

      expect(screen.getAllByRole("textbox")[1]).toHaveValue(
        inputCharacters.slice(0, 4)
      );
    });

    it("should only contain first 4 characters in third input", async () => {
      await user.type(screen.getAllByRole("textbox")[0], inputCharacters);
      await user.type(screen.getAllByRole("textbox")[1], inputCharacters);
      await user.type(screen.getAllByRole("textbox")[2], inputCharacters);

      expect(screen.getAllByRole("textbox")[2]).toHaveValue(
        inputCharacters.slice(0, 4)
      );
    });
  });
});

describe("FormFieldTaxNumber is not split", () => {
  let props;
  const exampleInput = "exampleInput";
  const inputCharacters = "123456789012";
  const user = userEvent.setup();

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

  it("should contain all 12 characters, when typing 12 characters into input", async () => {
    await user.type(screen.getByRole("textbox"), inputCharacters);

    expect(screen.getByRole("textbox")).toHaveValue(inputCharacters);
  });

  it("should set focus on input field, when pressing tab", async () => {
    await user.tab();

    expect(screen.getByRole("textbox")).toHaveFocus();
  });

  it("should enter letters into input field, when pressing tab", async () => {
    await user.tab();
    await user.keyboard(inputCharacters);

    expect(screen.getByRole("textbox")).toHaveValue(inputCharacters);
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
