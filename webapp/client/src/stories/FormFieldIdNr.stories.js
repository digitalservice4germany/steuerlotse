import React from "react";

import FormFieldIdNr from "../components/FormFieldIdNr";
import StepForm from "../components/StepForm";
import { Default as StepFormDefault } from "./StepForm.stories";

export default {
  title: "Form Fields/IdNr",
  component: FormFieldIdNr,
};

const Template = (args) => (
  <StepForm {...StepFormDefault.args}>
    <FormFieldIdNr {...args} />
  </StepForm>
);

export const Default = Template.bind({});
Default.args = {
  fieldId: "idnr",
  fieldName: "idnr",
  label: {
    text: "Steuer-Identifikationsnummer",
  },
  errors: [],
  values: [],
};
