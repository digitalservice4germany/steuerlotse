import React from "react";
import { contentPageDecorator } from "../../.storybook/decorators";
import ChurchTaxInfoPage from "../pages/ChurchTaxInfoPage";

export default {
  title: "Content Pages/ChurchTaxInfoPage",
  component: ChurchTaxInfoPage,
  decorators: contentPageDecorator,
};

function Template() {
  return <ChurchTaxInfoPage />;
}

export const Default = Template.bind({});
