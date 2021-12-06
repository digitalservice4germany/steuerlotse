import React from "react";

import FormFieldYesNo from "../components/FormFieldYesNo";
import StepForm from "../components/StepForm";
import { Default as StepFormDefault } from "./StepForm.stories";

export default {
  title: "Form Fields/YesNo",
  component: FormFieldYesNo,
};

function Template(args) {
  <StepForm {...StepFormDefault.args}>
    <FormFieldYesNo {...args} />
  </StepForm>;
}

export const Default = Template.bind({});
Default.args = {
  fieldId: "yesNo",
  fieldName: "yesNo",
  label: {
    text: "Haben Sie eine Steuernummer?",
  },
  errors: [],
};

export const YesPreselected = Template.bind({});
YesPreselected.args = {
  ...Default.args,
  value: "yes",
};

export const NoPreselected = Template.bind({});
NoPreselected.args = {
  ...Default.args,
  value: "no",
};

export const WithDetails = Template.bind({});
WithDetails.args = {
  ...Default.args,
  details: {
    title: "Warum diese Frage?",
    text: "Wenn Sie keine Steuernummer haben, dann müssen Sie eine neue Steuernummer beantragen.",
  },
};

export const YesNoWithChangeHandler = Template.bind({});
YesNoWithChangeHandler.args = {
  ...Default.args,
  onChangeHandler: (event) => {
    if (event.target.value === "yes") {
      alert("Sie haben eine Steuernummer!");
    } else {
      alert("Sie haben keine Steuernummer!");
    }
  },
};
