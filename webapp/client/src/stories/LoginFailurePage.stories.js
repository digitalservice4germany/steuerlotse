import React from "react";
import LoginFailurePage from "../pages/LoginFailurePage";

export default {
  title: "Pages/LoginFailure",
  component: LoginFailurePage,
};

function Template(args) {
  return <LoginFailurePage {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  stepHeader: {
    title: "Anmeldung fehlgeschlagen",
  },
  prevUrl: "/unlock_code_activation/step/data_input",
  registrationLink: "/unlock_code_request/step/start",
  revocationLink: "/unlock_code_revocation/step/start",
};
