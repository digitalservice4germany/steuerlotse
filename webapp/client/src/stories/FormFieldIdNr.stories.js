import React from "react";

import FormFieldIdNr from "../components/FormFieldIdNr";
import FormRowCentered from "../components/FormRowCentered";
import StepForm from "../components/StepForm";
import { Default as StepFormDefault } from "./StepForm.stories";

export default {
  title: "Form Fields/IdNr",
  component: FormFieldIdNr,
};

const Template = (args) => (
  <StepForm {...StepFormDefault.args}>
    <FormRowCentered>
      <FormFieldIdNr {...args} />
    </FormRowCentered>
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
