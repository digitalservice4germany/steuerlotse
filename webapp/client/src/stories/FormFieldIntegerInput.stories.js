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
export const WithValue = Template.bind({});
export const WithErrors = Template.bind({});
export const WithDetails = Template.bind({});
export const WithAllLabelExtras = Template.bind({});
export const WithMaxWidth = Template.bind({});
export const WithMaxLength = Template.bind({});
export const WithMaxLengthAndWidth = Template.bind({});

export const OnALongPage = TemplateLong.bind({});

Default.args = {
  fieldId: "number-input",
  fieldName: "number-input",
  label: {
    text: "Grad der Behinderung",
  },
  errors: [],
  value: "",
};

WithValue.args = {
  ...Default.args,
  value: "20",
};

WithErrors.args = {
  ...Default.args,
  errors: ["Dieses Feld wird benötigt"],
};

WithDetails.args = {
  ...Default.args,
  details: {
    title: "Was bedeutet das?",
    text: "Erklärungs-Platzhalter",
  },
};

WithAllLabelExtras.args = {
  ...WithDetails.args,
  label: {
    text: "Grad der Behinderung",
    showOptionalTag: true,
    help: "Das ist ein Hilfetext. Hilft er dir?",
    exampleInput: "ab 20",
  },
};

WithMaxWidth.args = {
  ...Default.args,
  maxWidth: 4,
};

WithMaxLength.args = {
  ...Default.args,
  maxLength: 4,
};

WithMaxLengthAndWidth.args = {
  ...Default.args,
  maxLength: 4,
  maxWidth: 4,
};

OnALongPage.args = {
  ...Default.args,
};
