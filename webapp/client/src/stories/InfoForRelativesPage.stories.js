import React from "react";
import InfoForRelativesPage from "../pages/InfoForRelativesPage";
import { contentPageDecorator } from "../../.storybook/decorators";

export default {
  title: "Content Pages/InfoForRelativesPage",
  component: InfoForRelativesPage,
  decorators: contentPageDecorator,
};

function Template() {
  return <InfoForRelativesPage />;
}

export const Default = Template.bind({});
