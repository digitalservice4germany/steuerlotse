import React from "react";

import StepForm from "../components/StepForm";

export default {
  title: "Forms/Step Form",
  component: StepForm,
};

function Template(args) {
  return <StepForm {...args}>&lt;Form fields will go here&gt;</StepForm>;
}

export const Default = Template.bind({});
Default.args = {
  action: "#form-submit",
  csrfToken: "abc123imacsrftoken",
};
