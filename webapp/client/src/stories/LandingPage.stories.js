import React from "react";
import LandingPage from "../pages/LandingPage";

export default {
  title: "Pages/Landing Page",
  component: LandingPage,
};

function Template(args) {
  return <LandingPage {...args} />;
}

export const Default = Template.bind({});
