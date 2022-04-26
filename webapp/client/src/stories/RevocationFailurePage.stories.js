import React from "react";
import RevocationFailurePage from "../pages/RevocationFailurePage";
import { baseDecorator } from "../../.storybook/decorators";

export default {
  title: "Pages/RevocationFailure",
  component: RevocationFailurePage,
  decorators: baseDecorator,
};

function Template(args) {
  return <RevocationFailurePage {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  prevUrl: "/unlock_code_revocation/step/data_input",
};
