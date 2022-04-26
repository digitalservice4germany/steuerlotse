import React from "react";
import FilingSuccessPage from "../pages/FilingSuccessPage";
import { baseDecorator } from "../../.storybook/decorators";

export default {
  title: "Pages/FilingSuccessPage",
  component: FilingSuccessPage,
  decorators: baseDecorator,
};

function Template(args) {
  return <FilingSuccessPage {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  nextUrl: "/lotse/step/ack",
  transferTicket: "et0453tpo67bku056b0kx5waznjbo0r8",
  downloadUrl: "/download_pdf",
};
