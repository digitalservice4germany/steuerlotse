describe("TelephoneNumber", () => {
  beforeEach(() => {
    cy.login();
  });

  context("with no data", () => {
    beforeEach(() => {
      cy.visit("/lotse/step/telephone_number");
    });

    it("Should link back to person a has disability page", () => {
      cy.get("a").contains("Zurück").click();
      cy.url().should("include", "/lotse/step/has_disability_person_a");
    });

    it("Should link forward to iban page", () => {
      cy.get("button[type=submit]").click();
      cy.url().should("include", "/lotse/step/iban");
    });
  });

  context("for separated taxes", () => {
    beforeEach(() => {
      cy.request("POST", "/testing/set_data/form_data", {
        familienstand: "single",
      });
      cy.visit("/lotse/step/telephone_number");
    });

    it("Should link back to person a has disability page", () => {
      cy.get("a").contains("Zurück").click();
      cy.url().should("include", "/lotse/step/has_disability_person_a");
    });
  });

  context("for joint taxes", () => {
    beforeEach(() => {
      cy.request("POST", "/testing/set_data/form_data", {
        familienstand: "married",
        familienstand_date: "02.09.2022",
        familienstand_married_lived_separated: "no",
        familienstand_confirm_zusammenveranlagung: true,
      });
      cy.visit("/lotse/step/telephone_number");
    });

    it("Should link back to person b has disability page", () => {
      cy.get("a").contains("Zurück").click();
      cy.url().should("include", "/lotse/step/has_disability_person_b");
    });
  });
});
