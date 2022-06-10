import React from "react";
import ContentPageBox from "../components/ContentPageBox";

export default {
  title: "Components/Secondary ContentPageInfoBox",
  component: ContentPageBox,
};

function Template(args) {
  return <ContentPageBox {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  boxText: {
    headerOne: "Kann ich den Steuerlotsen für meine Steuererklärung nutzen?",
    headerTwo: "Wo finde ich mehr Informationen zum Steuerlotsen?",
  },
  anchor: {
    buttonOne: {
      url: "/eligibility/step/marital_status?link_overview=False",
      text: "Fragebogen starten",
      plausibleGoal: "contentPage_startQuestionnaire_clicked",
    },
    buttonTwo: {
      url: "/sofunktionierts",
      text: "Häufig gestellte Fragen",
      plausibleGoal: "contentPage_faq_clicked",
    },
    buttonThree: {
      url: "mailto:kontakt@steuerlotse-rente.de",
      text: "Kontaktieren Sie uns",
      plausibleGoal: "contentPage_contactUs_clicked",
    },
  },
};
