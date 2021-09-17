import React from "react";
import FormHeader from "./FormHeader";

export default {
  title: "Forms/Form Header",
  component: FormHeader,
  decorators: [
    (
      Story // Render context from app/templates/basis/base.html
    ) => (
      <div className="main-content">
        <div className="mt-4">
          <div className="col-lg-9 col-md-10 col-xs-12 p-0">
            <Story />
          </div>
        </div>
      </div>
    ),
  ],
};

const Template = (args) => <FormHeader {...args} />;

export const Primary = Template.bind({});
Primary.args = {
  title: "Melden Sie sich mit Ihrem Freischaltcode an",
  intro:
    "Sie sind vorbereitet und haben den Freischaltcode per Post erhalten? Dann können Sie mit Ihrer Steuererklärung 2020 beginnen.",
};
