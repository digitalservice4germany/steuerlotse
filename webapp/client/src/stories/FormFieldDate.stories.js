import React from "react";

import FormFieldDate from "../components/FormFieldDate";
import StepForm from "../components/StepForm";
import { Default as StepFormDefault } from "./StepForm.stories";

export default {
  title: "Form Fields/Date",
  component: FormFieldDate,
};

const Template = (args) => (
  <StepForm {...StepFormDefault.args}>
    <FormFieldDate {...args} />
  </StepForm>
);

export const Default = Template.bind({});
Default.args = {
  fieldId: "date",
  fieldName: "date",
  label: {
    text: "Datum",
  },
  errors: [],
  values: [],
};
