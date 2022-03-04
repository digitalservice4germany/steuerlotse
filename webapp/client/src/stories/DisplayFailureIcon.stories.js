import React from "react";
import DisplayFailureIcon from "../components/DisplayFailureIcon";

export default {
  title: "Anchor Elements/DisplayFailureIcon",
  component: DisplayFailureIcon,
};

function Template(args) {
  return <DisplayFailureIcon {...args} />;
}

export const Default = Template.bind({});

Default.args = {
  title: "Ihre Steuererklärung kann nicht übermittelt werden.",
};
