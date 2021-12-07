import React from "react";

import FormFieldTaxNumber from "../components/FormFieldTaxNumber";
import StepForm from "../components/StepForm";
import { Default as StepFormDefault } from "./StepForm.stories";

export default {
  title: "Form Fields/TaxNumber",
  component: FormFieldTaxNumber,
};

function Template(args) {
  return (
    <StepForm {...StepFormDefault.args}>
      <FormFieldTaxNumber {...args} />
    </StepForm>
  );
}

export const Default = Template.bind({});
Default.args = {
  fieldId: "taxNumber",
  fieldName: "taxNumber",
  errors: [],
  values: [],
  splitType: "splitType_notSplit",
};

export const NotSplitDefaultValue = Template.bind({});
NotSplitDefaultValue.args = {
  ...Default.args,
  values: ["12345678901"],
};

export const NotSplitWithError = Template.bind({});
NotSplitWithError.args = {
  ...Default.args,
  values: ["123", "4567", "8901"],
  errors: ["Sie müssen eine gültige Steuernummer angeben"],
};

export const SplitDefaultValue = Template.bind({});
SplitDefaultValue.args = {
  ...Default.args,
  values: ["123", "4567", "8901"],
  splitType: "splitType_0",
};

export const SplitWithError = Template.bind({});
SplitWithError.args = {
  ...SplitDefaultValue.args,
  errors: ["Sie müssen eine gültige Steuernummer angeben"],
};
