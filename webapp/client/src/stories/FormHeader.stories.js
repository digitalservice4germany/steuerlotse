import React from "react";

import FormHeader from "../components/FormHeader";

export default {
  title: "Forms/Header",
  component: FormHeader,
};

const Template = (args) => <FormHeader {...args} />;

export const Default = Template.bind({});
Default.args = {
  title: "Melden Sie sich mit Ihrem Freischaltcode an",
  intro:
    "Sie sind vorbereitet und haben den Freischaltcode per Post erhalten? Dann können Sie mit Ihrer Steuererklärung 2020 beginnen.",
};
