describe("Filing", () => {
  beforeEach(() => {
    cy.login();
  });

  context("success", () => {
    beforeEach(() => {
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
      cy.visit("/lotse/step/filing");
    });

    it("downloading pdf is possible", () => {
      cy.window()
        .document()
        .then(function (doc) {
          doc.addEventListener("click", () => {
            setTimeout(function () {
              doc.location.reload();
            }, 1000);
          });
          // Downloads folder is automatically cleared
          cy.get("a").contains("Übersicht speichern").click();
          cy.readFile("cypress/downloads/AngabenSteuererklaerung.pdf").should(
            "exist"
          );
        });
    });

    it("going to next step is possible", () => {
      cy.get("a").contains("Weiter").click();
      cy.url().should("include", "/lotse/step/ack");
    });
  });

  context("failure", () => {
    beforeEach(() => {});
  });
});
