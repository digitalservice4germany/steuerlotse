import React from "react";
import ReplacementCostsInfoPage from "../pages/ReplacementCostsInfoPage";
import { contentPageDecorator } from "../../.storybook/decorators";

export default {
  title: "Content Pages/ReplacementCostsInfoPage",
  component: ReplacementCostsInfoPage,
  decorators: contentPageDecorator,
};

function Template() {
  return <ReplacementCostsInfoPage />;
}

export const Default = Template.bind({});
