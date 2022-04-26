import React from "react";
import SubmitAcknowledgePage from "../pages/SubmitAcknowledgePage";
import { baseDecorator } from "../../.storybook/decorators";

export default {
  title: "Pages/SubmitAcknowledgePage",
  component: SubmitAcknowledgePage,
  decorators: baseDecorator,
};

function Template(args) {
  return <SubmitAcknowledgePage {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  prevUrl: "/prev/url",
  logoutUrl: "/logout",
};
