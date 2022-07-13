import React from "react";
import HelpAreaPage from "../pages/HelpAreaPage";

export default {
  title: "Pages/HelpArea Page",
  component: HelpAreaPage,
};

function Template(args) {
  return <HelpAreaPage {...args} />;
}

export const Default = Template.bind({});
