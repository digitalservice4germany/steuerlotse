import React from "react";

import FieldLabel from "../components/FieldLabel";

export default {
  title: "Form Fields/Label",
  component: FieldLabel,
};

const Template = (args) => <FieldLabel {...args} />;

export const Default = Template.bind({});
Default.args = {
  fieldId: "some-id",
  label: {
    text: "Ich bin ein Label",
  },
};

export const WithExtras = Template.bind({});
WithExtras.args = {
  ...Default.args,
  label: {
    text: "Ich bin ein Label",
    help: "Hilfetext sieht so aus",
    optional: true,
    exampleInput: "Beispiel-Input sieht so aus",
  },
  details: {
    title: "Details Überschrift",
    text: "Details Text",
  },
};
