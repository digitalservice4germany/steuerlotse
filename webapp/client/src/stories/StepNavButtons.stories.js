import React from "react";

import StepNavButtons from "../components/StepNavButtons";

export default {
  title: "Forms/Nav Buttons",
  component: StepNavButtons,
};

const Template = (args) => <StepNavButtons {...args} />;

export const Default = Template.bind({});
Default.args = {};

export const WithOverviewLink = Template.bind({});
WithOverviewLink.args = {
  ...Default.args,
  showOverviewButton: true,
};

export const WithExplanatoryText = Template.bind({});
WithExplanatoryText.args = {
  ...Default.args,
  explanatoryButtonText: (
    <>
      Sie haben Ihren Freischaltcode bereits erhalten?
      <br />
      <a href="/">Dann können Sie sich anmelden</a>
    </>
  ),
};
