const translations = {
  errors: {
    warningImage: {
      ariaLabel: "Fehlermeldung",
    },
  },
  button: {
    help: {
      ariaLabel: "Weitere Informationen",
    },
    close: {
      ariaLabel: "Schließen",
    },
  },
  form: {
    optional: "optional",
    back: "Zurück",
    backToOverview: "Zurück zur Übersicht",
    next: "Weiter",
  },
  lotse: {
    fieldDeclarationIncomes: {
      fieldConfirmIncomes:
        "Hiermit erkläre ich / erklären wir, dass ich / wir im Steuerjahr 2020 keine weiteren Einkünfte hatte / hatten, außer der oben aufgeführten Einkünfte.",
    },
    declarationIncomes: {
      listItem1:
        "Renteneinkünfte und / oder Pensionen, die von den Rentenversicherungsträgern oder vom Arbeitgeber elektronisch gemeldet worden sind, und ggf.",
      listItem2:
        "Kapitaleinkünfte, von denen bereits Abgeltungsteuer an das Finanzamt abgeführt oder für die der Sparer-Pauschbetrag in Anspruch genommen wurde (Freistellungsauftrag), und ggf.",
      listItem3:
        "pauschal besteuerte Einkünfte aus geringfügigen Beschäftigungen (Mini-Jobs) bis zu einer Höhe von insgesamt 450 Euro monatlich",
    },
    confirmation: {
      fieldRegistrationConfirmDataPrivacy: {
        labelText:
          "Ich habe die <dataPrivacyLink>Datenschutzerklärung</dataPrivacyLink> inklusive der <taxGdprLink>Allgemeinen Informationen zur Umsetzung der datenschutzrechtlichen Vorgaben der Artikel 12 bis 14 der Datenschutz-Grundverordnung in der Steuerverwaltung</taxGdprLink> zur Kenntnis genommen und akzeptiere diese.",
      },
      fieldRegistrationConfirmTermsOfService: {
        labelText:
          "Ich habe die <termsOfServiceLink>Nutzungsbedingungen</termsOfServiceLink> gelesen und stimme ihnen zu.",
      },
      finish: "Steuererklärung abgeben",
    },
  },
  unlockCodeActivation: {
    idnr: {
      labelText: "Steuer-Identifikationsnummer",
      help: {
        title: "Wo finde ich diese Nummer?",
        text: "Die 11-stellige Nummer haben Sie mit einem Brief vom Bundeszentralamt für Steuern erhalten. Die Nummer steht oben rechts groß auf dem Brief. Alternativ finden Sie diese Nummer auch auf Ihrem letzten Steuerbescheid.",
      },
    },
    unlockCode: {
      labelText: "Freischaltcode",
      help: {
        title: "Wo finde ich diese Nummer?",
        text: "Wenn Sie sich beim Steuerlotsen erfolgreich registriert haben, bekommen Sie von Ihrer Finanzverwaltung einen Brief mit Ihrem persönlichen Freischaltcode zugeschickt. Den Freischaltcode finden Sie auf der letzten Seite des Briefes.",
      },
    },
  },
  unlockCodeRequest: {
    dob: {
      labelText: "Geburtsdatum",
    },
    dataPrivacyAndAgb: {
      title: "Datenschutzerklärung und Nutzungsbedingungen",
    },
    fieldRegistrationConfirmDataPrivacy: {
      labelText:
        "Ich habe die <dataPrivacyLink>Datenschutzerklärung</dataPrivacyLink> inklusive der <taxGdprLink>Allgemeinen Informationen zur Umsetzung der datenschutzrechtlichen Vorgaben der Artikel 12 bis 14 der Datenschutz-Grundverordnung in der Steuerverwaltung</taxGdprLink> zur Kenntnis genommen und akzeptiere diese.",
    },
    fieldRegistrationConfirmTermsOfService: {
      labelText:
        "Ich habe die <termsOfServiceLink>Nutzungsbedingungen</termsOfServiceLink> gelesen und stimme ihnen zu.",
    },
    fieldRegistrationConfirmIncomes: {
      labelText:
        "Ich habe unter <eligibilityLink>Nutzung prüfen</eligibilityLink> den Fragebogen ausgewertet und erfülle alle Voraussetzungen für die Nutzung des Steuerlotsen.",
    },
    fieldRegistrationConfirmEData: {
      labelText:
        "Ich bzw. wir sind damit einverstanden, dass die Festsetzung meiner / unserer Einkommensteuer anhand der elektronisch vorliegenden Daten erfolgt, die der Finanzbehörde vorliegen.",
    },
    eData: {
      title: "Einverständnis zur automatischen Übernahme vorliegender Daten",
      helpTitle: "Was bedeutet das?",
      helpText:
        "Daten zu beispielsweise <bold>Renten, Pensionen oder Kranken- und Pflegeversicherungen</bold> erhält die Steuerverwaltung vom jeweiligen Träger elektronisch. Diese Daten werden vom Finanzamt automatisch übernommen und müssen von Ihnen nicht in diese Steuererklärung eingetragen werden. Welche Beträge über Sie übermittelt wurden, können Sie den Bescheiden entnehmen, die Sie von der jeweiligen Stelle per Post erhalten haben. Die Daten kommen aus der gleichen Quelle. Sollten Sie mit der Übernahme nicht einverstanden sein, können Sie die vereinfachte Steuererklärung leider nicht nutzen.",
    },
    gotFsc:
      "Sie haben Ihren Freischaltcode bereits erhalten? <br><loginLink>Dann können Sie sich anmelden</loginLink>.",
    input: {
      intro:
        "Mit Ihrer Registrierung beantragen Sie einen Freischaltcode bei Ihrer Finanzverwaltung. Sie erhalten diesen mit einem Brief <bold>innerhalb von zwei Wochen</bold> nach erfolgreicher Beantragung. Wenn Sie die Zusammenveranlagung nutzen möchten, muss sich nur eine Person registrieren.",
    },
  },
  dateField: {
    day: "Tag",
    month: "Monat",
    year: "Jahr",
  },
  fields: {
    dateField: {
      exampleInput: {
        text: "z.B. 29.2.1951",
      },
    },
  },
  stmindSelection: {
    selectVorsorge: {
      label: {
        title: "Vorsorgeaufwendungen",
        text: "Beiträge zu bestimmten Versicherungen, mit denen Sie für Ihre Zukunft vorsorgen, sind Vorsorgeaufwendungen. Hierzu zählen Unfallversicherungen, Haftpflichtversicherungen und bestimmte Risikolebensversicherungen.",
      },
    },
    selectAussergBela: {
      label: {
        title: "Krankheitskosten und weitere außergewöhnliche Belastungen",
        text: "Hierzu zählen beispielsweise Kosten, die durch Krankheit, Unwetter oder Naturkatastrophen entstanden sind.",
      },
    },
    selectHandwerker: {
      label: {
        title: "Haushaltsnahe Dienstleistungen und Handwerkerleistungen",
        text: "Hierzu zählen beispielsweise Aufwendungen für Reinigung, Winterdienst, Gartenarbeit, Handwerker, Schornsteinfeger, Pflegeleistungen oder die Betreuung von Haustieren.",
      },
    },
    selectSpenden: {
      label: {
        title: "Spenden und Mitgliedsbeiträge",
        text: "Wählen Sie diesen Punkt aus, wenn Sie einen gemeinnützigen Verein, eine Stiftung, Partei oder Wählervereinigungen unterstützt haben.",
      },
    },
    selectReligion: {
      label: {
        title: "Steuern für Ihre Religionsgemeinschaft",
        text: "Im Jahr 2020 geleistete Steuern für eine Religionsgemeinschaft – nach Abzug der vom Finanzamt erstatteten Beträge – können Sie als Sonderausgaben angeben.",
      },
    },
  },
};

export default translations;
