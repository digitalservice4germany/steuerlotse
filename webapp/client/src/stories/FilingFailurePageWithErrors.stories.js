import React from "react";
import FilingFailurePage from "../pages/FilingFailurePage";
import { baseDecorator } from "../../.storybook/decorators";

export default {
  title: "Pages/FilingFailurePageWithErrors",
  component: FilingFailurePage,
  decorators: baseDecorator,
};

function Template(args) {
  return <FilingFailurePage {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  errorDetails: ["I am error number 1", "I am error number 2"],
};
