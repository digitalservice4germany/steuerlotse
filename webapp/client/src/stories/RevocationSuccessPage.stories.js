import React from "react";
import RevocationSuccessPage from "../pages/RevocationSuccessPage";

export default {
  title: "Pages/RevocationSuccess",
  component: RevocationSuccessPage,
};

const Template = (args) => <RevocationSuccessPage {...args} />;

export const Default = Template.bind({});
Default.args = {
  stepHeader: {
    title: "Stornierung erfolgreich",
    intro:
      "Ihr Freischaltcode wurde storniert. Wenn Sie einen Neuen beantragen wollen, fahren Sie mit dem nächsten Formular fort.",
  },
};
