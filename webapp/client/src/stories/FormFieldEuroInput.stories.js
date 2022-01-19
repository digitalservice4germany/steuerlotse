import React from "react";

import FormFieldEuroInput from "../components/FormFieldEuroInput";
import StepForm from "../components/StepForm";
import { Default as StepFormDefault } from "./StepForm.stories";

export default {
  title: "Form Fields/EuroInput",
  component: FormFieldEuroInput,
};

function Template(args) {
  return (
    <StepForm {...StepFormDefault.args}>
      <FormFieldEuroInput {...args} />
    </StepForm>
  );
}

export const Default = Template.bind({});
Default.args = {
  fieldId: "euro-input",
  fieldName: "euro-input",
  label: {
    text: "Summe der Rechnungsbeträge",
    exampleInput: "z.B 100,12€",
  },
  errors: [],
  value: "",
};

export const WithErrors = Template.bind({});
WithErrors.args = {
  ...Default.args,
  errors: ["Dieses Feld wird benötigt"],
};

export const WithValue = Template.bind({});
WithValue.args = {
  ...Default.args,
  value: "111,11",
};
