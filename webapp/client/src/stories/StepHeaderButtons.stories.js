import React from "react";

import StepHeaderButtons from "../components/StepHeaderButtons";

export default {
  title: "Forms/Step Header Buttons",
  component: StepHeaderButtons,
};

const Template = (args) => <StepHeaderButtons {...args} />;

export const Default = Template.bind({});
Default.args = {
  url: "#something",
};
