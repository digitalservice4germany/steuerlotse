import React from "react";
import LoginFailurePage from "../pages/LoginFailurePage";
import { baseDecorator } from "../../.storybook/decorators";

export default {
  title: "Pages/LoginFailure",
  component: LoginFailurePage,
  decorators: baseDecorator,
};

function Template(args) {
  return <LoginFailurePage {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  prevUrl: "/unlock_code_activation/step/data_input",
};
