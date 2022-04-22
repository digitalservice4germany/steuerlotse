import React from "react";
import KrankheitsKostenInfoPage from "../pages/KrankheitsKostenInfoPage";
import { contentPageDecorator } from "../../.storybook/decorators";

export default {
  title: "Content Pages/KrankheitskostenPage",
  component: KrankheitsKostenInfoPage,
  decorators: contentPageDecorator,
  args: {
    fscRequestUrl: "/unlock_code_request/step/data_input?link_overview=False",
    linkList: [
      {
        text: "Vorsorgeaufwendungen",
        url: "#",
      },
      {
        text: "Pflegekosten",
        url: "#",
      },
      {
        text: "Kosten aufgrund einer Behinderung",
        url: "#",
      },
      {
        text: "Bestattungskosten",
        url: "#",
      },
      {
        text: "Sonstige außergewöhnliche Belastungen",
        url: "#",
      },
      {
        text: "Haushaltsnahe Dienstleistungen",
        url: "#",
      },
      {
        text: "Handwerkerleistungen",
        url: "#",
      },
      {
        text: "Spenden und Mitgliedsbeiträge",
        url: "#",
      },
      {
        text: "Kirchensteuer",
        url: "#",
      },
    ],
  },
};

function Template(args) {
  return <KrankheitsKostenInfoPage {...args} />;
}

export const Default = Template.bind({});
