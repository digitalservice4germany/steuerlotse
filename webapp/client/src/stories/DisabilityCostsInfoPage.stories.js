import React from "react";
import DisabilityCostsInfoPage from "../pages/DisabilityCostsInfoPage";
import { contentPageDecorator } from "../../.storybook/decorators";

export default {
  title: "Content Pages/DisabilityCostsInfoPage",
  component: DisabilityCostsInfoPage,
  decorators: contentPageDecorator,
};

function Template() {
  return <DisabilityCostsInfoPage />;
}

export const Default = Template.bind({});
