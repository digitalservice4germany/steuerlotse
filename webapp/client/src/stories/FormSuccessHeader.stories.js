import React from "react";

import FormSuccessHeader from "../components/FormSuccessHeader";

export default {
  title: "Forms/SuccessHeader",
  component: FormSuccessHeader,
};

const Template = (args) => <FormSuccessHeader {...args} />;

export const Default = Template.bind({});
Default.args = {
  title: "Stornierung erfolgreich",
  intro:
    "Ihr Freischaltcode wurde stoniert. Wenn Sie einen Neuen beantragen wollen, fahren Sie mit dem nächsten Formular fort.",
};
