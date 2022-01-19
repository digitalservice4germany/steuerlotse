import React from "react";

import LogoutPage from "../pages/LogoutPage";

export default {
  title: "Pages/LogoutPage",
  component: LogoutPage,
};

function Template(args) {
  return <LogoutPage {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  stepHeader: {
    title: "Sind Sie sicher, dass Sie sich abmelden möchten?",
    intro:
      "Ihre bisher eingetragenen Angaben werden erst an uns übermittelt, wenn Sie Ihre Steuererklärung verschicken. Ihre Steuererklärung wird daher nicht zwischengespeichert. Wenn Sie sich abmelden, kann es sein, dass Ihre Angaben bei der nächsten Anmeldung nicht mehr vorhanden sind.",
  },
  nextButtonLabel: "Abmelden",
  nextUrl: "/unlock_code_activation/step/data_input",
};
