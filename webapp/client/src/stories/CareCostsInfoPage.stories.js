import React from "react";
import CareCostsInfoPage from "../pages/CareCostsInfoPage";
import { contentPageDecorator } from "../../.storybook/decorators";

export default {
  title: "Content Pages/CareCostsInfoPage",
  component: CareCostsInfoPage,
  decorators: contentPageDecorator,
};

function Template() {
  return <CareCostsInfoPage />;
}

export const Default = Template.bind({});
