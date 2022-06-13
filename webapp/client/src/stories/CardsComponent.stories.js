import React from "react";
import CardsComponent from "../components/CardsComponent";

export default {
  title: "Components/Cards Component",
  component: CardsComponent,
};

function Template(args) {
  return <CardsComponent {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  cards: [
    {
      header: "Herausfinden, ob Sie den Steuerlotsen nutzen können",
      text: "Prüfen Sie durch die Beantwortung weniger Fragen, ob Sie die Voraussetzungen für die Nutzung des Steuerlotsen erfüllen.",
      url: "/eligibility/step/tax_year?link_overview=False",
    },
    {
      header: "Registrieren und Freischaltcode beantragen",
      text: "Mit Ihrer Registrierung beantragen Sie einen Freischaltcode. Dieser wird Ihnen nach erfolgreicher Beantragung von Ihrer Finanzverwaltung zugeschickt.",
      url: "/unlock_code_request/step/data_input?link_overview=False",
    },
    {
      header: "Mit Freischaltcode anmelden und Steuererklärung machen",
      text: "Sie sind vorbereitet und haben Ihren Freischaltcode erhalten? Dann können Sie mit Ihrer Steuererklärung 2021 beginnen.",
      url: "/unlock_code_activation/step/data_input?link_overview=False",
    },
  ],
};
