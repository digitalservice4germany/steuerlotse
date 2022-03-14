import React from "react";
import ShareIcons from "../components/ShareIcons";

export default {
  title: "Anchor Elements/Share Icons",
  component: ShareIcons,
};

function Template(args) {
  return <ShareIcons {...args} />;
}

export const Default = Template.bind({});

Default.args = {
  promoteUrl: "https://steuerlotse-rente.de",
  shareText:
    "Tipp: Mit dem Steuerlotse für Rente und Pension kannst du deine Steuererklärung einfach und unkompliziert machen. Ich habe es selbst ausprobiert!",
  mailSubject: "Hallo, schau dir das mal an: Steuerlotse für Rente und Pension",
  sourcePage: "Story",
};
