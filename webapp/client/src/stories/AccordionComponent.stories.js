import React from "react";

import AccordionComponent from "../components/AccordionComponent";

export default {
  title: "Form Fields/Accordion",
  component: AccordionComponent,
};

function Template(args) {
  return <AccordionComponent {...args} />;
}

export const Default = Template.bind({});

Default.args = {
  title: "Häufig gestellte Fragen zum Steuerlotsen",
  items: [
    {
      title: "Wer kann den Steuerlotsen nutzen?",
      detail:
        "Der Steuerlotse richtet sich an Personen und Paare, die eine Rente und Pension beziehen und keine Zusatzeinkünfte haben. Sie beziehen steuerpflichtige Nebeneinkünfte, zum Beispiel Einnahmen aus Vermietung oder aus einer selbständigen Tätigkeit? Dann können Sie den Steuerlotsen derzeit nicht nutzen. Sie können mit unserem Fragebogen prüfen, ob Sie alle Voraussetzungen für den Steuerlotsen erfüllen.",
    },
    {
      title: "Wie läuft die Nutzung des Steuerlotsen ab?",
      detail:
        "Wenn Sie verpflichtet sind eine Steuererklärung abzugeben, muss Ihre Einkommensteuererklärung bis zum 31. Juli 2022 beim Finanzamt sein. Sie können Ihre Steuererklärung auch nach der Frist noch einreichen. Warten Sie aber lieber nicht allzu lange. Es kann vorkommen, dass Ihr Finanzamt einen Verspätungszuschlag einfordert, wenn Sie sich zu viel Zeit lassen.",
    },
  ],
};
