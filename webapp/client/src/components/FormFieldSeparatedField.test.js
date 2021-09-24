import React from "react";
import { render, screen } from "@testing-library/react";
import { fireEvent } from "@testing-library/dom";
import FormFieldSeparatedField from "./FormFieldSeparatedField";

describe("FormFieldSeparatedField", () => {
  let props;

  beforeEach(() => {
    props = {
      fieldName: "foo",
      fieldId: "foo",
      values: ["bar", "baz"],
      inputFieldLengths: [3, 4],
      errors: [],
      labelComponent: <></>,
      subFieldSeparator: "SPLITTO",
    };
  });

  it("should show the values", () => {
    render(<FormFieldSeparatedField {...props} />);
    expect(screen.getByDisplayValue("bar")).toBeInTheDocument();
    expect(screen.getByDisplayValue("baz")).toBeInTheDocument();
  });

  it("should assign the correct ids", () => {
    render(<FormFieldSeparatedField {...props} />);
    expect(screen.getByDisplayValue("bar")).toHaveAttribute("id", "foo_1");
    expect(screen.getByDisplayValue("baz")).toHaveAttribute("id", "foo_2");
  });

  it("should set the lenghts", () => {
    render(<FormFieldSeparatedField {...props} />);
    const bar = screen.getByDisplayValue("bar");
    expect(bar).toHaveAttribute("maxlength", "3");
    expect(bar).toHaveAttribute("data-field-length", "3");
  });

  it("should show field separators", () => {
    render(<FormFieldSeparatedField {...props} />);
    expect(screen.getByText("SPLITTO")).toBeInTheDocument();
  });

  describe("when pasting content", () => {
    let pasteData;
    let pasteText;

    beforeEach(() => {
      pasteText = "asd1234";
      pasteData = {
        clipboardData: {
          items: [
            {
              kind: "string",
              type: "text/plain",
              getAsString: (cb) => cb(pasteText),
            },
          ],
        },
      };
    });

    it("should do nothing for mime types other than text/plain", () => {
      render(<FormFieldSeparatedField {...props} />);

      const element = screen.getByDisplayValue("bar");
      pasteData = {
        clipboardData: {
          items: [
            {
              kind: "string",
              type: "text/html",
            },
          ],
        },
      };
      fireEvent.paste(element, pasteData);

      expect(element).toHaveValue("bar");
    });

    it("should distribute content according to field lengths", () => {
      render(<FormFieldSeparatedField {...props} />);

      const firstElement = screen.getByDisplayValue("bar");
      const secondElement = screen.getByDisplayValue("baz");

      pasteText = "asd123";
      fireEvent.paste(firstElement, pasteData);

      expect(firstElement).toHaveValue("asd");
      expect(secondElement).toHaveValue("123");
    });

    it("should discard extra content at the end", () => {
      render(<FormFieldSeparatedField {...props} />);

      const firstElement = screen.getByDisplayValue("bar");
      const secondElement = screen.getByDisplayValue("baz");

      pasteText = "asd1234567890";
      fireEvent.paste(firstElement, pasteData);

      expect(firstElement).toHaveValue("asd");
      expect(secondElement).toHaveValue("1234");
    });

    it("should clear fields if content is too short", () => {
      render(<FormFieldSeparatedField {...props} />);

      const firstElement = screen.getByDisplayValue("bar");
      const secondElement = screen.getByDisplayValue("baz");

      pasteText = "as";
      fireEvent.paste(firstElement, pasteData);

      expect(firstElement).toHaveValue("as");
      expect(secondElement).toHaveValue("");
    });

    it("pasting into the 2nd field should fill content starting with the 1st field", () => {
      render(<FormFieldSeparatedField {...props} />);

      const firstElement = screen.getByDisplayValue("bar");
      const secondElement = screen.getByDisplayValue("baz");

      pasteText = "asd1234";
      fireEvent.paste(secondElement, pasteData);

      expect(firstElement).toHaveValue("asd");
      expect(secondElement).toHaveValue("1234");
    });

    it("should apply the input mask if present", () => {
      // We need initial values that match the input mask.
      render(
        <FormFieldSeparatedField
          {...{
            ...props,
            values: ["000", "111"],
            extraFieldProps: { "data-mask": "0#" },
          }}
        />
      );

      const firstElement = screen.getByDisplayValue("000");
      const secondElement = screen.getByDisplayValue("111");

      pasteText = "asd1234";
      fireEvent.paste(secondElement, pasteData);

      expect(firstElement).toHaveValue("123");
      expect(secondElement).toHaveValue("4");
    });
  });
});
