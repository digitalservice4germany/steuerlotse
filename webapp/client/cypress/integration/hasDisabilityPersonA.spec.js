describe("PersonAHasDisability", () => {
  beforeEach(() => {
    cy.login();
  });

  context("with no data", () => {
    beforeEach(() => {
      cy.visit("/lotse/step/has_disability_person_a");
    });

    it("Should link back to person a page", () => {
      cy.get("a").contains("Zurück").click();
      cy.url().should("include", "/lotse/step/person_a");
    });
  });

  context("with person_a_has_disability yes", () => {
    beforeEach(() => {
      cy.request("POST", "/testing/set_data/form_data", {
        person_a_has_disability: "yes",
      });

      cy.visit("/lotse/step/has_disability_person_a");
    });

    it("Should check radio button for label yes", () => {
      cy.get("#person_a_has_disabilityyes").should("be.checked");
    });

    it("Should not check radio button for label no", () => {
      cy.get("#person_a_has_disabilityno").should("not.be.checked");
    });

    it("Should link back to person a page", () => {
      cy.get("a").contains("Zurück").click();
      cy.url().should("include", "/lotse/step/person_a");
    });

    it("Should link forward to merkzeichen_person_a", () => {
      cy.get("button[type=submit]").click();
      cy.url().should("include", "/lotse/step/merkzeichen_person_a");
    });
  });

  context("with person_a_has_disability no", () => {
    beforeEach(() => {
      cy.request("POST", "/testing/set_data/form_data", {
        person_a_has_disability: "no",
      });
      cy.visit("/lotse/step/has_disability_person_a");
    });

    it("Should check radio button for label no", () => {
      cy.get("#person_a_has_disabilityno").should("be.checked");
    });

    it("Should not check radio button for label yes", () => {
      cy.get("#person_a_has_disabilityyes").should("not.be.checked");
    });

    it("Should link forward to telephone_number page", () => {
      cy.get("button[type=submit]").click();
      cy.url().should("include", "/lotse/step/telephone_number");
    });
  });

  context("for joint taxes", () => {
    beforeEach(() => {
      cy.request("POST", "/testing/set_data/form_data", {
        familienstand: "married",
        familienstand_married_lived_separated: "no",
        familienstand_confirm_zusammenveranlagung: true,
        person_a_has_disability: "no",
      });
      cy.visit("/lotse/step/merkzeichen_person_a");
    });

    it("Should link forward to person b page", () => {
      cy.get("button[type=submit]").click();
      cy.url().should("include", "/lotse/step/person_b");
    });
  });
});
