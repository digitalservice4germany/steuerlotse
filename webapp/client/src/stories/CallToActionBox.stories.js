import React from "react";
import CallToActionBox from "../components/CallToActionBox";

export default {
  title: "Components/CallToActionBox",
  component: CallToActionBox,
};

function Template(args) {
  return <CallToActionBox {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  headline: "Haben Sie noch Fragen?",
  anchor: "/hilfebereich",
  variant: "",
  buttonText: "Schreiben Sie uns",
};

export const ButtonOutline = Template.bind({});
ButtonOutline.args = {
  headline: "Haben Sie noch Fragen?",
  anchor: "/hilfebereich",
  variant: "outline",
  buttonText: "Schreiben Sie uns",
};
