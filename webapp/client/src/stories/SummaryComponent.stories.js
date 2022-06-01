import React from "react";
import SummaryComponent from "../components/SummaryComponent";

export default {
  title: "Components/Summary Box Component",
  component: SummaryComponent,
};

function Template(args) {
  return <SummaryComponent {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  data: {
    data: {
      "Keine weiteren Einkünfte vorhanden:": "Ja",
    },
    label: "Angabe zu weiteren Einkünften",
    url: "/lotse/step/decl_incomes?link_overview=True",
  },
};
