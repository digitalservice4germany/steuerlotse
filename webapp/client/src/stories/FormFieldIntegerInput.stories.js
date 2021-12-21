import React from "react";

import FormFieldIntegerInput from "../components/FormFieldIntegerInput";
import StepForm from "../components/StepForm";
import { Default as StepFormDefault } from "./StepForm.stories";

export default {
  title: "Form Fields/IntegerInput",
  component: FormFieldIntegerInput,
};

function Template(args) {
  return (
    <StepForm {...StepFormDefault.args}>
      <FormFieldIntegerInput {...args} />
    </StepForm>
  );
}

function TemplateLong(args) {
  const style = {
    height: 1000,
  };
  return (
    <StepForm {...StepFormDefault.args}>
      <FormFieldIntegerInput {...args} />
      <div style={style} />
    </StepForm>
  );
}

export const Default = Template.bind({});
Default.args = {
  fieldId: "number-input",
  fieldName: "number-input",
  label: {
    text: "Grad der Behinderung",
  },
  errors: [],
  value: "",
};

export const WithErrors = Template.bind({});
WithErrors.args = {
  ...Default.args,
  errors: ["Dieses Feld wird benötigt"],
};

export const WithAllLabelExtras = Template.bind({});
WithAllLabelExtras.args = {
  ...Default.args,
  label: {
    text: "Grad der Behinderung",
    showOptionalTag: true,
    help: "Das ist ein Hilfetext. Hilft er dir?",
    exampleInput: "ab 20",
  },
  details: {
    title: "Was bedeutet das?",
    text: "Erklärungs-Platzhalter",
  },
};

export const WithMaxLengthAndWidth = Template.bind({});
WithMaxLengthAndWidth.args = {
  ...Default.args,
  maxLength: 4,
  fieldWidth: 4,
};

// We add this story because the Integer field previously had differing behaviour on short and long pages.
export const OnALongPage = TemplateLong.bind({});
OnALongPage.args = {
  ...Default.args,
};
