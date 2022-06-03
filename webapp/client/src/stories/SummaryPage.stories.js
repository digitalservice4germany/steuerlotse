import React from "react";
import SummaryPage from "../pages/SummaryPage";
import { Default as StepFormDefault } from "./StepForm.stories";

export default {
  title: "Pages/SummaryPage",
  component: SummaryPage,
};

function Template(args) {
  return <SummaryPage {...args} />;
}

export const Default = Template.bind({});
Default.args = {
  summaryData: {
    mandatoryData: [
      {
        data: [
          {
            name: "Keine weiteren Einkünfte vorhanden:",
            value: "Ja",
          },
        ],
        label: "Angabe zu weiteren Einkünften",
        url: "/lotse/step/decl_incomes?link_overview=True",
      },
      {
        data: [
          {
            name: "Einverständnis vorhanden:",
            value: "Ja",
          },
        ],
        label: "Übernahme vorliegender Daten",
        url: "/lotse/step/decl_edaten?link_overview=True",
      },
      {
        data: [
          {
            name: "Familienstand 2021:",
            value: "verheiratet / in eingetragener Lebenspartnerschaft",
          },
          {
            name: "seit dem:",
            value: "31.01.2000",
          },
          {
            name: "Vor dem 01.01.2022 dauernd getrennt gelebt:",
            value: "Nein",
          },
          {
            name: "Einverständnis Zusammenveranlagung:",
            value: "Ja",
          },
        ],
        label: "Familienstand",
        url: "/lotse/step/familienstand?link_overview=True",
      },
      {
        data: [
          {
            name: "Steuernummer vorhanden:",
            value: "Ja",
          },
          {
            name: "Auswahl Bundesland:",
            value: "Bayern",
          },
          {
            name: "Steuernummer:",
            value: "19811310010",
          },
        ],
        label: "Steuernummer",
        url: "/lotse/step/steuernummer?link_overview=True",
      },
      {
        data: [
          {
            name: "Steuer-Identifikationsnummer:",
            value: "04452397687",
          },
          {
            name: "Geburtsdatum:",
            value: "16.08.1950",
          },
          {
            name: "Vorname:",
            value: "Manfred",
          },
          {
            name: "Nachname:",
            value: "Mustername",
          },
          {
            name: "Straße:",
            value: "Steuerweg",
          },
          {
            name: "Hausnummer:",
            value: 42,
          },
          {
            name: "Hausnummerzusatz:",
            value: "a",
          },
          {
            name: "Adressergänzung:",
            value: "Seitenflügel",
          },
          {
            name: "Postleitzahl:",
            value: "20354",
          },
          {
            name: "Wohnort:",
            value: "Hamburg",
          },
        ],
        label: "Person A",
        url: "/lotse/step/person_a?link_overview=True",
      },
      {
        data: [
          {
            name: "Liegt eine Behinderung oder Pflegebedürftigkeit vor?:",
            value: "Ja",
          },
        ],
        label: "Behinderung oder Pflegebedürftigkeit für Person A",
        url: "/lotse/step/has_disability_person_a?link_overview=True",
      },
      {
        data: [
          {
            name: "Wurde ein Pflegegrad von 4 oder 5 festgestellt?:",
            value: "Nein",
          },
          {
            name: "Grad der Behinderung:",
            value: 80,
          },
          {
            name: "Merkzeichen G:",
            value: "Ja",
          },
          {
            name: "Merkzeichen Bl:",
            value: "Ja",
          },
        ],
        label:
          "Angaben zur festgestellten Behinderung oder Pflegebedürftigkeit Person A",
        url: "/lotse/step/merkzeichen_person_a?link_overview=True",
      },
      {
        data: [
          {
            name: "Beantragung Pauschbetrag für Menschen mit Behinderung:",
            value: "7400 Euro",
          },
          {
            name: "Grad der Behinderung:",
            value: 80,
          },
          {
            name: "Merkzeichen G:",
            value: "Ja",
          },
          {
            name: "Merkzeichen Bl:",
            value: "Ja",
          },
        ],
        label: "Pauschbetrag für Menschen mit Behinderung für Person A",
        url: "/lotse/step/person_a_requests_pauschbetrag?link_overview=True",
      },
      {
        data: [
          {
            name: "Beantragung behinderungsbedingte Fahrtkostenpauschale:",
            value: "4500 Euro",
          },
        ],
        label: "Behinderungsbedingte Fahrtkostenpauschale für Person A",
        url: "/lotse/step/person_a_requests_fahrtkostenpauschale?link_overview=True",
      },
      {
        data: [
          {
            name: "Steuer-Identifikationsnummer:",
            value: "02293417683",
          },
          {
            name: "Geburtsdatum:",
            value: "25.02.1951",
          },
          {
            name: "Vorname:",
            value: "Gerta",
          },
          {
            name: "Nachname:",
            value: "Mustername",
          },
          {
            name: "Mein Partner / Meine Partnerin und ich wohnen zusammen.:",
            value: "Mein Partner / Meine Partnerin und ich wohnen zusammen.",
          },
          {
            name: "Religionszugehörigkeit:",
            value: "Römisch-katholisch",
          },
        ],
        label: "Person B",
        url: "/lotse/step/person_b?link_overview=True",
      },
      {
        data: [
          {
            name: "Steuernummer vorhanden:",
            value: "Ja",
          },
        ],
        label: "Behinderung oder Pflegebedürftigkeit für Person B",
        url: "/lotse/step/has_disability_person_b?link_overview=True",
      },
      {
        data: [
          {
            name: "Wurde ein Pflegegrad von 4 oder 5 festgestellt?:",
            value: "Nein",
          },
        ],
        label:
          "Angaben zur festgestellten Behinderung oder Pflegebedürftigkeit Person B",
        url: "/lotse/step/merkzeichen_person_b?link_overview=True",
      },
      {
        data: [
          {
            name: "Beantragung Pauschbetrag für Menschen mit Behinderung:",
            value: "Kein Anspruch",
          },
        ],
        label: "Pauschbetrag für Menschen mit Behinderung für Person B",
        url: "/lotse/step/person_b_requests_pauschbetrag?link_overview=True",
      },
      {
        data: [
          {
            name: "Kontoinhaber:in:",
            value: "Person A",
          },
          {
            name: "IBAN:",
            value: "DE35133713370000012345",
          },
        ],
        label: "Bankverbindung",
        url: "/lotse/step/iban?link_overview=True",
      },
    ],
    sectionSteuerminderung: [
      {
        data: [
          {
            name: "Vorsorgeaufwendungen ausgewählt:",
            value: "Ja",
          },
          {
            name: "Krankheitskosten und weitere außergewöhnliche Belastungen ausgewählt:",
            value: "Ja",
          },
          {
            name: "Haushaltsnahe Dienstleistungen und Handwerkerleistungen ausgewählt:",
            value: "Ja",
          },
          {
            name: "Spenden und Mitgliedsbeiträge ausgewählt:",
            value: "Ja",
          },
          {
            name: "Wurde ein Pflegegrad von 4 oder 5 festgestellt?:",
            value: "Nein",
          },
          {
            name: "Steuern für Ihre Religionsgemeinschaft ausgwählt:",
            value: "Ja",
          },
        ],
        label: "Ihre Ausgaben",
        url: "/lotse/step/select_stmind?link_overview=True",
      },
    ],
  },
  fields: {
    confirmCompleteCorrect: {
      checked: false,
      errors: [],
    },
  },
  form: {
    ...StepFormDefault.args,
  },
  prevUrl: "test",
};
