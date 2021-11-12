import React from "react";

import FormFieldTaxNumber from "../components/FormFieldTaxNumber";
import StepForm from "../components/StepForm";
import { Default as StepFormDefault } from "./StepForm.stories";

export default {
  title: "Form Fields/TaxNumber",
  component: FormFieldTaxNumber,
};

const Template = (args) => (
  <StepForm {...StepFormDefault.args}>
    <FormFieldTaxNumber {...args} />
  </StepForm>
);

export const Default = Template.bind({});
Default.args = {
  fieldId: "taxNumber",
  fieldName: "taxNumber",
  label: {
    text: "Steuernummer",
    exampleInput: "123 3455 3456",
  },
  errors: [],
  values: [],
  isSplit: false,
};

export const NotSplitDefaultValue = Template.bind({});
NotSplitDefaultValue.args = {
  ...Default.args,
  values: ["12345678901"],
};

export const SplitDefaultValue = Template.bind({});
SplitDefaultValue.args = {
  ...Default.args,
  values: ["123", "4567", "8901"],
  isSplit: true,
};
