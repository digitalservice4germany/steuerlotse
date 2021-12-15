import React from "react";

import FormFieldRadio from "../components/FormFieldRadio";
import StepForm from "../components/StepForm";
import { Default as StepFormDefault } from "./StepForm.stories";

export default {
  title: "Form Fields/Radio",
  component: FormFieldRadio,
};

function Template(args) {
  return (
    <StepForm {...StepFormDefault.args}>
      <FormFieldRadio {...args} />
    </StepForm>
  );
}

export const Default = Template.bind({});
Default.args = {
  fieldId: "radio",
  fieldName: "radio",
  options: [
    { value: "yes", displayName: "Ja, ich zahle oder beziehe Unterhalt." },
    {
      value: "no",
      displayName: "Nein, weder zahle, noch beziehe ich Unterhalt.",
    },
  ],
  label: {
    text: "Zahlen oder beziehen Sie Unterhalt?",
  },
  errors: [],
};
