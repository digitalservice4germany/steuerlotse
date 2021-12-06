import React from "react";

import FormFieldIdNr from "../components/FormFieldIdNr";
import StepForm from "../components/StepForm";
import { Default as StepFormDefault } from "./StepForm.stories";

export default {
  title: "Form Fields/IdNr",
  component: FormFieldIdNr,
};

function Template(args) {
  <StepForm {...StepFormDefault.args}>
    <FormFieldIdNr {...args} />
  </StepForm>;
}

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

export const WithDetails = Template.bind({});
WithDetails.args = {
  fieldId: "idnr",
  fieldName: "idnr",
  label: {
    text: "Steuer-Identifikationsnummer",
  },
  details: {
    title: "Was ist das für eine Nummer?",
    text: "Das ist Ihre persönliche Nummer, mit der Sie sich beim Finanzamt identifizieren können.",
  },
  errors: [],
  values: [],
};
