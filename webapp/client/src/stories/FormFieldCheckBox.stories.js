import React from "react";

import FormFieldCheckBox from "../components/FormFieldCheckBox";
import StepForm from "../components/StepForm";
import { Default as StepFormDefault } from "./StepForm.stories";

export default {
  title: "Form Fields/CheckBox",
  component: FormFieldCheckBox,
};

function Template(args) {
  <StepForm {...StepFormDefault.args}>
    <FormFieldCheckBox {...args} />
  </StepForm>;
}

export const Default = Template.bind({});
Default.args = {
  fieldId: "checkBox",
  fieldName: "checkBox",
  labelText: "Merkzeichen G",
  errors: [],
  values: [],
};

export const WithErrors = Template.bind({});
WithErrors.args = {
  fieldId: "checkBox",
  fieldName: "checkBox",
  labelText: "Merkzeichen G",
  errors: ["Dieses Feld muss ausgewählt werden."],
};

export const PreCheckedWithErrors = Template.bind({});
PreCheckedWithErrors.args = {
  fieldId: "checkBox",
  fieldName: "checkBox",
  labelText: "Merkzeichen G",
  checked: true,
  errors: ["Dieses Feld darf nicht ausgewählt werden."],
  values: [],
};
