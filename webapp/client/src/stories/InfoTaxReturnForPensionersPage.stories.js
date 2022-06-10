import React from "react";
import { contentPageDecorator } from "../../.storybook/decorators";
import InfoTaxReturnForPensionersPage from "../pages/InfoTaxReturnForPensionersPage";

export default {
  title: "Content Pages/InfoTaxReturnForPensionersPage",
  component: InfoTaxReturnForPensionersPage,
  decorators: contentPageDecorator,
};

function Template() {
  return <InfoTaxReturnForPensionersPage />;
}

export const Default = Template.bind({});
