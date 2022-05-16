import React from "react";
import SuccessStepsInfoBox from "../components/SuccessStepsInfoBox";

export default {
  title: "Components/StepsInfoBox",
  component: SuccessStepsInfoBox,
};

function Template(args) {
  return <SuccessStepsInfoBox {...args} />;
}

export const Default = Template.bind({});
