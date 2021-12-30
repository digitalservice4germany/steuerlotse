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
      cy.visit("/lotse/step/person_b_has_disability");
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
      cy.visit("/lotse/step/person_b_has_disability");
    });

    it("Should check radio button for label yes", () => {
      cy.get("#person_b_has_disabilityyes").should("be.checked");
    });

    it("Should not check radio button for label no", () => {
      cy.get("#person_b_has_disabilityno").should("not.be.checked");
    });

    it("Should link forward to person b merkzeichen page", () => {
      cy.get("button[type=submit]").click();
      cy.url().should("include", "/lotse/step/telephone_number");
      // TODO cy.url().should("include", "/lotse/step/merkzeichen_person_b");
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
      cy.visit("/lotse/step/person_b_has_disability");
    });

    it("Should check radio button for label no", () => {
      cy.get("#person_b_has_disabilityno").should("be.checked");
    });

    it("Should not check radio button for label yes", () => {
      cy.get("#person_b_has_disabilityyes").should("not.be.checked");
    });
  });
});
