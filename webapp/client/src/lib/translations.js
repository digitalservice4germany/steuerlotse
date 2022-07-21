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
  anchorButton: {
    anmelden: {
      text: "Jetzt anmelden",
      url: "/unlock_code_request/step/data_input?link_overview=False",
    },
  },
  anchorBackUebersicht: {
    text: "Zurück zur Übersicht",
    url: "/#",
  },
  dropDown: {
    defaultOption: "Bitte auswählen",
  },
  form: {
    optional: "optional",
    back: "Zurück",
    backToOverview: "Zurück zur Übersicht",
    next: "Weiter",
    logout: {
      button: "Abmelden",
      title: "Sind Sie sicher, dass Sie sich abmelden möchten?",
      intro:
        "Ihre bisher eingetragenen Angaben werden erst an uns übermittelt, wenn Sie Ihre Steuererklärung verschicken. Ihre Steuererklärung wird daher nicht zwischengespeichert. Wenn Sie sich abmelden, kann es sein, dass Ihre Angaben bei der nächsten Anmeldung nicht mehr vorhanden sind.",
    },
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
    sessionNote: {
      title: "Hinweis zur Sitzung",
      listItem1:
        "Ihre Daten gehören Ihnen und werden erst übermittelt, wenn Sie Ihre Steuererklärung verschicken.",
      listItem2:
        "Aus diesem Grund werden Ihre Angaben derzeit nicht zwischengespeichert. Sie müssen Ihre Steuererklärung daher <bold>in einer Sitzung abschließen.</bold>",
      listItem3:
        "Sie können sich innerhalb der Sitzung für das Ausfüllen Ihrer Steuererklärung natürlich Zeit lassen. Sollten Sie allerdings <bold>länger als 3 Stunden</bold> nichts mehr auf dieser Webseite machen, werden Sie aus Sicherheitsgründen automatisch abgemeldet.",
      listItem4:
        "Sie können alle Angaben vor Versand noch einmal kontrollieren.",
    },
    declarationEdaten: {
      intro1:
        "Da viele Informationen der Finanzverwaltung bereits vorliegen, müssen Sie diese nicht mehr in Ihre Steuererklärung eintragen. Dazu gehören zum Beispiel die elektronisch an die Finanzverwaltung übermittelten inländischen Renteneinkünfte, Pensionen und Krankenversicherungsbeiträge.",
      intro2:
        "Welche Beträge über Sie übermittelt wurden, können Sie den Bescheiden entnehmen, die Sie von der jeweiligen Stelle per Post erhalten haben. Die Daten kommen aus der gleichen Quelle.",
      labelText:
        "Ich bzw. wir sind damit einverstanden, dass die Festsetzung meiner / unserer Einkommensteuer anhand der elektronisch vorliegenden Daten erfolgt, die der Finanzbehörde vorliegen.",
    },
    confirmation: {
      fieldRegistrationConfirmDataPrivacy: {
        labelText:
          "Ich habe die <dataPrivacyLink href='http://test.de'>Datenschutzerklärung</dataPrivacyLink> inklusive der <taxGdprLink>Allgemeinen Informationen zur Umsetzung der datenschutzrechtlichen Vorgaben der Artikel 12 bis 14 der Datenschutz-Grundverordnung in der Steuerverwaltung</taxGdprLink> zur Kenntnis genommen und akzeptiere diese.",
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
    summary: {
      heading: "Prüfen Sie Ihre Angaben",
      mandatorySection: "PFLICHTANGABEN",
      steuerminderungSection: "STEUERMINDERNDE AUFWENDUNGEN",
      confirmCompleteCorrect:
        "Hiermit bestätige ich, dass die Angaben überprüft wurden und dass sie vollständig und richtig sind.",
      changeAlt: "Angaben ändern",
      change: "Ändern",
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
        "Mit Ihrer Registrierung beantragen Sie einen Freischaltcode bei Ihrer Finanzverwaltung. Sie erhalten diesen mit einem Brief <bold>innerhalb von zwei Wochen</bold> nach erfolgreicher Beantragung. Wenn Sie die Zusammenveranlagung nutzen möchten, reicht es aus, wenn sich eine Person registriert.",
    },
  },
  newsletter: {
    headline: "Bleiben Sie informiert",
    text: "Erhalten Sie per E-Mail Erinnerungen zu wichtigen Fristen und weitere Informationen zum Steuerlotsen, zum Beispiel zur Vorbereitung der Steuererklärung.",
    fieldEmail: {
      label: "Ihre E-Mail Adresse",
    },
    button: {
      label: "E-Mails abonnieren",
    },
    smallText:
      "Mit dem Abonnieren der E-Mails nehmen Sie die <dataPrivacyLink>Datenschutzerklärung</dataPrivacyLink> zur Kenntnis.",
    errors: {
      emailEmpty: "Dieses Feld darf nicht leer sein.",
      emailInvalid: "Die eingegebene E-Mail Adresse ist nicht gültig.",
      emailDuplicate: "Die eingegebene E-Mail Adresse ist bereits registriert.",
      unexpectedError:
        "Das Speichern Ihrer E-Mail-Adresse hat nicht geklappt.  Bitte versuchen Sie es erneut.",
    },
    success: {
      text: "Vielen Dank! Wir haben eine E-Mail zur Bestätigung an {{emailValue}} geschickt. Der Bestätigungslink ist 48 Stunden gültig.",
    },
    successPage: {
      title:
        "Vielen Dank für Ihre Bestätigung! Sie erhalten nun E-Mails vom Steuerlotsen.",
    },
  },
  filing: {
    success: {
      title:
        "Ihre Informationen wurden erfolgreich verschickt. Speichern Sie Ihre Nachweise für Ihre Unterlagen.",
      intro:
        "Ihre Informationen wurden erfolgreich an Ihre Finanzverwaltung übermittelt. Bewahren Sie Ihre Nachweise für Nachfragen gut auf.",
      transfer_ticket: {
        heading: "Transferticket",
        text: "Mit dem Transferticket wird die erfolgreiche Übermittlung Ihrer Daten durch die Finanzverwaltung bestätigt. Notieren Sie sich Ihr Transferticket, damit Sie nachweisen können, dass Ihre Daten erfolgreich übermittelt wurden.",
        your_heading: "Ihr Transferticket:",
      },
      pdf: {
        heading: "Übersicht Ihrer übermittelten Angaben",
        text: "Sie finden in der Übersicht Ihrer übermittelten Angaben alle Daten, die an Ihre Finanzverwaltung gesendet wurden. So können Sie jederzeit nachsehen, was Sie angegeben haben. Die Übersicht hilft Ihnen zum Beispiel dabei, Ihren Steuerbescheid zu kontrollieren.",
        download: "Übersicht speichern",
      },
    },
    failure: {
      alert: {
        title: "Ihre Steuererklärung kann nicht übermittelt werden.",
      },
      nextStep: {
        heading: "Wie geht es weiter?",
        text: "Bitte wenden Sie sich mit einer E-Mail an  <anchormail>kontakt@steuerlotse-rente.de</anchormail>  und schildern Sie uns das Problem. Vermeiden Sie aber unbedingt, uns persönliche Daten, wie Ihren Freischaltcode oder Ihre Steuer-Identifikationsnummer zu senden.",
        mailto: "mailto:kontakt@steuerlotse-rente.de",
      },
      textUs: "Schreiben Sie uns",
      icon_alt: "Weißes Kreuzzeichen auf rotem Kreis",
    },
  },
  submitAcknowledge: {
    title:
      "Steuerformular - Abgabebestätigung - Der Steuerlotse für Rente und Pension",
    successMessage:
      "Herzlichen Glückwunsch! Sie sind mit Ihrer Steuererklärung fertig!",
    "next-steps": {
      heading: "Wie geht es weiter?",
      text: "Ihre Steuererklärung wird von Ihrem Finanzamt bearbeitet. Sie bekommen Ihren Steuerbescheid per Post zugeschickt.",
    },
    recommend: {
      heading: "Empfehlen Sie uns weiter!",
      text: "Wir möchten noch mehr Menschen bei Ihrer Steuererklärung helfen! Sie können uns dabei helfen, indem Sie den Steuerlotsen bekannter machen. Empfehlen Sie uns Ihren Bekannten und Freunden!",
      share_text:
        "Mit dem Steuerlotse für Rente und Pension können Menschen im Ruhestand Ihre Steuererklärung einfach und unkompliziert machen. Die Online-Dienstleistung wurde vom Bundesfinanzministerium in Auftrag gegeben und ist kostenlos. Mehr Informationen: https://www.steuerlotse-rente.de/",
      mail_subject: "Vereinfachte Steuererklärung für Rentner und Pensionäre",
      promote_url: "https://www.steuerlotse-rente.de/",
    },
    supportingDocumentsEvidence: {
      heading: "Was mache ich mit Belegen und Nachweisen?",
      text: "Belege müssen Sie nur einreichen, wenn das Finanzamt Sie schriftlich dazu auffordert. Bewahren Sie Ihre Belege daher für den Fall einer Nachfrage gut auf. Belege, nach denen das Finanzamt häufig fragt, können zum Beispiel Spendenbescheinigungen, der Nachweis von Pflegekosten, einer Behinderung oder Rechnungen von Handwerkern sein.",
    },
    logout: {
      heading: "Wir löschen Ihr Nutzerkonto",
      text: "Bitte beachten Sie, dass Sie Ihren Freischaltcode nicht erneut verwenden können. Wenn Sie unseren Service nächstes Jahr wieder nutzen möchten, können Sie sich einfach erneut registrieren. Haben Sie Ihre Steuererklärung gespeichert? Dann können Sie sich abmelden.",
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
        header: {
          title:
            "Ihr Freischaltcode wurde bei Ihrem Finanzamt beantragt und wird Ihnen per Post zugeschickt.",
        },
        howItContinues: {
          heading: "So geht es weiter",
          "step-1": {
            heading: "Vorbereiten und Belege sammeln",
            text: "Sie können sich auf Ihre Steuererklärung vorbereiten, bis Sie den Brief erhalten haben. Eine Übersicht über die notwendigen Unterlagen und Informationen, die Sie für die Erstellung Ihrer Steuererklärung brauchen, finden Sie in unserer Vorbereitungshilfe oder unter dem Menüpunkt <vorbereitenLink>Vorbereiten</vorbereitenLink>.",
            buttonText: "Vorbereitungshilfe speichern ",
          },
          "step-2": {
            heading: "Brief mit Freischaltcode zur Anmeldung erhalten",
            text: "Sie erhalten in den nächsten zwei Wochen von Ihrer Finanzverwaltung einen Brief mit Ihrem Freischaltcode. Auf dem Brief wird der DigitalService als Antragssteller stehen. Die Organisation ist der Betreiber des Steuerlotsen. Ihren Freischaltcode finden Sie auf der letzten Seite des Briefes:",
          },
          "step-3": {
            heading: "Steuererklärung online machen",
            text: "Wenn Sie den Brief erhalten haben und vorbereitet sind, gehen Sie erneut auf steuerlotse-rente.de. Wählen Sie den Menüpunkt „Ihre Steuererklärung“ und melden Sie sich mit Ihrem Freischaltcode an. Nach der Anmeldung können Sie das Steuerformular ausfüllen und verschicken.",
          },
        },
      },
      letter: {
        heading: "So sieht der Brief aus, den Sie erhalten werden",
        intro:
          "Auf dem Brief wird der DigitalService als Antragsteller angegeben. Die Organisation ist der Betreiber des Steuerlotsen. Ihren Freischaltcode finden Sie auf der letzten Seite des Briefes.",
      },
      preparation: {
        heading: "Wie Sie sich auf Ihre Steuererklärung vorbereiten können",
        intro:
          "Unsere Vorbereitungshilfe gibt Ihnen einen Überblick darüber, welche Unterlagen Sie für die Erstellung Ihrer Steuererklärung beim Steuerlotsen brauchen, und erklärt, wie Sie nach Erhalt des Briefes fortfahren.",
        anchor: "Vorbereitungshilfe herunterladen",
      },
    },
    failure: {
      header: {
        title: "Registrierung fehlgeschlagen. Bitte prüfen Sie Ihre Angaben.",
        intro:
          "Haben Sie sich vielleicht bereits registriert? In diesem Fall können Sie sich nicht erneut registrieren und bekommen einen Brief mit Ihrem persönlichen Freischaltcode von Ihrer Finanzverwaltung zugeschickt.",
      },
    },
    icons: {
      iconOne: {
        altText: "Schritt 1",
      },
      iconTwo: {
        altText: "Schritt 2",
      },
      iconThree: {
        altText: "Schritt 3",
      },
    },
  },
  revocation: {
    failure: {
      header: {
        title: "Stornierung fehlgeschlagen. Bitte prüfen Sie Ihre Angaben.",
        intro:
          "Sind Sie vielleicht noch nicht bei uns registriert? In diesem Fall können Sie Ihren Freischaltcode nicht stornieren. Haben Sie Ihre Steuererklärung bereits erfolgreich verschickt? Dann haben wir Ihren Freischaltcode automatisiert storniert und Sie müssen nichts weiter tun.",
      },
    },
  },
  fields: {
    idnr: {
      labelText: "Steuer-Identifikationsnummer",
      help: {
        title: "Wo finde ich diese Nummer?",
        text: "Die 11-stellige Nummer haben Sie mit einem Brief vom Bundeszentralamt für Steuern erhalten. Die Nummer steht oben rechts groß auf dem Brief. Alternativ finden Sie diese Nummer auch auf Ihrem letzten Steuerbescheid. Sollten Sie Ihre Steuer-Identifikationsnummer nicht finden, erhalten Sie <steuerIdLink>hier</steuerIdLink> weitere Unterstützung.",
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
  infoTaxReturnPensioners: {
    intro: {
      heading:
        "Vereinfachte Steuererklärung für Rentner — wie Sie in wenigen Minuten Ihre Steuererklärung kostenlos online machen können",
      paragraphOne:
        "Dank des neuen vereinfachten Online-Steuerformulars für Menschen im Ruhestand, das wir im Auftrag des Bundesfinanzministeriums entwickelt haben, können Sie jetzt Ihre Steuererklärung schnell, unkompliziert und kostenlos online einreichen. Ganz ohne Vorwissen und lästigen Papierkram.",
      paragraphTwo:
        "Was viele nicht wissen: Auch Rentner sind grundsätzlich steuerpflichtig - wenn ihre Alterseinkünfte eine gewisse Grenze überschreiten. Und weil die <statistaLink>Renten seit Jahren angepasst</statistaLink> werden, rutschen immer mehr Ruheständler in die Steuerpflicht. Aktuell zählt das Statistische Bundesamt insgesamt <destatisLink>6,8 Millionen steuerpflichtige Rentnerinnen und Rentner</destatisLink> in Deutschland. Tendenz steigend. ",
    },
    section_two: {
      heading:
        "Die vereinfachte Steuererklärung wurde speziell für Menschen im Ruhestand entwickelt",
      paragraph:
        "Wenn Sie also zu denen gehören, denen unerwartet ein Brief vom Finanzamt ins Haus flattert, können Sie erstmal beruhigt sein. Denn mit dem Steuerlotsen für Rente und Pension schrumpft die Steuererklärung zu einer kleinen Pflicht, die Sie in wenigen Minuten erledigen können. Der Steuerlotse führt Sie Schritt-für-Schritt mit einfachen Erklärungen durch die vereinfachte Steuererklärung. Außerdem müssen Sie viel weniger Angaben machen als bei üblichen Steuerformularen. Die Daten zu Ihren Einkünften werden direkt via E-Daten an das Finanzamt übermittelt. Ihre Steuererklärung beschränkt sich damit auf persönliche Angaben und die Beiträge, die Sie absetzen möchten. Was Sie alles absetzen können, erfahren Sie in unserem <downloadPreparationLink>Vorbereitungs-PDF</downloadPreparationLink>. Das spart enorm Zeit und Nerven und vereinfacht den gesamten Prozess. ",
    },
    section_three: {
      heading: "Wie finde ich heraus, ob ich als Rentner steuerpflichtig bin? ",
      paragraphOne:
        "Ob Sie den Steuerlotsen nutzen können, hängt natürlich davon ab, ob Sie steuerpflichtig sind. Wenn Sie bereits wissen, dass dies bei Ihnen der Fall ist, weil Sie zum Beispiel ein Schreiben vom Finanzamt erhalten haben, können Sie direkt zum Abschnitt „So funktioniert der Steuerlotse“ springen.",
      paragraphTwo:
        "Wenn Sie jedoch noch unsicher sind, ob Sie überhaupt eine Steuererklärung abgeben müssen, dann können Sie mit dem <incomeCalculatorLink>Alterseinkünfte-Rechner</incomeCalculatorLink> des Bayerischen Landesamts für Steuern kostenlos kalkulieren, wie hoch eine mögliche Einkommensteuer bei Ihnen ausfällt. Außerdem finden Sie weitere Informationen zur Besteuerung der Rente auf der Seite der <pensionersInsuranceLink>Deutschen Rentenversicherung.</pensionersInsuranceLink>",
    },
    section_four: {
      heading: "So funktioniert der Steuerlotse für Rente und Pension",
      paragraph:
        "Ist die Frage der Steuerpflicht geklärt, dann geht es mit dem Steuerlotsen in 4 Schritten zur fertigen Steuererklärung.",
    },
    section_five: {
      listItemOneHeading: "Schritt 1: Nutzung prüfen",
      listItemOne:
        "Im ersten Schritt müssen Sie auf der <eligibilityLink>Webseite des Steuerlotsen prüfen</eligibilityLink>, ob Sie den Steuerlotsen in seiner aktuellen Entwicklungsform nutzen können. Denn zur Zeit richtet sich der Steuerlotse nur an Personen und Paare, die eine Rente und Pension beziehen und keine Zusatzeinkünfte haben. Trifft dies zu, können Sie im zweiten Schritt mit der Registrierung fortfahren.",
      listItemTwoHeading: "Schritt 2: Registrieren",
      listItemTwo:
        "Wenn Sie den Steuerlotsen nutzen können, registrieren Sie sich im nächsten Schritt. Bei der <registrationLink>Registrierung</registrationLink> wird automatisch ein Freischaltcode bei Ihrer Finanzverwaltung beantragt. Der Freischaltcode wird Ihnen per Brief innerhalb von zwei Wochen nach erfolgreicher Beantragung zugesendet. Übrigens: auch eine Zusammenveranlagung ist möglich. Hierfür muss sich nur eine Person registrieren.",
      listItemThreeHeading: "Schritt 3: Vorbereiten",

      listItemThree:
        "Nach der erfolgreichen Registrierung ist es wichtig, dass Sie sich gut vorbereiten. Stellen Sie daher sicher, alle erforderlichen Informationen, wie zum Beispiel Belege, vorliegen zu haben. Damit Sie nichts vergessen und perfekt vorbereitet sind, haben wir eine nützliche Kontrollliste mit allen wichtigen Informationen zum <downloadPreparationLink>Herunterladen</downloadPreparationLink> für Sie angefertigt.",
      listItemFourHeading: "Schritt 4: Steuererklärung ausfüllen",

      listItemFour:
        "Nach Erhalt des Freischaltcodes können Sie mit der Steuererklärung beginnen. Dafür melden Sie sich auf der Webseite unter <activationLink>„Ihre Steuererklärung“</activationLink> mit den entsprechenden Daten an.",
    },
    section_six: {
      text: "Nachdem Sie sich durch das Online-Formular des Steuerlotsen geklickt haben und alle Angaben gemacht haben, wird Ihre Steuererklärung elektronisch an Ihr Finanzamt weitergeleitet. Ihre Steuererklärung ist offiziell eingereicht! Sie können sich nun zurücklehnen und auf den Steuerbescheid warten. Dieser wird Ihnen vom Finanzamt innerhalb der üblichen Frist zugeschickt.",
    },
    ShareBox: {
      header: "Artikel weiterempfehlen",
      text: "Dieser Artikel könnte auch hilfreich für Ihre Freunde oder Bekannten sein. ",
      promoteUrl:
        "https://www.steuerlotse-rente.de/vereinfachte-steuererklärung-für-rentner",
      shareText:
        "Diesen Artikel beim Steuerlotsen für Rente und Pension finde ich interessant: https://www.steuerlotse-rente.de/vereinfachte-steuererklärung-für-rentner",
      mailSubject: "Artikel beim Steuerlotsen für Rente und Pension",
      sourcePage: "shareAcknowledged",
    },
  },
  ContentPagesAnchors: {
    Krankheitskosten: {
      text: "Krankheitskosten",
    },
    Vorsorgeaufwendungen: {
      text: "Vorsorgeaufwendungen",
    },
    Pflegekosten: {
      text: "Pflegekosten",
    },
    Behinderung: {
      text: "Angaben bei einer Behinderung",
    },
    Bestattungskosten: {
      text: "Bestattungskosten",
    },
    Belastungen: {
      text: "Wiederbeschaffungskosten",
    },
    Dienstleistungen: {
      text: "Haushaltsnahe Dienstleistungen",
    },
    Handwerkerleistungen: {
      text: "Handwerkerleistungen",
    },
    Spenden: {
      text: "Spenden und Mitgliedsbeiträge",
    },
    Kirchensteuer: {
      text: "Kirchensteuer",
    },
  },
  Handwerkerleistungen: {
    Section1: {
      heading: "Handwerkerleistungen",
      text: "Auch Kosten für Dienstleistungen oder Handwerkerleistungen im eigenen Haushalt können zu Steuerermäßigungen führen. Die Arbeiten müssen in Ihren eigenen vier Wänden oder auf Ihrem Grundstück ausgeführt werden.",
    },
    Section2: {
      heading: "Beispiele für Handwerkerleistungen",
      text:
        "Viele Handwerkerleistungen bei Renovierungs-, Erhaltungs- und Modernisierungsmaßnahmen können Sie " +
        "von der Steuer absetzen. Die Arbeitsleistung muss dabei im eigenen Haushalt erbracht worden sein.",
      list: {
        item1: "Reparatur in der Wohnung",
        item2: "Reinigung von Abflussrohren",
        item3: "Reparatur oder Austausch von Bodenbelägen",
        item4: "Modernisierung des Badezimmers oder der Einbauküche",
        item5:
          "Reparatur, Wartung oder Austausch von Heizungsanlagen, Elektro-, Gas- und Wasserinstallationen",
        item6: "Schornsteinfegerleistungen",
        item7: "Arbeiten an Innen- und Außenwänden",
        item8: "Reinigung von Dachrinnen",
        item9: "Maßnahmen der Gartengestaltung",
      },
      text2:
        "<bold>Achtung:</bold> Insbesondere bei Handwerkerleistungen ist zu beachten, dass nur der Arbeitslohn, nicht aber " +
        "die Materialkosten abzugsfähig sind. Prüfen Sie, ob die Rechnungen entsprechend aufgeschlüsselt sind.",
      text3:
        "Der Arbeitslohn ist inklusive anfallender Umsatzsteuer abzugsfähig. Wenn in der Rechnung der Arbeitslohn " +
        "nicht extra ausgewiesen ist, können Sie den Dienstleister bitten, eine neue, detailliertere Rechnung auszustellen.",
    },
    Section3: {
      heading: "Rechnungen und Zahlungsweg beachten",
      text:
        "Es muss eine Rechnung vorliegen, die zum Beispiel per Überweisung oder EC-Kartenzahlung beglichen worden " +
        "ist. Barzahlungen berücksichtigt das Finanzamt nicht! ",
      text2: "Bewahren Sie immer die entsprechenden Kontoauszüge auf!",
    },
    Section5: {
      heading: "Weitere Ausgaben, die Sie absetzen können",
    },
  },
  Bestattungskosten: {
    Section1: {
      heading: "Bestattungskosten",
      text:
        "Bestattungskosten zählen zur Kategorie der außergewöhnlichen Belastungen. Die Kosten können allerdings " +
        "nur insoweit abgesetzt werden, wie diese das Erbe übersteigen.",
    },
    Section2: {
      heading: "Beispiele für absetzbare Bestattungskosten",
      text: "Sie können die Kosten angeben, die unmittelbar mit der Bestattung von Angehörigen zusammenhängen. Die entstehenden Kosten weisen Sie mithilfe der entsprechenden Rechnungen nach. Kosten, die Sie absetzen können:",
      list: {
        item1:
          "Kosten für die Trauerfeier wie Gestecke, Trauerhalle, Redner*in/Pfarrer*in, Sargträger, musikalische Darbietung etc.",
        item2: "Kosten für die Grabstätte",
        item3:
          "Weitere Kosten: Darlehenszinsen zur Finanzierung der Beerdigung, Zahlungsrückstände des*der Verstorbenen (Miete, Strom etc.)",
      },
    },
    Section3: {
      heading: "Nicht absetzbare Bestattungskosten",
      text: "Folgende Angaben werden steuerlich nicht anerkannt:",
      list: {
        item1: "Kosten für Trauerkleidung",
        item2: "Bewirtung der Trauergäste",
        item3: "Reisekosten anlässlich der Bestattung",
        item4: "Kosten für die laufende Grabpflege",
      },
    },
    Section4: {
      heading: "Die zumutbare Belastung",
      text:
        "Die Absetzbarkeit von Bestattungskosten hat wie alle außergewöhnlichen Belastungen eine Hürde: " +
        "Die zumutbare Belastung. Nur der Betrag, der höher ist als Ihre zumutbare Belastung, wirkt sich steuermindernd aus.",
      text2:
        "Die zumutbare Belastung hängt unter anderem von der Höhe Ihres Einkommens ab und wird von " +
        "Ihrem Finanzamt automatisch berechnet.",
    },
    Section5: {
      heading: "Weitere Ausgaben, die Sie absetzen können",
    },
  },
  Krankheitskosten: {
    Paragraph1: {
      heading: "Krankheitskosten",
      text:
        "Krankheitskosten sind durch Krankheit verursachte besondere Kosten und gehören zur Kategorie der " +
        "außergewöhnlichen Belastungen. Hierunter zählen aber nur solche Aufwendungen, die der Heilung oder Linderung " +
        "einer Krankheit dienen.",
    },
    Paragraph2: {
      heading: "Beispiele für absetzbare Krankheitskosten",
      list: {
        item1:
          "Selbstgetragene Arztkosten/Behandlungskosten und Zuzahlungen zum Beispiel von Zahnärzt:innen, Logopäd:innen, Physiotherapeut:innen, Heilpraktiker:innen oder Psychotherapeut:innen ",
        item2: "Rezeptgebühren ",
        item3:
          "Notwendige Hilfsmittel wie Brillen, Hörgeräte oder spezielle Schuheinlagen",
        item4: "Verschriebene Heilkuren, Massagen, Bäder und Einläufe",
        item5: "Eigenanteil bei Zahnersatz",
        item6: "Fahrtkosten zum Arzt",
      },
    },
    Paragraph3: {
      heading: "Nachweise",
      text:
        "Für die steuerliche Anerkennung der Krankheitskosten brauchen Sie eine ärztliche Verordnung, ein Rezept " +
        "oder ein amtsärztliches Gutachten als Nachweis für eine medizinische Indikation der Behandlung. " +
        "Das amtsärztliche Gutachten muss vor Behandlungsbeginn ausgestellt worden sein. " +
        "Bei einer andauernden Erkrankung mit anhaltendem Verbrauch bestimmter Medikamente, reicht die einmalige " +
        "Vorlage " +
        "einer solchen Verordnung aus.",
    },
    Paragraph4: {
      heading: "Die zumutbare Belastung",
      text:
        "Die Absetzbarkeit von Krankheitskosten hat wie alle außergewöhnlichen Belastungen eine Hürde: Die zumutbare " +
        "Belastung. Nur der Betrag, der höher ist als Ihre zumutbare Belastung, wirkt sich steuermindernd aus. " +
        "Die zumutbare Belastung hängt unter anderem von der Höhe Ihres Einkommens ab und wird von Ihrem Finanzamt " +
        "automatisch berechnet.",
    },
    Paragraph5: {
      heading: "Weitere Ausgaben, die Sie absetzen können",
    },
    List: {
      item1: {
        text: "Selbstgetragene Arztkosten/Behandlungskosten und Zuzahlungen zum Beispiel von Zahnärzt:innen, Logopäd:innen, Physiotherapeut:innen, Heilpraktiker:innen oder Psychotherapeut:innen",
      },
      item2: {
        text: "Rezeptgebühren",
      },
      item3: {
        text: "Notwendige Hilfsmittel wie Brillen, Hörgeräte oder spezielle Schuheinlagen",
      },
      item4: {
        text: "Verschriebene Heilkuren, Massagen, Bäder und Einläufe",
      },
      item5: {
        text: "Eigenanteil bei Zahnersatz",
      },
      item6: {
        text: "Fahrtkosten zum Arzt",
      },
    },
  },
  Spenden: {
    Section1: {
      heading: "Spenden und Mitgliedsbeiträge",
      text: "Spenden und Mitgliedsbeiträge können als Sonderausgaben abgesetzt werden. Wir erklären, wie Sie Spenden absetzen können.",
    },
    Section2: {
      heading: "Spenden und Beiträge für steuerbegünstigte Zwecke",
      text: "Spenden können nur steuermindernd berücksichtigt werden, wenn sie an steuerbegünstigte Organisationen fließen. Dazu zählen z.B.",
      list: {
        item1: "Kirchen",
        item2: "Stiftungen",
        item3: "staatliche Museen",
        item4: "Universitäten oder",
        item5: "Vereine",
      },
      text2:
        "Ob eine Organisation steuerbegünstigt ist, stellt das Finanzamt fest. Auch Mitgliedsbeiträge an " +
        "steuerbegünstigte Organisationen können steuermindernd berücksichtigt werden, zum Beispiel Mitgliedsbeiträge " +
        "für kulturelle Fördervereine.",
      text3: "Nicht absetzbar sind Mitgliedsbeiträge in Freizeitvereinen wie",
      list2: {
        item1: "Sportklubs",
        item2: "Gesangsvereine",
        item3: "Vereine für Heimatpflege",
        item4: "Vereine für Tierzucht",
        item5: "Kleingartenvereine",
      },
    },
    Section3: {
      heading: "Spenden an politische Parteien",
      text:
        "Auch Spenden an politiche Parteien können Sie absetzen. Zu beachten ist jedoch, dass der Abzug nicht " +
        "möglich ist, wenn die politische Partei von der staatlichen Parteienfinanzierung ausgeschlossen ist.",
      text2:
        "Spenden und Mitgliedsbeiträge an inländische politische Parteien und unabhängige Wählervereinigungen " +
        "können Sie zu 50 % von der Steuer absetzen. Allerdings bis maximal 825 Euro pro Person bei Ausgaben in Höhe von 1.650 Euro.",
    },
    Section4: {
      heading: "Nachweise",
      text:
        "Für einen Spendenabzug benötigen Sie grundsätzlich eine Spendenbescheinigung im Original. Diese sind aber " +
        "nur auf Anforderung des Finanzamts nachzuweisen.",
      text2:
        "Bei Spenden bis 300 Euro reicht den meisten Finanzämtern eine Kopie der Abbuchung vom Kontoauszug aus.",
    },
    Section5: {
      heading: "Weitere Ausgaben, die Sie absetzen können",
    },
  },
  Kirchensteuer: {
    Section1: {
      heading: "Kirchensteuer",
      text: "Zahlen Sie Steuern für eine Religionsgemeinschaft, können Sie diese als Sonderausgabe absetzen. Dazu zählt auch gezahltes Kirchgeld oder Ortskirchensteuer.",
    },
    Section2: {
      heading: "Geleistete Zahlungen",
      text: "Sie können zum einen die Summe Ihrer im letzten Jahr gezahlten Kirchensteuer angeben. Diese Daten finden Sie zum Beispiel auf ihrem Einkommensteuerbescheid und Ihrem Vorauszahlungsbescheid, sowie auf Ihrer Lohnsteuerbescheinigung.",
    },
    Section3: {
      heading: "Erhaltene Erstattungen",
      text:
        "Haben Sie im letzten Jahr zu viel gezahlte Kirchensteuer erstattet bekommen, kann dies ebenfalls angegeben. " +
        "Die Summe der erstatteten Kirchensteuer finden Sie zum Beispiel auf dem Steuerbescheid des Vorjahres.",
    },
    Section5: {
      heading: "Weitere Ausgaben, die Sie absetzen können",
    },
  },
  InfoBox: {
    heading: "Sie sind vorbereitet und haben Ihren Freischaltcode erhalten?",
    text: "Wenn Sie den Brief mit Ihrem Freischaltcode erhalten haben, starten Sie mit Ihrer Steuererklärung.",
  },
  InfoBoxGrundsteuer: {
    heading: "Weitere Steuerprodukte vom DigitalService",
    text: "Mit unserem weiteren Service können private Eigentümer:innen ihre Grundsteuererklärung einfach und kostenlos online abgeben!",
    button: "Zum Service",
  },
  CheckNowInfoBox: {
    heading: "Steuererklärung kann auch einfach sein",
    text: "Schnell und unkompliziert – mit und für Rentenbeziehende entwickelt! Finden Sie heraus, ob Sie den Steuerlotsen nutzen können.",
    button: "Jetzt prüfen",
  },
  taxGuideQuestionBox: {
    canIUseTaxGuide:
      "Kann ich den Steuerlotsen für meine Steuererklärung nutzen?",
    startQuestionnaire: "Fragebogen starten",
    moreInformationTaxGuide:
      "Wo finde ich mehr Informationen zum Steuerlotsen?",
    faq: "Häufig gestellte Fragen",
    contactUs: "Kontaktieren Sie uns",
  },
  vorbereitenOverview: {
    Paragraph1: {
      heading: "Vorbereitung auf Ihre Steuererklärung 2021",
      text: "Wussten Sie, dass die Steuererklärung mit dem Steuerlotsen im Durchschnitt nur 24 Minuten dauert? Damit es auch bei Ihnen so schnell geht, müssen Sie einige Vorkehrungen treffen. Dafür haben wir eine nützliche Vorbereitungshilfe für Sie erstellt. ",
    },
    Paragraph2: {
      heading: "Unsere Vorbereitungshilfe",
      text: "Unsere Vorbereitungshilfe zeigt Ihnen, welche Angaben Sie in der Steuererklärung machen müssen und welche Ausgaben Sie steuerlich absetzen können. So wissen Sie genau, in welchen Unterlagen Sie nachschauen müssen und welche Belege Sie raussuchen sollten. Sie können die Vorbereitungshilfe einfach speichern und ausdrucken und sich beim Ausfüllen der Steuererklärung neben den Computer legen. ",
    },
    Download: "Vorbereitungshilfe speichern [PDF]",
    Accordion: {
      heading: "Diese Angaben müssen Sie angeben",
      Item1: {
        heading: "Familienstand",
        detail:
          "Sollten Sie nicht ledig sein, müssen Sie angeben, seit wann Sie verheiratet, geschieden oder verwitwet sind. Wenn Sie verheiratet sind oder in einer eingetragenen Partnerschaft leben, können Sie die Zusammenveranlagung nutzen.",
      },
      Item2: {
        heading: "Name, Geburtsdatum, Adresse und Religionszugehörigkeit",
        detail:
          "Möchten Sie die Steuererklärung gemeinsam als Paar machen, müssen Sie die Angaben für beide Personen machen. Sollten Sie keiner Religionsgemeinschaft angehören, können Sie »nicht kirchensteuerpflichtig« auswählen.",
      },
      Item3: {
        heading: "Steuer-Identifikationsnummer",
        detail:
          "Die 11-stellige Nummer haben Sie mit einem Brief vom Bundeszentralamt für Steuern erhalten. Die Nummer steht oben rechts groß auf dem Brief. Alternativ finden Sie die Nummer auch auf Ihrem letzten Steuerbescheid. Sollten Sie Ihre Steuer-Identifikationsnummer nicht finden, erhalten Sie <steuerIdLink>hier</steuerIdLink> weitere Unterstützung. ",
      },
      Item4: {
        heading: "Steuernummer",
        detail:
          "Sie finden Ihre Steuernummer auf den Briefen Ihres Finanzamtes. Abhängig von dem Bundesland, in dem Sie leben, besteht Ihre Steuernummer aus 10-11 Ziffern.\nSollten Sie noch keine Steuernummer haben, können Sie mit der Abgabe der Steuererklärung eine neue Steuernummer beim zuständigen Finanzamt beantragen.",
      },
      Item5: {
        heading: "IBAN Ihrer Bankverbindung",
        detail:
          "Die IBAN besteht in Deutschland aus 22 Stellen. Sie finden die Nummer beispielsweise auf jedem Kontoauszug oder Ihrer Girocard.",
      },
    },
    Paragraph3: {
      heading: "Diese Ausgaben können Sie absetzen",
      text: "Sie können eine Vielzahl an Ausgaben absetzen. Wir erklären Ihnen, welche Ausgaben es gibt und was diese bedeuten.",
    },
  },
  Vorsorgeaufwendungen: {
    Paragraph1: {
      Heading: "Vorsorgeaufwendungen",
      Text: "Viele Versicherungen, mit denen Sie für Ihre Zukunft vorsorgen, können Sie von der Steuer absetzen. Die Höhe der Beiträge steht in den Versicherungsunterlagen oder kann zum Beispiel Kontoauszügen entnommen werden.",
    },
    Paragraph2: {
      Heading:
        "Beispiele für absetzbare Versicherungen als Vorsorgeaufwendungen",
      Text: "Viele Versicherungen, mit denen Sie für Ihre Zukunft vorsorgen, können Sie von der Steuer absetzen. Die Höhe der Beiträge steht in den Versicherungsunterlagen oder kann zum Beispiel Kontoauszügen entnommen werden.",
      ListItem1: "Gesetzliche Krankenversicherungen",
      ListItem2: "Pflegeversicherungen",
      ListItem3: "Arbeitslosenversicherung",
      ListItem4: "Haftpflichtversicherungen (auch Kfz)",
      ListItem5: "Krankenzusatzversicherungen",
      ListItem6: "Risikolebensversicherung",
    },
    Paragraph3: {
      Heading: "Nicht absetzbare Versicherungen",
      Text: "Nicht absetzen können Sie Sachversicherungen, die Gegenstände oder Inventar schützen. Dazu zählen:",
      ListItem1: "Kaskoversicherungen",
      ListItem2: "Hausratversicherungen",
      ListItem3: "Gebäudeversicherungen",
      ListItem4: "Rechtsschutzversicherungen",
    },
    Paragraph4: {
      Heading: "Weitere Ausgaben, die Sie absetzen können",
    },
  },
  DisabilityCostsInfo: {
    Section1: {
      Heading: "Angaben bei einer Behinderung",
      Text: "Im Falle einer Behinderung oder Pflegebedürftigkeit können erhöhte Kosten für Medikamente und Betreuung anfallen. Damit diese Ausgaben Sie nicht zu sehr belasten, können Sie steuerliche Vergünstigungen in Anspruch nehmen.",
    },
    Section2: {
      Heading: "Wahl zwischen Pauschbetrag und Angabe Einzelkosten",
      Text: "Wenn bei Ihnen eine Behinderung vorliegt, können Sie wählen, ob Sie Ihre mit der Behinderung zusammenhängenden Aufwendungen im Einzelnen oder einen Pauschbetrag in Anspruch nehmen. ",
    },
    Section3: {
      Heading: "Pauschbetrag für Menschen mit Behinderung",
      Text: "Für die Errechnung der Höhe des möglichen Pauschbetrag, werden Sie im Steuerformular nach folgenden Angaben gefragt: ",
      ListItem1: "Grad der Behinderung",
      ListItem2: "Bescheinigte Merkzeichen",
      ListItem3: "Pflegegrad 4 oder 5",
    },
    Section4: {
      Heading: "Einige Beispiele für Kosten aufgrund einer Behinderung",
      Text: "Verzichten Sie auf den Pauschebetrag können Sie einzelne Aufwendungen, die Ihnen typischerweise durch ihre Behinderung entstehen, absetzen. Das können Aufwendungen für die Unterstützung und – teilweise – Übernahme für folgende Beispiele sein:",
      ListItem1: "Körperpflege wie Waschen, Zahnpflege, Kämmen, Rasieren",
      ListItem2: "Mobilität wie An- und Auskleiden, Aufstehen und Zubettgehen",
      ListItem3: "Nahrungsaufnahme wie mundgerechte Zubereitung",
      ListItem4:
        "hauswirtschaftliche Versorgung wie Einkaufen, Kochen, Reinigen der Wohnung, Spülen oder Wäschepflege",
    },
    Section5: {
      Heading: "Die zumutbare Belastung",
      Text: "Die Absetzbarkeit der Einzelkosten bei einer Behinderung hat eine Hürde: Die zumutbare Belastung. Nur der Betrag, der höher ist als Ihre zumutbare Belastung, wirkt sich steuermindernd aus.",
      Text2:
        "Die zumutbare Belastung hängt unter anderem von der Höhe Ihres Einkommens ab und wird von Ihrem Finanzamt automatisch berechnet.",
    },
    Section6: {
      Heading: "Die behinderungsbedingte Fahrtkostenpauschale",
      Text: "Für behinderungsbedingte Fahrtkosten wurde eine Pauschbetragsregelung eingeführt – die bisherigen Einzelnachweise für solche Fahrten müssen Sie nicht mehr einreichen. Die Höhe der behinderungsbedingte Fahrtkosten und des Pauschbetrags für Menschen mit Behinderung ist von dem Grad der Behinderung beziehungsweise des Merkzeichens oder Pflegegrad abhängig.",
    },
    Section7: {
      Heading: "Nachweise",
      Text: "Sie müssen Nachweise wie eine Kopie des Behindertenausweises oder den Bescheid über die Einstufung als pflegebedürftige Person in die Pflegegrade 4 oder 5 eingereicht werden, falls diese dem Finanzamt nicht bereits vorgelegen haben. ",
    },
    Section8: {
      Heading: "Weitere Ausgaben, die Sie absetzen können",
    },
  },
  CareCostsInfo: {
    Paragraph1: {
      Heading: "Pflegekosten",
      Text: "Pflegekosten gehören zur Kategorie der außergewöhnlichen Belastungen. Hierzu zählen Kosten, die durch die Pflegebedürftigkeit entstanden sind.",
    },
    Paragraph2: {
      Heading: "Beispiele für Pflegekosten",
      ListItem1: "Unterbringung in einem Pflegeheim",
      ListItem2: "Kosten zur Beschäftigung einer ambulanten Pflegekraft",
    },
    Paragraph3: {
      Heading: "Nachweise",
      Text: "Die Pflegebedürftigkeit muss nachgewiesen werden. Dies kann mit der Bescheinigung der Pflegekasse oder einer privaten Pflegeversicherung gemacht werden. Auch der Schwerbehindertenausweis dient als Nachweis, wenn das Merkzeichen H vorliegt.",
    },
    Paragraph4: {
      Heading: "Die zumutbare Belastung",
      Text: "Die Absetzbarkeit von Pflegekosten hat wie alle außergewöhnlichen Belastungen eine Hürde: Die zumutbare Belastung. Nur der Betrag, der höher ist als Ihre zumutbare Belastung, wirkt sich steuermindernd aus.",
      Text2:
        " Die zumutbare Belastung hängt unter anderem von der Höhe Ihres Einkommens ab und wird von Ihrem Finanzamt automatisch berechnet.",
    },
    Paragraph5: {
      Heading: "Weitere Ausgaben, die Sie absetzen können",
    },
  },
  HouseholdServicesInfo: {
    Section1: {
      Heading: "Haushaltsnahe Dienstleistungen ",
      Text: "Auch Kosten für Dienstleistungen im eigenen Haushalt können zu Steuerermäßigungen führen. Voraussetzung ist unter anderem, dass die Arbeiten in Ihren eigenen vier Wänden oder auf Ihrem Grundstück ausgeführt wurden.",
    },
    Section2: {
      Heading: "Beispiele für Haushaltsnahe Dienstleistungen",
      Text: "Sie können Dienstleistungen absetzen, die Sie beauftragt haben, aber auch von einer im Haushalt lebenden Person erbracht worden sein können. Hierzu gehören zum Beispiel:",
      ListItem1: "Reinigung der Wohnung",
      ListItem2: "Kochen, Waschen, Bügeln durch eine Haushaltshilfe",
      ListItem3: "Gartenpflege wie Rasenmähen, Unkraut entfernen",
      ListItem4: "Winterdienst auf oder vor dem eigenen Grundstück",
      ListItem5: "Zubereitung von Mahlzeiten im Haushalt",
      ListItem6: "Fütterung und Pflege von Haustieren im Haushalt",
      ListItem7:
        "Pflege, Versorgung und Betreuung von kranken, alten und pflegebedürftigen Personen, auch wenn die Pflege- und Betreuungsleistungen im Haushalt der gepflegten / betreuten Person ausgeübt werden, soweit diese Aufwendungen nicht steuermindernd bei der gepflegten Person berücksichtigt wurden",
      ListItem8: "das Hausnotrufsystem innerhalb des betreuten Wohnens",
      Text2:
        "Falls Sie Leistungen aus einer Nebenkostenabrechnung haben oder Leistungen selbstständig in Auftrag gegeben haben, können diese ebenfalls geltend gemacht werden.",
    },
    Section3: {
      Heading: "Haushaltsnahe Dienstleistungen aus der Nebenkostenabrechnung",
      Text: "Auch in der Nebenkostenabrechung für Ihre Wohnung verstecken sich zum Teil haushaltsnahe Dienstleistungen oder Handwerkerkosten, die in der Steuererklärung eingetragen werden können.",
      Text2:
        "Achten Sie hierbei darauf, dass Sie nur den Teil angeben, der für Ihre Wohnung entfällt.",
    },
    Section4: {
      Heading: "Weitere Ausgaben, die Sie absetzen können",
    },
  },
  ReplacementCostsInfo: {
    Section1: {
      Heading: "Wiederbeschaffungskosten",
      Text: "Wiederbaschaffungskosten können unter anderem bei den sonstigen außergewöhnlichen Belastungen angegeben werden.",
    },
    Section2: {
      Heading: "Was können sonstige außergewöhnliche Belastungen sein?",
      Text: "Zu den sonstigen außergewöhnlichen Belastungen zählen zum Beispiel Kosten für Hausrat und Kleidung, die durch ein unabwendbares Ereignis (zum Beispiel Brand oder Hochwasser) verloren wurden.",
      Text2:
        "Vorausgesetzt ist jedoch, das keine allgemein zugängliche und übliche Versicherung möglich war. In den außergewöhnlichen Belastungen sind auch die notwendigen und angemessenen Kosten der Schadensbeseitigung enthalten.",
    },
    Section3: {
      Heading: "Die zumutbare Belastung",
      Text: "Die Absetzbarkeit von Wiederbeschaffungskosten und sonstigen außergewöhnlichen Belastungen hat eine Hürde: Die zumutbare Belastung. Nur der Betrag, der höher ist als Ihre zumutbare Belastung, wirkt sich steuermindernd aus.",
      Text2:
        "Die zumutbare Belastung hängt unter anderem von der Höhe Ihres Einkommens ab und wird von Ihrem Finanzamt automatisch berechnet.",
    },
    Section4: {
      Heading: "Weitere Ausgaben, die Sie absetzen können",
    },
  },
  InfoForRelatives: {
    Section1: {
      Heading: "Informationen für Angehörige",
      Text: "Wir erklären Ihnen, wer helfen darf und wer nicht. Dass sich Angehörige ohne Bezahlung gegenseitig bei der Steuererklärung helfen, erlaubt sogar das sonst so strenge Steuerberatungsgesetz.",
    },
    Section2: {
      Heading: "Wer helfen darf",
      ListItem1: "Ehepartner",
      ListItem2: "Verlobte",
      ListItem3: "Eltern, Schwiegereltern, Kinder, Großeltern, Enkel",
      ListItem4: "Geschwister (auch Halbgeschwister)",
      ListItem5: "Nichten und Neffen",
      ListItem6: "Schwager oder Schwägerin",
      ListItem7: "Onkel und Tante",
      ListItem8: "Pflegeeltern und Pflegekinder",
      ListItem9: "geschiedene Ehepartner",
    },
    Section3: {
      Heading: "Wer nicht bei der Steuererklärungen helfen darf",
      Text: "Helfen zum Beispiel Freunde oder ehemaligen Arbeitskollege bei der Steuererklärung ist das eine Ordnungswidrigkeit – egal ob mit oder ohne Bezahlung. Wer erwischt wird, zahlt bis zu 5.000 € Strafe. Das sollten Sie daher vermeiden!",
    },
  },
  LandingPage: {
    Hero: {
      title: "Die vereinfachte Steuererklärung für Menschen im Ruhestand",
      subTitle:
        "Mit dem Steuerlotsen können Sie Ihre Steuererklärung für das Steuerjahr 2021 einfach und ohne besonderes Vorwissen online machen.",
      listItem1: "mit Schritt-für-Schritt-Anleitung",
      listItem2: "kostenlos und ohne Installation",
      listItem3: "schnell und unkompliziert",
      eligibilityTest:
        "Möchten Sie wissen, ob Sie den Steuerlotsen nutzen können?",
      checkUseButton: "Jetzt prüfen",
      plausibleGoal: "Nutzung prüfen",
    },
    Cards: {
      cardOne: {
        header: "Herausfinden, ob Sie den Steuerlotsen nutzen können",
        text: "Prüfen Sie durch die Beantwortung weniger Fragen, ob Sie die Voraussetzungen für die Nutzung des Steuerlotsen erfüllen.",
        url: "/eligibility/step/tax_year?link_overview=False",
      },
      cardTwo: {
        header: "Registrieren und Freischaltcode beantragen",
        text: "Mit Ihrer Registrierung beantragen Sie einen Freischaltcode. Dieser wird Ihnen nach erfolgreicher Beantragung von Ihrer Finanzverwaltung zugeschickt.",
        url: "/unlock_code_request/step/data_input?link_overview=False",
      },
      cardThree: {
        header: "Mit Freischaltcode anmelden und Steuererklärung machen",
        text: "Sie sind vorbereitet und haben Ihren Freischaltcode erhalten? Dann können Sie mit Ihrer Steuererklärung 2021 beginnen.",
        url: "/unlock_code_activation/step/data_input?link_overview=False",
      },
    },
    Accordion: {
      heading: "Häufig gestellte Fragen zum Steuerlotsen",
      Item1: {
        title: "Wer kann den Steuerlotsen nutzen?",
        detail:
          "Der Steuerlotse richtet sich an Personen und Paare, die eine Rente und Pension beziehen und keine Zusatzeinkünfte haben.\n\nSie beziehen steuerpflichtige Nebeneinkünfte, zum Beispiel Einnahmen aus Vermietung oder aus einer selbständigen Tätigkeit? Dann können Sie den Steuerlotsen derzeit nicht nutzen.\n\nSie können <eligibilityLink>mit unserem Fragebogen</eligibilityLink> prüfen, ob Sie alle Voraussetzungen für den Steuerlotsen erfüllen.",
      },
      Item2: {
        title: "Wie läuft die Nutzung des Steuerlotsen ab?",
        detail:
          "Mit dem Steuerlotsen kommen Sie ganz automatisch in 4 Schritten durch Ihre Steuererklärung:",
        listItem1:
          "<eligibilityLink> Prüfen Sie</eligibilityLink>, ob Sie die Voraussetzung für die Nutzung des Steuerlotsen erfüllen.",
        listItem2:
          "<registrationLink>Registrieren Sie sich</registrationLink> beim Steuerlotsen für Ihre Online-Steuererklärung. Mit der erfolgreichen Registrierung beantragen Sie einen Freischaltcode bei Ihrer Finanzverwaltung.",
        listItem3:
          "Sie erhalten einen Brief mit einem 12-stelligen Freischaltcode.",
        listItem4:
          "Für den letzten Schritt, das Ausfüllen Ihrer Steuererklärung, rufen Sie erneut unsere Seite auf. Klicken Sie auf <activationLink>Ihre Steuererklärung</activationLink>und melden Sie sich mit Ihrem Freischaltcode an. Danach können Sie mit dem Ausfüllen der Steuererklärung beginnen.",
      },
      Item3: {
        title: "Bis wann kann ich die Steuererklärung abgeben?",
        detail:
          "Wenn Sie verpflichtet sind eine Steuererklärung abzugeben, muss Ihre Einkommensteuererklärung bis zum <strong>31. Oktober 2022</strong> beim Finanzamt sein. Wenn dieser Tag in Ihrem Bundesland ein Feiertag ist, gilt der 1. November 2022 als Fristende.\n\nSie können Ihre Steuererklärung auch nach der Frist noch einreichen. Warten Sie aber lieber nicht allzu lange. Es kann vorkommen, dass Ihr Finanzamt einen Verspätungszuschlag einfordert, wenn Sie sich zu viel Zeit lassen.",
      },
      Item4: {
        title: "Kann ich Angaben machen, die meine Steuerlast reduzieren?",
        detailOne:
          "Ja. Sie können eine Vielzahl an Ausgaben beim Steuerlotsen angeben und somit Ihre Steuerlast reduzieren. Zu folgenden Bereichen können Sie Angaben machen:",
        detailTwo:
          "Die <strong>haushaltsnahen Dienstleistungen</strong> und Handwerkerleistungen umfassen im Steuerlotsen <strong>keine Arbeitsverhältnisse</strong>. Sollten Sie Haushaltshilfen als Arbeitnehmer einstellen, können Sie dies im Steuerlotsen nicht steuerlich absetzen.\n\nEine detaillierte Übersicht, welche Angaben zu den Bereichen gehören, finden Sie in unserer Vorbereitungshilfe.\n\n<downloadPreparationLink>Vorbereitungshilfe speichern</downloadPreparationLink>",
        listItem1: "Vorsorgeaufwendungen",
        listItem2: "Spenden und Mitgliedsbeiträge",
        listItem3: "außergewöhnliche Belastungen, wie Krankheitskosten",
        listItem4: "Haushaltsnahe Dienstleistungen",
        listItem5: "Haushaltsnahe Handwerkerleistungen",
        listItem6: "Gezahlte Kirchensteuer",
      },
      Item5: {
        title: "Können wir die Steuererklärung gemeinsam als Paar machen?",
        detail:
          'Ja. Wenn Sie verheiratet sind oder in einer eingetragenen Partnerschaft leben, können Sie Ihre Steuererklärung gemeinsam als Paar machen. Es reicht in diesem Fall aus, wenn sich nur eine Person registriert und unter "Ihre Steuererklärung" für die gemeinsame Steuererklärung anmeldet. Im Steuerformular können Sie dann, zusätzlich zu Ihren Angaben, auch die Daten zu Ihrem Partner oder Ihrer Partnerin eintragen.',
      },
      Item6: {
        title:
          "Kann ich den Service nutzen, wenn ich bereits ein Konto bei ELSTER habe?",
        detail:
          "Sie können den Steuerlotsen vielleicht nutzen. Der Steuerlotse ist nur mit dem Briefersatzverfahren für den Datenabruf von ELSTER nutzbar.\n\nWenn Sie ein ELSTER-Konto und das digitale Verfahren zur Berechtigung für den Datenabruf aktiviert haben, ist die Nutzung des Steuerlotsen Rente nicht möglich. In diesem Falle empfehlen wir Ihnen die Nutzung von ELSTER.\n\nELSTER steht für »Elektronische Steuererklärung« und ist die offizielle Plattform der deutschen Finanzverwaltung.",
      },
      Item7: {
        title: "Wer hat den Steuerlotsen entwickelt?",
        detail:
          "Der Steuerlotse wurde vom <digitalServiceLink>DigitalService</digitalServiceLink> – einer Bundes GmbH – im Auftrag des <bundesfinanzministeriumLink>Bundesfinanzministerium</bundesfinanzministeriumLink> entwickelt. Daneben hat der DigitalService die <grundsteuererklärungLink>“Grundsteuererklärung für Privateigentum”</grundsteuererklärungLink> entwickelt.",
      },
      Item8: {
        title:
          "Für welche Steuerjahre kann ich den Steuerlotsen für meine Steuererklärung nutzen?",
        detail:
          "Der Steuerlotse kann zurzeit nur für die Abgabe einer Steuererklärung für das Steuerjahr 2021 verwendet werden. Für alle früheren Steuerjahre können Sie beispielsweise auf <elsterLink>Mein ELSTER</elsterLink> oder in einigen Bundesländern auch auf das <simplifiedPaperFormLink>vereinfachte Papierformular</simplifiedPaperFormLink> zurückgreifen.",
      },
    },
    ButtonLabel: "Zur Informationsseite",
    InformationButtonPlausibleGoal: "Zur Informationsseite",
  },
  freeTaxDeclarationForPensioners: {
    meta: {
      title: "Kostenlose Steuererklärung für Rentner | Steuerlotse Rente",
      description:
        "Steuererklärungen stellen viele Rentner vor Probleme. Lesen Sie hier, welche (kostenlosen) Beratungsmöglichkeiten bereitstehen.",
      keywords:
        "Steuererklärung Rentner, Steuererklärung für Rentner, Steuererklärung für Rentner kostenlos, Steuererklärung Rentner Pflicht",
    },
    Heading: "Kostenlose Steuererklärung für Rentner – ein Überblick",
    Teaser:
      "Immer mehr Bezieher einer Rente oder Pension werden vom Finanzamt um eine Steuererklärung gebeten. Lesen Sie hier, wieso diese anfällt – und wo Sie Hilfe für die Einkommensteuererklärung erhalten.",
    AnchorList: {
      anchor1: "Voraussetzungen Einkommensteuer",
      anchor2: "Beratungsangebote Rentner",
      anchor3: "Kostenfreie Steuererklärung erstellen",
    },
    Accordion: {
      heading:
        "Die wichtigsten Antworten zu Steuererklärungen für Rentner im Überblick",
      Item1: {
        heading: "Muss ich als Rentner oder Pensionär Einkommensteuer zahlen?",
        detail:
          "Grundsätzlich sind Renten und Pensionen einkommensteuerpflichtig. Liegen Ihre zu versteuernde Einkünfte unter dem Grundfreibetrag, so müssen Sie allerdings keine Steuererklärung beim Finanzamt einreichen.",
      },
      Item2: {
        heading: "Wie hoch ist der Grundfreibetrag?",
        detail:
          "Im Jahr 2020 lag der Grundfreibetrag bei 9.408 Euro, im Jahr 2021 bei 9.744 Euro. 2022 wird der Grundfreibetrag auf 9.984 Euro angehoben.",
      },
      Item3: {
        heading:
          "Bislang musste ich keine Steuererklärung einreichen. Wieso ist das jetzt anders?",
        detail:
          "Einerseits erhöhen sich die Renten in fast jedem Jahr, andererseits nimmt der Besteuerungsanteil stetig zu. Das führt dazu, dass immer mehr Menschen im Ruhestand Einkommensteuer entrichten müssen.",
      },
      Item4: {
        heading: "Welche Beratungsmöglichkeiten stehen mir zur Verfügung?",
        detail:
          "Neben Steuerberatern bieten auch Lohnsteuerhilfevereine ihre Dienste an. Es gibt sogar völlig kostenlose Möglichkeiten der Beratung und Unterstützung.",
      },
    },
    Body: {
      introText:
        "Vielleicht sind Sie Rentnerin oder Rentner und haben Post vom Finanzamt erhalten: Die Behörde fordert Sie möglicherweise auf, eine Einkommensteuererklärung einzureichen. Sie sind damit nicht allein: Knapp sieben Millionen Rentnerinnen und Rentner mussten im Jahr 2017 – aktuellere Daten liegen noch nicht vor – Einkommensteuer auf ihre Renteneinkünfte zahlen. Das bedeutet, dass etwa <destatisLink>jeder dritte Rentenempfänger</destatisLink> in Deutschland eine Steuererklärung bei seinem Finanzamt abgeben muss. Falls dieser Sachverhalt auch auf Sie zutrifft, müssen Sie aber nicht in Sorge geraten: Wir möchten Ihnen aufzeigen, wo Sie Hilfe und Unterstützung finden – und das sogar kostenlos.",
      part1: {
        heading: "Rente und Einkommensteuer",
        introText:
          "Nicht jedem ist bekannt, dass auf Renten und Pensionen Einkommensteuer anfällt. Die <deutscheRente>Deutsche Rentenversicherung</deutscheRente> meldet die relevanten Daten der zuständigen Finanzverwaltung, führt aber keine Steuern an das Finanzamt ab.",
        subHeading1:
          "Rentenfreibetrag und einkommensteuerpflichtiger Teil der Rente",
        text1:
          "Alle Rentenempfänger erhalten einen „Rentenfreibetrag“: Hierbei handelt es sich um einen festen Eurobetrag, auf den keine Steuern anfallen. Die Höhe des Anteils des Rentenfreibetrags hängt von dem Jahr ab, in dem Sie erstmals eine Rente erhalten. Liegt der erstmalige Erhalt einer Rente zum Beispiel im Jahr 2020, unterliegen 20 Prozent Ihrer Rente keiner Einkommensteuer. Bekommen Sie Ihre erste Rente im Jahr 2021, dann sind es nur noch 19 Prozent. Im Folgejahr sind es 18 Prozent für Bezieher der ersten Rentenzahlung und so weiter. Grund hierfür ist die sogenannte „nachgelagerte Besteuerung“, für die sich der Gesetzgeber im Jahr 2005 entschieden hat.",
        example1:
          "<bold>Beispiel:</bold> Herr Mayer ist ledig und erhält erstmals im Jahr 2020 eine Jahresbruttorente von 14.000 Euro. 80 Prozent hiervon müssen versteuert werden: Das sind 11.200 Euro, der Rentenfreibetrag beläuft sich auf 2.800 Euro. Sollte Herr Mayer aufgrund einer Erhöhung seiner Rente fünf Jahre später 15.000 Euro Rente erhalten, ändert das nichts am Rentenfreibetrag: Dieser bleibt bei 2.800 Euro, sodass 12.200 Euro versteuert werden müssen.",
        text2:
          "Bei Pensionen ist das anders: Sie werden bereits jetzt in voller Höhe versteuert. Als „Pensionen“ gelten jene Bezüge, welche Beamtinnen und Beamte im Ruhestand erhalten.",
        subHeading2: "Grundfreibetrag: Ab wann Einkommensteuer anfällt",
        text3:
          "Neben dem Rentenfreibetrag gibt es noch den Grundfreibetrag. Letzterer hat zur Folge, dass die Einkommensteuer erst ab einem bestimmten <bfinm>Schwellenwert</bfinm> greift: Im Jahr 2020 lag dieser bei 9.408 Euro, ein Jahr später bei 9.744 Euro, anno 2022 wird er auf 9.984 Euro angehoben.",
        example2:
          "<bold>Beispiel:</bold> Für Herrn Mayer, Bezieher einer Rente, hat das zur Folge, dass im Jahr 2020 auf lediglich 1.792 Euro (11.200 Euro minus 9.408 Euro) Einkommensteuer anfällt. Würde Herr Mayer übrigens eine jährliche Pension in Höhe von 14.000 Euro erhalten, so würden 4.592 Euro der Einkommensteuer unterliegen (14.000 Euro minus 9.408 Euro).",
        text4:
          "Aufgrund der oben beschriebenen Anpassung des Rentenfreibetrags und den Erhöhungen der Renten zahlen immer mehr Menschen im Ruhestand Einkommensteuer.",
      },
      ShareBox: {
        header: "Artikel weiterempfehlen",
        text: "Dieser Artikel könnte auch hilfreich für Ihre Freunde oder Bekannten sein.",
        promoteUrl:
          "https://www.steuerlotse-rente.de/kostenlose-steuererklaerung-rentner",
        shareText:
          "Diesen Artikel beim Steuerlotsen für Rente und Pension finde ich interessant: https://www.steuerlotse-rente.de/kostenlose-steuererklaerung-rentner",
        mailSubject: "Artikel beim Steuerlotsen für Rente und Pension",
        sourcePage: "FreeTaxDeclarationForPensionersPage",
      },
      part2: {
        heading:
          "An diese Stellen können Sie sich bei Fragen zur Einkommensteuer wenden",
        introText:
          "Wenn Sie das Finanzamt auffordert, eine Steuererklärung abzugeben, gilt es einige Punkte zu beachten. Zum Beispiel diese:",
        subHeading1: "Fristverlängerung und Formulare im Internet",
        text1:
          "Sie finden im Schreiben der Behörde ein Datum, an dem Ihre Erklärung spätestens eingereicht werden sollte. Falls absehbar ist, dass ein fristgerechtes Einbringen der Steuererklärung nicht mehr möglich ist, stellt das üblicherweise kein Problem dar: Bitten Sie Ihr zuständiges Finanzamt einfach um eine Fristverlängerung. Ein formloses Schreiben ist völlig ausreichend. Falls Sie bereits sehr versiert im Umgang mit Ihrer Steuererklärung sind, können Sie diese elektronisch über <elster>ELSTER</elster> vornehmen. Die notwendigen Vordrucke finden Sie außerdem auf dem <bfinv>Formularserver der Finanzverwaltung</bfinv> oder direkt bei Ihrem Finanzamt. ",
        tipp: "<bold>Tipp:</bold> Sie können Ihre Steuererklärung auch kostenlos direkt mit dem <steuerlotse>Steuerlotsen</steuerlotse> erledigen. Dazu brauchen Sie keinen Elster-Account! ",
        subHeading2:
          "Beratung beim Finanzamt, Lohnsteuerverein oder Steuerberater",
        text2:
          "Tauchen beim Ausfüllen der Formulare Fragen auf, zögern Sie nicht, diese an Ihr Finanzamt zu richten. Viele dieser Behörden bieten persönliche Beratungsgespräche und telefonische Hilfestellung an. Eine kostengünstige Möglichkeit, Beratung einzuholen und die Steuererklärung an fachkundige Personen zu delegieren, sind sogenannte „Lohnsteuerhilfevereine“. Die Mitgliedschaft in einem solchen Verein hängt von der Höhe des Einkommens ab und kostet in der Regel zwischen 50 und 400 Euro jährlich. Deutlich teurer fallen die Dienste eines Steuerberaters aus. Allerdings geht die Inanspruchnahme eines Lohnsteuerhilfevereins oder Steuerberaters mit einem großen Vorteil einher: Die Frist zur Abgabe der Steuererklärung verlängert sich automatisch um sieben Monate!",
      },
      part3: {
        heading: "Kostenlose Steuererklärung für Rentner mit dem Steuerlotsen",
        introText:
          "Falls Sie eine Rente oder Pension beziehen und keine weiteren Einkünfte erzielen, gibt es neben den oben genannten Beratungsangeboten eine weitere Möglichkeit: Der <steuerlotse>Steuerlotse</steuerlotse> wurde im Auftrag des Bundesfinanzministeriums entwickelt und verfolgt daher keine kommerziellen Absichten. Im Gegenteil: Die Nutzung des Dienstes ist völlig kostenfrei. Er richtet sich gezielt an Menschen im Ruhestand. Die Installation eines gesonderten Programms ist nicht erforderlich, die Internetseite führt Sie bequem durch die Steuererklärung.",
        subHeading1: "So funktioniert der Steuerlotse",
        text1:
          "Um sich <steuerlotseRegister>beim Steuerlotsen zu registrieren</steuerlotseRegister>, reichen Angaben zu Ihrem Geburtsdatum und Ihrer Steuer-Identifikationsnummer aus. Binnen zwei Wochen erhalten Sie einen Brief mit einem persönlichen Freischaltcode. Übrigens: Falls Sie eine gemeinsame Veranlagung als Paar vornehmen möchten, weil Sie verheiratet sind oder in einer eingetragenen Lebenspartnerschaft leben, ist das problemlos möglich. Es reicht aus, wenn sich eine Person registriert.",
        text2:
          "Selbstverständlich berücksichtigt der Steuerlotse auch jene Ausgaben, die Ihre Steuerlast verringern. So können Sie unter anderem gezahlte Kirchensteuer, Spenden und Mitgliedsbeiträge sowie außergewöhnliche Belastungen steuerlich geltend machen.",
      },
      button: {
        label: "Zum Steuerlotsen für Rente und Pension",
        plausibleGoal: "contentPage_freeTaxDeclaration_clicked",
        url: "/",
      },
    },
  },
  mandateForTaxDeclaration: {
    meta: {
      title: "Steuererklärung für Eltern machen | Steuerlotse Rente",
      description:
        "Viele Rentner müssen eine Steuererklärung abgeben. Wie können Kinder die Steuererklärung für ihre Eltern machen? Mehr erfahren!",
      keywords:
        "Steuererklärung für Eltern machen (40), Steuererklärung Eltern Unterstützung (20), Steuererklärung Unterstützung Eltern wo eintragen (10), Vollmacht Finanzamt Eltern (30)",
    },
    Heading: "Steuererklärung für Eltern machen (inkl. Vollmacht-Vorlage)",
    Teaser:
      "Immer mehr Rentner und Rentnerinnen müssen eine Steuererklärung abgeben. Viele von ihnen sind damit jedoch überfordert. Wir erklären, wie Sie als Angehöriger die Steuererklärung für Ihre Eltern machen können und was Sie dabei beachten sollten.",
    AnchorList: {
      anchor1: "Wie entsteht die Steuerpflicht?",
      anchor2: "Wer darf bei der Steuererklärung helfen?",
      anchor3: "Vollmacht für das Finanzamt ausstellen",
      anchor4: "Mit dem Steuerlotsen Steuererklärungen erledigen",
    },
    Accordion: {
      heading:
        "Die wichtigsten Antworten zum Thema „Steuererklärung für Eltern machen“ im Überblick:",
      Item1: {
        heading: "Warum müssen immer mehr Rentner eine Steuererklärung machen?",
        detail:
          "Im Jahr 2020 hat die Bundesregierung die Rente erhöht. Auf diese Weise überschreiten immer mehr Menschen im Ruhestand den Freibetrag – also den Betrag, den sie pro Jahr steuerfrei einnehmen dürfen. Heute zahlen daher rund sieben Millionen der gut 21 Millionen Rentenbeziehenden eine Einkommensteuer. Das heißt auch: Sie müssen eine Steuererklärung abgeben.",
      },
      Item2: {
        heading: "Wer kann Rentnern bei der Steuererklärung helfen?",
        detail:
          "Grundsätzlich können Angehörige Rentnern bei ihrer Steuererklärung helfen. Oftmals bieten Kinder ihren Eltern eine Unterstützung für die Steuererklärung an.",
      },
      Item3: {
        heading:
          "Wo müssen Eltern die Unterstützung durch ihre Kinder in der Steuererklärung angeben?",
        detail:
          "Eltern können im Mantelbogen der Steuererklärung angeben, dass ihre Kinder ihnen bei der Steuererklärung geholfen haben.",
      },
      Item4: {
        heading:
          "Wie können Rentner eine Vollmacht für das Finanzamt ausstellen?",
        detail:
          "Eine rechtssichere Vollmacht für das Finanzamt benötigt den Namen des Rentners, seine Anschrift, den des bevollmächtigten Kindes (oder eines anderen Angehörigen), das aktuelle Datum und die Unterschrift des Rentners. Alternativ können Sie einfach diese <bfinm>Vollmacht-Vorlage</bfinm> nutzen.",
      },
    },
    Body: {
      introText:
        "Ihre Eltern haben ihr Leben lang gearbeitet und fleißig in die Rentenkasse eingezahlt. Jetzt im Ruhestand erhalten sie jeden Monat Geld – ohne etwas dafür tun zu müssen. Ganz so einfach ist es für Rentner dann aber doch nicht. Denn: Immer mehr Menschen im Ruhestand müssen Steuern zahlen. Das bedeutet auch: Sie müssen eine Steuererklärung abgeben. Viele Rentner suchen daher Unterstützung bei ihren Kindern. Wie können Sie als Angehöriger also die Steuererklärung für Ihre Eltern machen? Und was sollten Sie dabei beachten?",
      part1: {
        heading: "Warum müssen immer mehr Rentner eine Steuererklärung machen?",
        text1:
          "Im Juli 2020 erhöhte die Bundesregierung die Rente. Seitdem erhalten Menschen in Westdeutschland 3,45 Prozent und Menschen in Ostdeutschland 4,2 Prozent <vlh>mehr Rente</vlh>. Das war für ältere Menschen grundsätzlich eine gute Nachricht. Mehr Geld heißt im Ruhestand mehr Lebensqualität!",
        text2:
          "Die höhere Rente bedeutet jedoch auch, dass viele Rentner und Pensionäre die Mehreinnahmen vollständig versteuern müssen. Das passiert, sobald das Einkommen aus ihrer Rente den Grundfreibetrag überschreitet. Dieser liegt im Jahr 2022 bei 9.984 Euro.",
        text3:
          "Für die Praxis hieß das: Im Jahr 2020 rutschten plötzlich rund 51.000 Rentner neu in die Steuerpflicht. Das schätzt das <finanztip>Bundesfinanzministerium</finanztip>. Heute zahlen knapp sieben Millionen der gut 21 Millionen Rentenbeziehenden in Deutschland eine Einkommensteuer. Das bedeutet für die Rentner: Sie müssen jedes Jahr immer wieder eine Steuererklärung abgeben – eine für ältere Menschen manchmal nicht einfache Aufgabe.",
      },
      ShareBox: {
        header: "Artikel weiterempfehlen",
        text: "Dieser Artikel könnte auch hilfreich für Ihre Freunde oder Bekannten sein.",
        promoteUrl:
          "https://www.steuerlotse-rente.de/steuererklärung-eltern-vollmacht",
        shareText:
          "Diesen Artikel beim Steuerlotsen für Rente und Pension finde ich interessant: https://www.steuerlotse-rente.de/steuererklärung-eltern-vollmacht",
        mailSubject: "Artikel beim Steuerlotsen für Rente und Pension",
        sourcePage: "MandateForTaxDeclarationPage",
      },
      part2: {
        heading: "Wann müssen Rentner tatsächlich Steuern zahlen?",
        text1:
          "Ob ein Rentner tatsächlich eine Steuererklärung abgeben und Steuern zahlen muss, hängt davon ab...",
        list: {
          item1: "...wie viel Rente er bekommt.",
          item2: "...wann er zum ersten Mal Rente bezogen hat.",
          item3: "...wie hoch der steuerpflichtige Anteil seiner Rente ist.",
          item4: "...ob er verheiratet ist.",
          item5:
            "...wie viel Versicherungsbeiträge und Krankheitskosten er zahlt.",
          item6:
            "...ob er mit seinen Einnahmen über dem <mdr>jährlichen Freibetrag</mdr> liegt.",
        },
        text2:
          "Wann genau Rentner und Rentnerinnen eine Steuererklärung abgeben müssen, hat die Finanzverwaltung NRW in einem anschaulichen Video erklärt:",
      },
      part3: {
        heading: "Wer darf Rentnern bei der Steuererklärung helfen?",
        text1:
          "Eigentlich hatten Ihre Eltern bereits einen großen Haken an das Thema Arbeit und Steuern gemacht – und plötzlich sollen sie doch wieder eine Steuererklärung machen. Wer kann ihnen dabei helfen?",
        text2:
          "Grundsätzlich dürfen Kinder ihren Eltern Unterstützung bei der Steuererklärung anbieten. Daneben dürfen ihnen auch:",
        list: {
          item1: "Ehegatten",
          item2: "geschiedene Ehepartner",
          item3: "Lebenspartner",
          item4: "Verlobte",
          item5: "Verwandte und Verschwägerte gerader Linie",
          item6: "Geschwister",
          item7: "Kinder der Geschwister",
          item8: "Ehegatten oder Lebenspartner der Geschwister",
          item9: "Geschwister der Ehegatten oder Lebenspartner",
          item10: "Geschwister der Eltern",
          item11: "Pflegeeltern und Pflegekinder",
        },
        text3:
          "bei der <steuertipps>Steuererklärung helfen</steuertipps>. Das muss jedoch kostenlos sein!",
        subHeading1:
          "Wo müssen Kinder die Unterstützung ihrer Eltern bei der Steuererklärung eintragen?",
        text4:
          "Möchten Angehörige Rentner oder Pensionäre bei der Steuererklärung unterstützen, sollten sie diesen Umstand bei der Steuererklärung angeben. Sie können die <steuertipps>Hilfe im Mantelbogen der Steuererklärung</steuertipps> im Feld „Bei der Anfertigung dieser Steuererklärung hat mitgewirkt“ angeben. Dabei sollten sie auch das Verwandtschaftsverhältnis mitteilen.",
      },
      part4: {
        heading:
          "Wie können Eltern eine Vollmacht für das Finanzamt ausstellen?",
        text1:
          "Steuererklärung anfertigen, Bescheid auslesen und eventuelle Nachzahlungen tätigen: Um im Ruhestand auch die wohlverdiente Ruhe zu genießen, können Eltern ihren Kindern eine Vollmacht für das Finanzamt ausstellen. Die Kinder übernehmen in diesem Fall jegliche Steuerangelegenheiten.",
        text2: "Damit eine Vollmacht wirksam ist, sollte diese:",
        list: {
          item1: "Namen des Rentners",
          item2: "Anschrift des Rentners",
          item3:
            "Namen des bevollmächtigten Kindes (oder eines anderen Angehörigen)",
          item4: "Aktuelles Datum",
          item5: "Unterschrift des Rentners",
        },
        text3:
          "enthalten. Damit Sie dabei auf der sicheren Seite stehen, haben wir für Sie eine wasserdichte <bfinm>Vollmacht-Vorlage</bfinm> erstellt.",
      },
      part5: {
        heading:
          "Mit dem Steuerlotsen die Steuererklärung in wenigen Minuten erledigen",
        text1:
          "Wenn Sie die Steuererklärung für Ihre Eltern machen möchten, schaffen Sie das mit dem Steuerlotsen schnell und unkompliziert!",
        text2:
          "Der Steuerlotse ist ein Online-Tool für Rentner und Pensionäre, mit dem Sie intuitiv und ganz ohne Vorkenntnisse in wenigen Minuten die Steuererklärung für Ihre Eltern erledigen. Dazu gibt Ihnen der Steuerlotse eine Schritt-für-Schritt-Anleitung an die Hand, die Sie schnell und unkompliziert durch Ihre Steuern führt. Das Beste daran: Das Angebot wurde im Auftrag des Bundesfinanzministeriums entwickelt und ist daher kostenlos!",
      },
      button: {
        label: "Jetzt Ihre Steuererklärung mit dem Steuerlotsen erledigen!",
        plausibleGoal: "contentPage_mandateForTaxDeclaration_clicked",
        url: "/eligibility/step/tax_year?link_overview=False",
      },
    },
  },
};

export default translations;
