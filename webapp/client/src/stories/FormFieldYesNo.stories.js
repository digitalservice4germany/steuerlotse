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
    text: "Haben Sie eine Steuernummer?",
  },
  errors: [],
};

export const YesPreselected = Template.bind({});
YesPreselected.args = {
  fieldId: "yesNo",
  fieldName: "yesNo",
  defaultValue: undefined,
  label: {
    text: "Haben Sie eine Steuernummer?",
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
    text: "Haben Sie eine Steuernummer?",
  },
  errors: [],
  value: "no",
};

export const WithDetails = Template.bind({});
WithDetails.args = {
  fieldId: "yesNo",
  fieldName: "yesNo",
  defaultValue: undefined,
  label: {
    text: "Haben Sie eine Steuernummer?",
  },
  errors: [],
  details: {
    title: "Warum diese Frage?",
    text: "Wenn Sie keine Steuernummer haben, dann müssen Sie eine neue Steuernummer beantragen.",
  },
  value: "no",
};

export const YesNoWithChangeHandler = Template.bind({});
YesNoWithChangeHandler.args = {
  fieldId: "yesNo",
  fieldName: "yesNo",
  defaultValue: undefined,
  label: {
    text: "Haben Sie eine Steuernummer?",
  },
  errors: [],
  value: "no",
  onChangeHandler: (event) => {
    if (event.target.value === "yes") {
      alert("Sie haben eine Steuernummer!");
    } else {
      alert("Sie haben keine Steuernummer!");
    }
  },
};
