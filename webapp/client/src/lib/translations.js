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
  dropDown: {
    defaultOption: "Bitte auswählen",
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
        "Hiermit erkläre ich / erklären wir, dass ich / wir im Steuerjahr 2021 keine weiteren Einkünfte hatte / hatten, außer der oben aufgeführten Einkünfte.",
    },
    declarationIncomes: {
      listItem1:
        "inländische Renteneinkünfte und / oder Pensionen, die von den Rentenversicherungsträgern oder vom Arbeitgeber elektronisch gemeldet worden sind, und ggf.",
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
    taxNumber: {
      taxNumberExists: {
        labelText_one: "Haben Sie bereits eine Steuernummer?",
        labelText_other: "Haben Sie bereits eine gemeinsame Steuernummer?",
        help: {
          title: "Wo finde ich diese Nummer?",
          text: "Sie finden Ihre Steuernummer auf jedem Steuerbescheid. Sollten Sie noch keine Steuererklärung abgegeben haben, können Sie eine neue Steuernummer beantragen. Bitte beachten Sie, dass die Steuernummer und die Steuer-Identifikationsnummer zwei verschiedene Nummern sind.",
        },
      },
      bundesland: {
        labelText: "Wählen Sie Ihr Bundesland",
      },
      taxOffices: {
        labelText: "Wählen Sie Ihr Finanzamt",
      },
      taxNumberInput: {
        label: {
          labelText: "Steuernummer",
          exampleInput: "Muss 10 oder 11 Ziffern haben",
        },
      },
      requestNewTaxNumber: {
        labelText_one:
          "Hiermit bestätige ich, dass ich noch keine Steuernummer bei meinem Finanzamt habe und eine neue Steuernummer beantragen möchten.",
        labelText_other:
          "Hiermit bestätigen wir, dass wir noch keine Steuernummer bei unserem Finanzamt haben und eine neue Steuernummer beantragen möchten.",
        headline: "Neue Steuernummer beantragen",
        intro:
          "Mit der Abgabe der Steuererklärung wird eine neue Steuernummer beim zuständigen Finanzamt beantragt. Die neue Steuernummer wird Ihnen dann mit dem Steuerbescheid mitgeteilt.",
      },
    },
    hasDisability: {
      intro_single:
        "Im Falle einer Behinderung oder Pflegebedürftigkeit können erhöhte Kosten für Medikamente und Betreuung anfallen. Damit diese Ausgaben Sie nicht zu sehr belasten, können Sie steuerliche Vergünstigungen in Anspruch nehmen.",
      intro_person_a:
        "Im Falle einer Behinderung oder Pflegebedürftigkeit können erhöhte Kosten für Medikamente und Betreuung anfallen. Damit diese Ausgaben Sie nicht zu sehr belasten, können Sie steuerliche Vergünstigungen für Person A in Anspruch nehmen.",
      intro_person_b:
        "Im Falle einer Behinderung oder Pflegebedürftigkeit können erhöhte Kosten für Medikamente und Betreuung anfallen. Damit diese Ausgaben Sie nicht zu sehr belasten, können Sie steuerliche Vergünstigungen für Person B in Anspruch nehmen.",
      details: {
        title: "Infos zu den steuerlichen Vergünstigungen",
        text: "Bei einer Behinderung besteht in der Regel Anspruch auf den <bold>Pauschbetrag für Menschen mit Behinderung.</bold> Die Höhe des Pauschbetrags ist vom Grad der Behinderung abhängig. Menschen mit Behinderung können unter bestimmten Voraussetzungen außerdem eine <bold>Pauschale für Fahrtkosten</bold> beantragen. Wählen Sie hier aus, ob Sie Angaben zu einer Behinderung machen möchten.",
      },
    },
    merkzeichen: {
      hasPflegegrad: {
        label: "Wurde ein Pflegegrad 4 oder 5 festgestellt?",
      },
      disabilityDegree: {
        label: "Grad der Behinderung",
        example: "ab 20",
      },
      merkzeichen: {
        label: "Merkzeichen",
        details: {
          title: "Infos zu den Merkzeichen",
          text: "Im Schwerbehindertenausweis, den man ab einem Grad der Behinderung von 50 und mehr erhalten kann, werden spezifische Behinderungen und bestimmte gesundheitliche Einschränkungen durch Merkzeichen kenntlich gemacht. Viele Nachteilsausgleiche für schwerbehinderte Menschen sind an bestimmte Merkzeichen gekoppelt. Sollten Sie kein Merkzeichen haben, lassen Sie das Feld frei.",
        },
      },
      hasMerkzeichenH: {
        label: "Merkzeichen H",
      },
      hasMerkzeichenG: {
        label: "Merkzeichen G",
      },
      hasMerkzeichenBl: {
        label: "Merkzeichen Bl",
      },
      hasMerkzeichenTbl: {
        label: "Merkzeichen TBl",
      },
      hasMerkzeichenAg: {
        label: "Merkzeichen aG",
      },
    },
    noPauschbetrag: {
      intro: {
        p1: "Ein Pauschbetrag wird erst ab einem Grad der Behinderung von 20 gewährt. Liegt der Grad der Behinderung darunter, gibt es keinen Anspruch auf einen Pauschbetrag.",
        p2: "<bold>Hinweis:</bold> Auch ohne Pauschbetrag können Sie behinderungsbedingte Aufwendungen absetzen. Und zwar im Bereich Krankheitskosten und weitere außergewöhnliche Belastungen.",
      },
    },
    pauschbetrag: {
      intro:
        "Auf Basis Ihrer Angaben haben Sie Anspruch auf den Pauschbetrag für Menschen mit Behinderung. <bold>Alternativ können die tatsächlichen Kosten</bold>, die in Zusammenhang mit Ihrer Behinderung entstanden sind, einzeln angegeben werden. Wählen Sie aus, ob Sie den Pauschbetrag in Anspruch nehmen möchten.",
      details: {
        title: "Welche Kosten sind damit abgegolten?",
        p1: "Den Pauschbetrag erhalten Sie für die Mehraufwendungen, die erfahrungsgemäß durch ihre Krankheit bzw. Behinderung entstehen. Hierzu zählen Aufwendungen für",
        p2: "Sind Ihre tatsächlichen Kosten, die auf Grund der Behinderung entstanden sind, höher als der Behinderten-Pauschbetrag, ist es sinnvoll die tatsächlichen Kosten anzugeben. Das können Sie im Bereich „Krankheitskosten und weitere außergewöhnliche Belastungen” machen.",
        p3: "<bold>Wichtig</bold>: In diesem Fall werden die tatsächlichen Aufwendungen um die zumutbare Belastung gekürzt.",
        p4: "Außerordentliche Kosten sind auch neben dem Pauschbetrag gesondert zu berücksichtigen, wenn sie zwar mit der Körperbehinderung zusammenhängen, sich jedoch in Folge ihrer Einmaligkeit der Typisierung des §  33b Abs. 3 EStG entziehen.",
        list: {
          listItem1:
            "die Hilfe bei den gewöhnlichen und regelmäßig wiederkehrenden Verrichtungen des täglichen Lebens",
          listItem2: "die eigene Pflege und",
          listItem3: "einen erhöhten Wäschebedarf.",
        },
      },
      requestPauschbetrag: {
        yes: "Pauschbetrag in Höhe von <bold>{{pauschbetrag}} Euro</bold> beantragen",
        no: "Pauschbetrag nicht beantragen",
      },
    },
    fahrtkostenpauschale: {
      introText:
        "Auf Basis Ihrer Angaben haben Sie Anspruch auf die behinderungsbedingte Fahrtkostenpauschale von <bold>{{fahrtkostenpauschaleAmount}} Euro abzüglich der zumutbaren Belastung</bold>. Einzelne Fahrten können Sie nicht mehr geltend machen.",
      requestsFahrtkostenpauschale: {
        yesLabel: "Pauschale beantragen",
        noLabel: "Pauschale nicht beantragen",
      },
      helpTitle: "Hinweis zur zumutbaren Belastung",
      helpText:
        "Nur der Betrag, der höher ist als Ihre zumutbare Belastung, wirkt sich steuermindernd aus. Die zumutbare Belastung hängt unter anderem von der Höhe Ihres Einkommens ab und wird von Ihrem Finanzamt automatisch berechnet.",
    },
    telephoneNumber: {
      fieldTelephoneNumber: {
        label: "Telefonnummer",
      },
    },
    stmindSelection: {
      selectVorsorge: {
        label: {
          title: "Vorsorgeaufwendungen",
          text: "Viele Versicherungen, mit denen Sie für Ihre Zukunft vorsorgen, können Sie von der Steuer absetzen. Hierzu zählen z.B. Unfallversicherungen, Haftpflichtversicherungen und bestimmte Risikolebensversicherungen.",
        },
      },
      selectAussergBela: {
        label: {
          title: "Krankheitskosten und weitere außergewöhnliche Belastungen",
          text: "In diesen Bereich fallen z.B. Aufwendungen, die durch Krankheit, Kur, eine Behinderung, Pflege, Bestattung, Unwetter oder durch Naturkatastrophen entstanden sind.",
        },
      },
      selectHandwerker: {
        label: {
          title: "Haushaltsnahe Dienstleistungen und Handwerkerleistungen",
          text: "Zu den Kosten für haushaltsnahe Dienst- und Handwerkerleistungen zählen z.B. Leistungen für Reinigung, Winterdienst, Gartenarbeit, Handwerker, Schornsteinfeger, Pflegeleistungen oder die Betreuung von Haustieren.",
        },
      },
      selectSpenden: {
        label: {
          title: "Spenden und Mitgliedsbeiträge",
          text: "An dieser Stellen können Sie Spenden und Mitgliedsbeiträge für steuerbegünstigte Zwecke angeben. Hierzu zählen z.B. Zahlungen an steuerbegünstigte Vereine, Stiftungen und inländische Parteien.",
        },
      },
      selectReligion: {
        label: {
          title: "Steuern für Ihre Religionsgemeinschaft",
          text: "Im Veranlagungsjahr 2021 gezahlte Steuern für Ihre Religionsgemeinschaft können Sie als sogenannte Sonderausgaben angeben.",
        },
      },
    },
  },
  unlockCodeActivation: {
    unlockCode: {
      labelText: "Freischaltcode",
      help: {
        title: "Wo finde ich diese Nummer?",
        text: "Wenn Sie sich beim Steuerlotsen erfolgreich registriert haben, bekommen Sie von Ihrer Finanzverwaltung einen Brief mit Ihrem persönlichen Freischaltcode zugeschickt. Den Freischaltcode finden Sie auf der letzten Seite des Briefes.",
      },
    },
    failure: {
      causes: {
        title: "Mögliche Ursachen",
        reasons1:
          "Ihr Freischaltcode ist nicht korrekt. Eine Ursache kann die Verwechslung von Ziffern oder Buchstaben sein, die sich ähneln. So kann die Ziffer 0 schnell mit dem Buchstaben O oder der Buchstabe B schnell mit der Ziffer 8 verwechselt werden. Prüfen Sie Ihre Angabe.",
        reasons2:
          "Haben Sie sich vor 90 Tagen registriert? In diesem Fall können Sie sich mit diesem Freischaltcode nicht mehr beim Steuerlotsen anmelden. <registrationLink>Registrieren</registrationLink> Sie sich bitte erneut. Sie erhalten dann einen Brief mit einem neuen Freischaltcode.",
        reasons3:
          "Ihre Anmeldung ist bereits mehr als 5 Mal fehlgeschlagen. Dann ist Ihr Freischaltcode nicht mehr gültig. Bitte <revocationLink>stornieren</revocationLink> Sie Ihren Freischaltcode und <registrationLink>registrieren</registrationLink> sich erneut. Sie erhalten dann einen Brief mit einem neuen Freischaltcode.",
      },
    },
  },
  unlockCodeRequest: {
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
        "Daten zu beispielsweise <bold>inländischen Renten, Pensionen oder Kranken- und Pflegeversicherungen</bold> erhält die Steuerverwaltung vom jeweiligen Träger elektronisch. Diese Daten werden vom Finanzamt automatisch übernommen und müssen von Ihnen nicht in diese Steuererklärung eingetragen werden. Welche Beträge über Sie übermittelt wurden, können Sie den Bescheiden entnehmen, die Sie von der jeweiligen Stelle per Post erhalten haben. Die Daten kommen aus der gleichen Quelle. Sollten Sie mit der Übernahme nicht einverstanden sein, können Sie die vereinfachte Steuererklärung leider nicht nutzen.",
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
  register: {
    success: {
      "next-steps": {
        heading: "So geht es weiter",
        "step-1":
          "Sie bekommen von Ihrem Finanzamt den <bold>Brief mit Ihrem persönlichen Freischaltcode</bold> zugeschickt.",
        "step-2":
          "Sie können sich auf Ihre Steuererklärung vorbereiten bis Sie den Brief erhalten haben. Sammeln Sie dazu alle notwendigen Unterlagen sowie Belege. Eine Übersicht über die notwendigen Unterlagen, die Sie für die Erstellung Ihrer Steuererklärung brauchen, finden Sie in unserer <vorbereitungshilfeLink>Vorbereitungshilfe</vorbereitungshilfeLink>.",
        "step-3":
          "Wenn Sie den Brief erhalten haben und vorbereitet sind, gehen Sie erneut auf www.steuerlotse-rente.de",
        "step-4":
          "Wählen Sie den Menüpunkt <steuerErklaerungsLink>Ihre Steuererklärung</steuerErklaerungsLink> und melden sich mit Ihrem Freischaltcode an. Nach der Anmeldung können Sie das Steuerformular ausfüllen und verschicken.",
      },
      letter: {
        heading: "So sieht der Brief aus, den Sie erhalten werden",
        intro:
          "Auf dem Brief wird der DigitalService4Germany als Antragsteller angegeben. Die Organisation ist der Betreiber des Steuerlotsen. Ihren Freischaltcode finden Sie auf der letzten Seite des Briefes.",
      },
      preparation: {
        heading: "Wie Sie sich auf Ihre Steuererklärung vorbereiten können",
        intro:
          "Unsere Vorbereitungshilfe gibt Ihnen einen Überblick darüber, welche Unterlagen Sie für die Erstellung Ihrer Steuererklärung beim Steuerlotsen brauchen, und erklärt, wie Sie nach Erhalt des Briefes fortfahren.",
        button: "Vorbereitungshilfe herunterladen",
      },
    },
  },
  fields: {
    idnr: {
      labelText: "Steuer-Identifikationsnummer",
      help: {
        title: "Wo finde ich diese Nummer?",
        text: "Die 11-stellige Nummer haben Sie mit einem Brief vom Bundeszentralamt für Steuern erhalten. Die Nummer steht oben rechts groß auf dem Brief. Alternativ finden Sie diese Nummer auch auf Ihrem letzten Steuerbescheid.",
      },
    },
    dob: {
      labelText: "Geburtsdatum",
    },
    dateField: {
      exampleInput: {
        text: "z.B. 29.2.1951",
      },
    },
    yesNoSwitch: {
      Yes: "Ja",
      No: "Nein",
    },
  },
};

export default translations;
