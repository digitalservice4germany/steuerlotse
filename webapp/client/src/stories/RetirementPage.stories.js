import React from "react";
import RetirementPage from "../pages/RetirementPage";

export default {
  title: "Pages/Retirement Page",
  component: RetirementPage,
};

function Template(args) {
  return <RetirementPage {...args} />;
}

export const Default = Template.bind({});
