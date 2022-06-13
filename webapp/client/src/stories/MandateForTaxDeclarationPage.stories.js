import React from "react";
import { contentPageDecorator } from "../../.storybook/decorators";
import MandateForTaxDeclarationPage from "../pages/MandateForTaxDeclarationPage";

export default {
  title: "Content Pages/MandateForTaxDeclarationPage",
  component: MandateForTaxDeclarationPage,
  decorators: contentPageDecorator,
};

function Template() {
  return <MandateForTaxDeclarationPage />;
}

export const Default = Template.bind({});
