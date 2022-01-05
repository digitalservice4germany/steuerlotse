describe("PersonBHasDisability", () => {
  beforeEach(() => {
    cy.login();
  });

  context("with no data", () => {
    beforeEach(() => {
      // precondition of person_b_has_disability
      cy.request("POST", "/testing/set_data/form_data", {
        familienstand: "married",
        familienstand_married_lived_separated: "no",
        familienstand_confirm_zusammenveranlagung: true,
      });
      cy.visit("/lotse/step/has_disability_person_b");
    });

    it("Should link back to person b page", () => {
      cy.get("a").contains("Zurück").click();
      cy.url().should("include", "/lotse/step/person_b");
    });
  });

  context("with person_b_has_disability yes", () => {
    beforeEach(() => {
      cy.request("POST", "/testing/set_data/form_data", {
        familienstand: "married",
        familienstand_married_lived_separated: "no",
        familienstand_confirm_zusammenveranlagung: true,
        person_b_has_disability: "yes",
      });
      cy.visit("/lotse/step/has_disability_person_b");
    });

    it("Should check radio button for label yes", () => {
      cy.get("#person_b_has_disability-yes").should("be.checked");
    });

    it("Should not check radio button for label no", () => {
      cy.get("#person_b_has_disability-no").should("not.be.checked");
    });

    it("Should link forward to merkzeichen person b page", () => {
      cy.get("button[type=submit]").click();
      cy.url().should("include", "/lotse/step/merkzeichen_person_b");
    });
  });

  context("with person_b_has_disability no", () => {
    beforeEach(() => {
      cy.request("POST", "/testing/set_data/form_data", {
        familienstand: "married",
        familienstand_married_lived_separated: "no",
        familienstand_confirm_zusammenveranlagung: true,
        person_b_has_disability: "no",
      });
      cy.visit("/lotse/step/has_disability_person_b");
    });

    it("Should check radio button for label no", () => {
      cy.get("#person_b_has_disability-no").should("be.checked");
    });

    it("Should not check radio button for label yes", () => {
      cy.get("#person_b_has_disability-yes").should("not.be.checked");
    });

    it("Should link forward to telephone number page", () => {
      cy.get("button[type=submit]").click();
      cy.url().should("include", "/lotse/step/telephone_number");
    });
  });
});
