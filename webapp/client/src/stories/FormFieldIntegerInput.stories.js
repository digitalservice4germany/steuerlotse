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

export const WithValue = Template.bind({});
WithValue.args = {
  ...Default.args,
  value: "20",
};

export const WithErrors = Template.bind({});
WithErrors.args = {
  ...Default.args,
  errors: ["Dieses Feld wird benötigt"],
};

export const WithDetails = Template.bind({});
WithDetails.args = {
  ...Default.args,
  details: {
    title: "Was bedeutet das?",
    text: "Erklärungs-Platzhalter",
  },
};

export const WithAllLabelExtras = Template.bind({});
WithAllLabelExtras.args = {
  ...WithDetails.args,
  label: {
    text: "Grad der Behinderung",
    showOptionalTag: true,
    help: "Das ist ein Hilfetext. Hilft er dir?",
    exampleInput: "ab 20",
  },
};

export const WithFieldWidth = Template.bind({});
WithFieldWidth.args = {
  ...Default.args,
  fieldWidth: 4,
};

export const WithMaxLength = Template.bind({});
WithMaxLength.args = {
  ...Default.args,
  maxLength: 4,
};

export const WithMaxLengthAndWidth = Template.bind({});
WithMaxLengthAndWidth.args = {
  ...Default.args,
  maxLength: 4,
  fieldWidth: 4,
};

export const OnALongPage = TemplateLong.bind({});
OnALongPage.args = {
  ...Default.args,
};
