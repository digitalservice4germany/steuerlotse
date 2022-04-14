from app.config import Config

aendern = 'ändern'
uebersicht = 'Zurück zur Übersicht'
domain = Config.PLAUSIBLE_DOMAIN

plausible_data_cta = {
    'decl_incomes_summary': {
        'domain': domain,
        'target': aendern,
        'source': 'CTA Eingabe zu weiteren Einkünften'
    },
    'decl_edaten_summary': {
        'domain': domain,
        'target': aendern,
        'source': 'CTA Übernahme vorliegender Daten'
    },
    'steuernummer_summary': {
        'domain': domain,
        'target': aendern,
        'source': 'CTA Steuernummer'
    },
    'familienstand': {
        'domain': domain,
        'target': uebersicht,
        'source': 'CTA Familienstand'
    },
    'familienstand_summary': {
        'domain': domain,
        'target': aendern,
        'source': 'CTA Familienstand'
    },
    'iban': {
        'domain': domain,
        'target': uebersicht,
        'source': 'CTA Bankverbindung'
    },
    'iban_summary': {
        'domain': domain,
        'target': aendern,
        'source': 'CTA Bankverbindung'
    },
    'person_a': {
        'domain': domain,
        'target': uebersicht,
        'source': 'CTA Person A'
    },
    'person_a_summary': {
        'domain': domain,
        'target': aendern,
        'source': 'CTA Person A'
    },
    'has_disability_person_a_summary': {
        'domain': domain,
        'target': aendern,
        'source': 'Behinderung oder Pflegebedürftigkeit für Person A'
    },
    'merkzeichen_person_a_summary': {
        'domain': domain,
        'target': aendern,
        'source': 'CTA Angaben zur festgestellten Behinderung oder Pflegebedürftigkeit Person A'
    },
    'person_a_requests_pauschbetrag_summary': {
        'domain': domain,
        'target': aendern,
        'source': 'CTA Pauschbetrag für Menschen mit Behinderung für Person A'
    },
    'person_a_requests_fahrtkostenpauschale_summary': {
        'domain': domain,
        'target': aendern,
        'source': 'CTA Behinderungsbedingte Fahrtkostenpauschale für Person A'
    },
    'person_b': {
        'domain': domain,
        'target': uebersicht,
        'source': 'CTA Person B'
    },
    'person_b_summary': {
        'domain': domain,
        'target': aendern,
        'source': 'CTA Person B'
    },
    'has_disability_person_b_summary': {
        'domain': domain,
        'target': aendern,
        'source': 'Behinderung oder Pflegebedürftigkeit für Person B'
    },
    'merkzeichen_person_b_summary': {
        'domain': domain,
        'target': aendern,
        'source': 'CTA Angaben zur festgestellten Behinderung oder Pflegebedürftigkeit Person B'
    },
    'person_b_requests_pauschbetrag_summary': {
        'domain': domain,
        'target': aendern,
        'source': 'CTA Pauschbetrag für Menschen mit Behinderung für Person B'
    },
    'person_b_requests_fahrtkostenpauschale_summary': {
        'domain': domain,
        'target': aendern,
        'source': 'CTA Behinderungsbedingte Fahrtkostenpauschale für Person B'
    },
    'vorsorge': {
        'domain': domain,
        'target': uebersicht,
        'source': 'CTA Vorsorgeaufwendungen'
    },
    'vorsorge_summary': {
        'domain': domain,
        'target': aendern,
        'source': 'CTA Vorsorgeaufwendungen'
    },
    'ausserg_bela': {
        'domain': domain,
        'target': uebersicht,
        'source': 'CTA Krankheitskosten und weitere außergewöhnliche Belastungen'
    },
    'ausserg_bela_summary': {
        'domain': domain,
        'target': aendern,
        'source': 'CTA Krankheitskosten und weitere außergewöhnliche Belastungen'
    },
    'haushaltsnahe_handwerker': {
        'domain': domain,
        'target': uebersicht,
        'source': 'CTA Haushaltsnahe Dienstleistungen und Handwerkerleistungen'
    },
    'haushaltsnahe_handwerker_summary': {
        'domain': domain,
        'target': aendern,
        'source': 'CTA Haushaltsnahe Dienstleistungen und Handwerkerleistungen'
    },
    'religion': {
        'domain': domain,
        'target': uebersicht,
        'source': 'CTA Steuern für Ihre Religionsgemeinschaft'
    },
    'religion_summary': {
        'domain': domain,
        'target': aendern,
        'source': 'CTA Steuern für Ihre Religionsgemeinschaft'
    },
    'spenden': {
        'domain': domain,
        'target': uebersicht,
        'source': 'CTA Spenden und Mitgliedsbeiträge'
    },
    'spenden_summary': {
        'domain': domain,
        'target': aendern,
        'source': 'CTA Spenden und Mitgliedsbeiträge'
    },
    'telefonnummer_summary': {
        'domain': domain,
        'target': aendern,
        'source': 'CTA Telefonnummer für Rückfragen'
    },
    'select_stmind_summary': {
        'domain': domain,
        'target': aendern,
        'source': 'CTA Steuermindernde Aufwendungen'
    },
}
