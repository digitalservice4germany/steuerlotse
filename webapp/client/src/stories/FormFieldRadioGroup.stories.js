import React from "react";

import FormFieldRadioGroup from "../components/FormFieldRadioGroup";
import StepForm from "../components/StepForm";
import { Default as StepFormDefault } from "./StepForm.stories";

export default {
  title: "Form Fields/RadioGroup",
  component: FormFieldRadioGroup,
};

function Template(args) {
  return (
    <StepForm {...StepFormDefault.args}>
      <FormFieldRadioGroup {...args} />
    </StepForm>
  );
}

export const Default = Template.bind({});
export const WithError = Template.bind({});
export const WithAutofocus = Template.bind({});
export const WithPreselectedValue = Template.bind({});
export const WithDetails = Template.bind({});
export const WithMoreRadioButtons = Template.bind({});

Default.args = {
  fieldId: "radio",
  fieldName: "radio",
  radioButtons: [
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

WithError.args = {
  ...Default.args,
  errors: ["Bitte wählen Sie eine Option aus um fortfahren zu können."],
};

WithAutofocus.args = {
  ...Default.args,
  autofocus: true,
};

WithPreselectedValue.args = {
  ...Default.args,
  value: "yes",
};

WithDetails.args = {
  ...Default.args,
  details: {
    title: "Was bedeutet das?",
    text: "Beantworten Sie die Frage mit »Ja«, wenn Sie Unterhalt an einen geschiedenen bzw. dauernd getrennt lebenden Partner oder an bedürftige Personen leisten oder selbst Unterhalt erhalten.",
  },
};

WithMoreRadioButtons.args = {
  ...Default.args,
  radioButtons: [
    { value: "yes", displayName: "Ja, ich zahle oder beziehe Unterhalt." },
    {
      value: "no",
      displayName: "Nein, weder zahle, noch beziehe ich Unterhalt.",
    },
    {
      value: "maybe",
      displayName: "Vielleicht zahle oder beziehe ich Unterhalt.",
    },
    {
      value: "unknown",
      displayName: "Ich weiß nicht ob ich Unterhalt bezahle oder beziehe.",
    },
  ],
};
