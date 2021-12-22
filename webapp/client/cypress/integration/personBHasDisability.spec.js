describe("PersonBHasDisability", () => {
  beforeEach(() => {
    cy.login();
  });

  context("with no data", () => {
    beforeEach(() => {
      cy.visit("/lotse/step/person_b_has_disability");
    });

    it("Should link back to person b page", () => {
      cy.get("a").contains("Zurück").click();
      cy.url().should("include", "/lotse/step/person_b");
    });

    it("Should link forward to telephone number page", () => {
      cy.get("button[type=submit]").click();
      cy.url().should("include", "/lotse/step/telephone_number");
    });
  });

  context("with person_b_has_disability yes", () => {
    beforeEach(() => {
      cy.request("POST", "/testing/set_data/form_data", {
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
  });

  context("with person_b_has_disability no", () => {
    beforeEach(() => {
      cy.request("POST", "/testing/set_data/form_data", {
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
