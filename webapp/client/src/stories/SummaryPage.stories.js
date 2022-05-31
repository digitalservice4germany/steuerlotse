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
    section_steps: {
      mandatory_data: {
        data: {
          decl_incomes: {
            data: {
              "Keine weiteren Einkünfte vorhanden:": "Ja",
            },
            label: "Angabe zu weiteren Einkünften",
            url: "/lotse/step/decl_incomes?link_overview=True",
          },
          decl_edaten: {
            data: {
              "Einverständnis vorhanden:": "Ja",
            },
            label: "Übernahme vorliegender Daten",
            url: "/lotse/step/decl_edaten?link_overview=True",
          },
          familienstand: {
            data: {
              "Familienstand 2021:":
                "verheiratet / in eingetragener Lebenspartnerschaft",
              "seit dem:": "31.01.2000",
              "Vor dem 01.01.2022 dauernd getrennt gelebt:": "Nein",
              "Einverständnis Zusammenveranlagung:": "Ja",
            },
            label: "Familienstand",
            url: "/lotse/step/familienstand?link_overview=True",
          },
          steuernummer: {
            data: {
              "Steuernummer vorhanden:": "Ja",
              "Auswahl Bundesland:": "Bayern",
              "Steuernummer:": "19811310010",
            },
            label: "Steuernummer",
            url: "/lotse/step/steuernummer?link_overview=True",
          },
          person_a: {
            data: {
              " Steuer-Identifikationsnummer:": "04452397687",
              "Geburtsdatum:": "16.08.1950",
              "Vorname:": "Manfred",
              "Nachname:": "Mustername",
              "Straße:": "Steuerweg",
              "Hausnummer:": 42,
              "Hausnummerzusatz:": "a",
              "Adressergänzung:": "Seitenflügel",
              "Postleitzahl:": "20354",
              "Wohnort:": "Hamburg",
            },
            label: "Person A",
            url: "/lotse/step/person_a?link_overview=True",
          },
          has_disability_person_a: {
            data: {
              "Liegt eine Behinderung oder Pflegebedürftigkeit vor?:": "Ja",
            },
            label: "Behinderung oder Pflegebedürftigkeit für Person A",
            url: "/lotse/step/has_disability_person_a?link_overview=True",
          },
          merkzeichen_person_a: {
            data: {
              "Wurde ein Pflegegrad von 4 oder 5 festgestellt?:": "Nein",
              "Grad der Behinderung:": 80,
              "Merkzeichen G:": "Ja",
              "Merkzeichen Bl:": "Ja",
            },
            label:
              "Angaben zur festgestellten Behinderung oder Pflegebedürftigkeit Person A",
            url: "/lotse/step/merkzeichen_person_a?link_overview=True",
          },
          person_a_requests_pauschbetrag: {
            data: {
              "Beantragung Pauschbetrag für Menschen mit Behinderung:":
                "7400 Euro",
            },
            label: "Pauschbetrag für Menschen mit Behinderung für Person A",
            url: "/lotse/step/person_a_requests_pauschbetrag?link_overview=True",
          },
          person_a_requests_fahrtkostenpauschale: {
            data: {
              "Beantragung behinderungsbedingte Fahrtkostenpauschale:":
                "4500 Euro",
            },
            label: "Behinderungsbedingte Fahrtkostenpauschale für Person A",
            url: "/lotse/step/person_a_requests_fahrtkostenpauschale?link_overview=True",
          },
          person_b: {
            data: {
              "Steuer-Identifikationsnummer:": "02293417683",
              "Geburtsdatum:": "25.02.1951",
              "Vorname:": "Gerta",
              "Nachname:": "Mustername",
              "Mein Partner / Meine Partnerin und ich wohnen zusammen.:":
                "Mein Partner / Meine Partnerin und ich wohnen zusammen.",
              "Religionszugehörigkeit:": "Römisch-katholisch",
            },
            label: "Person B",
            url: "/lotse/step/person_b?link_overview=True",
          },
          has_disability_person_b: {
            data: {
              "Steuernummer vorhanden:": "Ja",
            },
            label: "Behinderung oder Pflegebedürftigkeit für Person B",
            url: "/lotse/step/has_disability_person_b?link_overview=True",
          },
          merkzeichen_person_b: {
            data: {
              "Wurde ein Pflegegrad von 4 oder 5 festgestellt?:": "Nein",
            },
            label:
              "Angaben zur festgestellten Behinderung oder Pflegebedürftigkeit Person B",
            url: "/lotse/step/merkzeichen_person_b?link_overview=True",
          },
          person_b_requests_pauschbetrag: {
            data: {
              "Beantragung Pauschbetrag für Menschen mit Behinderung:":
                "Kein Anspruch",
            },
            label: "Pauschbetrag für Menschen mit Behinderung für Person B",
            url: "/lotse/step/person_b_requests_pauschbetrag?link_overview=True",
          },
          iban: {
            data: {
              "Kontoinhaber:in:": "Person A",
              "IBAN:": "DE35133713370000012345",
            },
            label: "Bankverbindung",
            url: "/lotse/step/iban?link_overview=True",
          },
        },
      },
      section_steuerminderung: {
        data: {
          select_stmind: {
            data: {
              "Vorsorgeaufwendungen ausgewählt:": "Ja",
              "Krankheitskosten und weitere außergewöhnliche Belastungen ausgewählt:":
                "Ja",
              "Haushaltsnahe Dienstleistungen und Handwerkerleistungen ausgewählt:":
                "Ja",
              "Spenden und Mitgliedsbeiträge ausgewählt:": "Ja",
              "Steuern für Ihre Religionsgemeinschaft ausgwählt:": "Ja",
            },
            label: "Ihre Ausgaben",
            url: "/lotse/step/select_stmind?link_overview=True",
          },
          vorsorge: {
            data: {
              "Summe der Rechnungsbeträge:": "111.11 €",
            },
            label: "Vorsorgeaufwendungen",
            url: "/lotse/step/vorsorge?link_overview=True",
          },
          ausserg_bela: {
            data: {
              "Krankheitskosten Summe:": "1011.11 €",
              "Krankheitskosten Anspruch auf Erstattung:": "1011.12 €",
              "Pflegekosten Summe:": "2022.21 €",
              "Pflegekosten Anspruch auf Erstattung:": "2022.22 €",
              "Behinderungsbedingte Aufwendungen Summe:": "3033.31 €",
              "Behinderungsbedingte Aufwendungen Anspruch auf Erstattung:":
                "3033.32 €",
              "Bestattungskosten Summe:": "5055.51 €",
              "Bestattungskosten Anspruch auf Erstattung:": "5055.52 €",
              "Sonstige Außergewöhnliche Belastungen Summe:": "6066.61 €",
              "Sonstige Außergewöhnliche Belastungen Anspruch auf Erstattung:":
                "6066.62 €",
            },
            label: "Krankheitskosten und weitere außergewöhnliche Belastungen",
            url: "/lotse/step/ausserg_bela?link_overview=True",
          },
          haushaltsnahe_handwerker: {
            data: {
              "Haushaltsnahe Aufwendungen:": "Gartenarbeiten",
              "Summe der Rechnungsbeträge (Haushalt):": "500.00 €",
              "Handwerker Aufwendungen:": "Renovierung Badezimmer",
              "Summe der Rechnungsbeträge (Handwerker):": "200.00 €",
              "Betrag der Lohn-, Maschinen- und Fahrtkosten, inkl. USt:":
                "100.00 €",
            },
            label: "Haushaltsnahe Dienstleistungen und Handwerkerleistungen",
            url: "/lotse/step/haushaltsnahe_handwerker?link_overview=True",
          },
          spenden: {
            data: {
              "Spenden und Mitgliedsbeiträge:": "222.22 €",
              "an inländische politische Parteien:": "333.33 €",
            },
            label: "Spenden und Mitgliedsbeiträge",
            url: "/lotse/step/spenden?link_overview=True",
          },
          religion: {
            data: {
              "Geleistete Zahlungen:": "444.44 €",
              "Erhaltene Erstattungen:": "555.55 €",
            },
            label: "Steuern für Ihre Religionsgemeinschaft",
            url: "/lotse/step/religion?link_overview=True",
          },
        },
      },
    },
  },
  fields: {
    declarationSummary: {
      checked: false,
      errors: [],
    },
  },
  form: {
    ...StepFormDefault.args,
  },
  prevUrl: "test",
};
