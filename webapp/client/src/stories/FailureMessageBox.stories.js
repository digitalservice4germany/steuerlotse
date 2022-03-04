import React from "react";
import FailureMessageBox from "../components/FailureMessageBox";

export default {
  title: "Forms/FailureMessageBox",
  component: FailureMessageBox,
};

function Template(args) {
  return <FailureMessageBox {...args} />;
}

export const Default = Template.bind({});

Default.args = {
  title: "Ihre Steuererklärung kann nicht übermittelt werden.",
};
