import React from "react";
import SubmitAcknowledgePage from "../pages/SubmitAcknowledgePage";

export default {
  title: "Pages/SubmitAcknowledgePage",
  component: SubmitAcknowledgePage,
};

function Template(args) {
  return <SubmitAcknowledgePage {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  prevUrl: "/prev/url",
  logoutUrl: "/logout",
};
