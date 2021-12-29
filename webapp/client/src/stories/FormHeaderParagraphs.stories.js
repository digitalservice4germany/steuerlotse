import React from "react";

import FormHeaderParagraphs from "../components/FormHeaderParagraphs";

export default {
  title: "Forms/HeaderParagraphs",
  component: FormHeaderParagraphs,
};

function Template(args) {
  return <FormHeaderParagraphs {...args} />;
}

export const Default = Template.bind({});
export const WithOneParagraph = Template.bind({});
export const WithoutParagraph = Template.bind({});

Default.args = {
  title: "Melden Sie sich mit Ihrem Freischaltcode an",
  intros: [
    "Sie sind vorbereitet und haben den Freischaltcode per Post erhalten?",
    "Dann können Sie mit Ihrer Steuererklärung 2021 beginnen.",
  ],
};

WithOneParagraph.args = {
  title: "Melden Sie sich mit Ihrem Freischaltcode an",
  intros: [
    "Sie sind vorbereitet und haben den Freischaltcode per Post erhalten?",
  ],
};

WithoutParagraph.args = {
  title: "Melden Sie sich mit Ihrem Freischaltcode an",
};
