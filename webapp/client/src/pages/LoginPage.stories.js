import React from "react";

import LoginPage from "./LoginPage";

export default {
  title: "Pages/Login",
  component: LoginPage,
};

const Template = (args) => <LoginPage {...args} />;

export const Primary = Template.bind({});
Primary.args = {};
