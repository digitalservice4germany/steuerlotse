import React from "react";

import FormFieldDate from "../components/FormFieldDate";
import FormRowCentered from "../components/FormRowCentered";
import StepForm from "../components/StepForm";
import { Default as StepFormDefault } from "./StepForm.stories";

export default {
  title: "Form Fields/Date",
  component: FormFieldDate,
};

const Template = (args) => (
  <StepForm {...StepFormDefault.args}>
    <FormRowCentered>
      <FormFieldDate {...args} />
    </FormRowCentered>
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
