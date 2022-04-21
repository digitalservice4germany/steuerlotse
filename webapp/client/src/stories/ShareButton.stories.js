import React from "react";
import ShareButtons from "../components/ShareButtons";

export default {
  title: "Anchor Elements/Share Button Group",
  component: ShareButtons,
};

function Template(args) {
  return <ShareButtons {...args} />;
}

export const Default = Template.bind({});

Default.args = {
  promoteUrl: "https://steuerlotse-rente.de",
  shareText:
    "Tipp: Mit dem Steuerlotse für Rente und Pension kannst du deine Steuererklärung einfach und unkompliziert machen. Ich habe es selbst ausprobiert!",
  mailSubject: "Hallo, schau dir das mal an: Steuerlotse für Rente und Pension",
  sourcePage: "Story",
};
