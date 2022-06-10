import React from "react";
import InfoBox from "../components/InfoBox";

export default {
  title: "Components/Info Box",
  component: InfoBox,
};

function Template(args) {
  return <InfoBox {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  boxHeadline: "Sie sind vorbereitet und haben Ihren Freischaltcode erhalten?",
  boxText:
    "Wenn Sie den Brief mit Ihrem Freischaltcode erhalten haben, starten Sie mit Ihrer Steuererklärung.",
  anchor: {
    url: "/unlock_code_request/step/data_input?link_overview=False",
    text: "Jetzt anmelden",
  },
};
