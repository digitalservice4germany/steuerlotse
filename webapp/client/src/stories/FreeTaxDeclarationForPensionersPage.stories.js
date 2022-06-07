import React from "react";
import { contentPageDecorator } from "../../.storybook/decorators";
import FreeTaxDeclarationForPensionersPage from "../pages/FreeTaxDeclarationForPensionersPage";

export default {
  title: "Content Pages/FreeTaxDeclarationForPensionersPage",
  component: FreeTaxDeclarationForPensionersPage,
  decorators: contentPageDecorator,
};

function Template() {
  return <FreeTaxDeclarationForPensionersPage />;
}

export const Default = Template.bind({});
