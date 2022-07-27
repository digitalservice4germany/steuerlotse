import React from "react";
import HowItWorksPage from "../pages/HowItWorksPage";

export default {
  title: "Pages/HowItWorks Page",
  component: HowItWorksPage,
  parameters: {
    layout: "centered",
  },
};

function Template(args) {
  return <HowItWorksPage {...args} />;
}

export const Default = Template.bind({});
