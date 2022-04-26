import React from "react";
import RevocationSuccessPage from "../pages/RevocationSuccessPage";
import { baseDecorator } from "../../.storybook/decorators";

export default {
  title: "Pages/RevocationSuccess",
  component: RevocationSuccessPage,
  decorators: baseDecorator,
};

function Template(args) {
  return <RevocationSuccessPage {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  stepHeader: {
    title: "Stornierung erfolgreich",
    intro:
      "Ihr Freischaltcode wurde storniert. Wenn Sie einen Neuen beantragen wollen, fahren Sie mit dem nächsten Formular fort.",
  },
  prevUrl: "/unlock_code_revocation/step/data_input",
  nextUrl: "/unlock_code_request/step/data_input",
};
