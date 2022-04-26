import React from "react";

import FormFailureHeader from "../components/FormFailureHeader";
import { baseDecorator } from "../../.storybook/decorators";

export default {
  title: "Forms/FailureHeader",
  component: FormFailureHeader,
  decorators: baseDecorator,
};

function Template(args) {
  return <FormFailureHeader {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  title: "Anmeldung fehlgeschlagen",
  intro: "Ihr Freischaltcode konnte nicht validiert werden.",
};
