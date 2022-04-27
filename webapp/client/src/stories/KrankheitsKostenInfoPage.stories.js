import React from "react";
import KrankheitsKostenInfoPage from "../pages/KrankheitsKostenInfoPage";
import { contentPageDecorator } from "../../.storybook/decorators";

export default {
  title: "Content Pages/KrankheitskostenPage",
  component: KrankheitsKostenInfoPage,
  decorators: contentPageDecorator,
};

function Template() {
  return <KrankheitsKostenInfoPage />;
}

export const Default = Template.bind({});
