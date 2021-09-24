import React from "react";

import FormNavButtons from "../components/FormNavButtons";

export default {
  title: "Forms/Nav Buttons",
  component: FormNavButtons,
};

const Template = (args) => <FormNavButtons {...args} />;

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
  explanatoryButtonText:
    'Sie haben Ihren Freischaltcode bereits erhalten? <br><a href="#">Dann können Sie sich anmelden</a>',
};
