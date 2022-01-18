import React from "react";
import RevocationFailurePage from "../pages/RevocationFailurePage";

export default {
  title: "Pages/RevocationFailure",
  component: RevocationFailurePage,
};

function Template(args) {
  return <RevocationFailurePage {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  prevUrl: "/unlock_code_revocation/step/data_input",
};
