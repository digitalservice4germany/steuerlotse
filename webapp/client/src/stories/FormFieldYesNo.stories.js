import React from "react";

import FormFieldYesNo from "../components/FormFieldYesNo";
import StepForm from "../components/StepForm";
import { Default as StepFormDefault } from "./StepForm.stories";

export default {
  title: "Form Fields/YesNo",
  component: FormFieldYesNo,
};

const Template = (args) => (
  <StepForm {...StepFormDefault.args}>
    <FormFieldYesNo {...args} />
  </StepForm>
);

export const Default = Template.bind({});
Default.args = {
  fieldId: "yesNo",
  fieldName: "yesNo",
  defaultValue: undefined,
  label: {
    text: "Hat Han zuerst geschossen?",
  },
  errors: [],
};

export const YesPreselected = Template.bind({});
YesPreselected.args = {
  fieldId: "yesNo",
  fieldName: "yesNo",
  defaultValue: undefined,
  label: {
    text: "Hat Han zuerst geschossen?",
  },
  errors: [],
  value: "yes",
};

export const NoPreselected = Template.bind({});
NoPreselected.args = {
  fieldId: "yesNo",
  fieldName: "yesNo",
  defaultValue: undefined,
  label: {
    text: "Hat Han zuerst geschossen?",
  },
  errors: [],
  value: "no",
};

export const YesNoWithDetails = Template.bind({});
YesNoWithDetails.args = {
  fieldId: "yesNo",
  fieldName: "yesNo",
  defaultValue: undefined,
  label: {
    text: "Hat Han zuerst geschossen?",
  },
  errors: [],
  details: {
    title: "Warum diese Frage?",
    text: "Es gibt diese eine Szene in Episode IV.",
  },
  value: "no",
};
