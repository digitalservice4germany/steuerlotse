import React from "react";

import SessionNotePage from "../pages/SessionNotePage";

export default {
  title: "Pages/SessionNote",
  component: SessionNotePage,
};

function Template(args) {
  return <SessionNotePage {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  form: {
    action: "#form-submit",
    csrfToken: "abc123imacsrftoken",
    showOverviewButton: true,
  },
  prevUrl: "/previous/step",
};
