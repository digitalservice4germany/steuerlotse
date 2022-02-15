describe("Logout", () => {
  beforeEach(() => {
    cy.login();
  });

  it("has no back link", () => {
    cy.visit("logout");
    cy.get("a").contains("Zurück").should("not.exist");
    cy.extended_footer_is_disabled(false);
  });

  it("logout to login page", () => {
    cy.visit("logout");
    cy.get("button[type=submit]").contains("Abmelden").click();

    cy.url().should("include", "unlock_code_activation/step/data_input");

    cy.get("div[class*=alert-success]").contains(
      "Sie haben sich erfolgreich abgemeldet."
    );
    cy.extended_footer_is_disabled(false);
  });

  it("logout to start page because of completed tax return", () => {
    cy.request("POST", "/testing/set_session_data/form_data", {
      idnr: "04452397687",

      declaration_incomes: true,
      declaration_edaten: true,

      steuernummer_exists: "yes",
      bundesland: "BY",
      steuernummer: "19811310010",

      familienstand: "ledig",

      person_a_idnr: "04452397687",
      person_a_dob: "1950-08-16",
      person_a_first_name: "Manfred",
      person_a_last_name: "Mustername",
      person_a_street: "Steuerweg",
      person_a_street_number: 42,
      person_a_street_number_ext: "a",
      person_a_address_ext: "Seitenflügel",
      person_a_plz: "20354",
      person_a_town: "Hamburg",
      person_a_religion: "none",
      person_a_has_disability: "no",
      person_a_has_pflegegrad: "no",

      is_user_account_holder: "yes",

      iban: "DE35133713370000012345",

      stmind_select_vorsorge: false,
      stmind_select_ausserg_bela: false,
      stmind_select_handwerker: false,
      stmind_select_religion: false,
      stmind_select_spenden: false,

      confirm_complete_correct: true,
      confirm_data_privacy: true,
      confirm_terms_of_service: true,
    });

    cy.visit("/lotse/step/confirmation");

    cy.get("button[type=submit]").contains("Steuererklärung abgeben").click();

    cy.visit("logout");

    cy.url().should("not.contain", "logout");

    cy.get("div[class*=alert-success]").contains(
      "Sie haben sich erfolgreich abgemeldet."
    );
    cy.extended_footer_is_disabled(false);
  });
});
