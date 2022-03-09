import React from "react";
import FilingFailurePage from "../pages/FilingFailurePage";

export default {
  title: "Pages/FilingFailurePageWithErrors",
  component: FilingFailurePage,
};

function Template(args) {
  return <FilingFailurePage {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  errorDetails: ["I am error number 1", "I am error number 2"],
};
