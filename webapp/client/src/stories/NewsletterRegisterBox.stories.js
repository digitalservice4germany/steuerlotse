import React from "react";
import NewsletterRegisterBox from "../components/NewsletterRegisterBox";

export default {
  title: "Components/Newsletter Register Box",
  component: NewsletterRegisterBox,
};

function Template(args) {
  return <NewsletterRegisterBox {...args} />;
}

export const Default = Template.bind({});
