import React from "react";

import StepHeaderButtons from "../components/StepHeaderButtons";

export default {
  title: "Forms/Step Header Buttons",
  component: StepHeaderButtons,
};

function Template(args) {
  return <StepHeaderButtons {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  url: "#something",
};
