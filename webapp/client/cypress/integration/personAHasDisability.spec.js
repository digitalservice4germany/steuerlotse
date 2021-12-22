describe("PersonAHasDisability", () => {
  beforeEach(() => {
    cy.login();
  });

  context("with no data", () => {
    beforeEach(() => {
      // Default is single and no tax joint
      cy.request("POST", "/testing/set_data/form_data", {
        familienstand: "single",
        familienstand_confirm_zusammenveranlagung: false,
      });

      cy.visit("/lotse/step/person_a_has_disability");
    });

    it("Should link back to person a page", () => {
      cy.get("a").contains("Zurück").click();
      cy.url().should("include", "/lotse/step/person_a");
    });

    it("Should link forward to telephone number page", () => {
      cy.get("button[type=submit]").click();
      cy.url().should("include", "/lotse/step/telephone_number");
    });
  });

  context("with person_a_has_disability yes", () => {
    beforeEach(() => {
      cy.request("POST", "/testing/set_data/form_data", {
        person_a_has_disability: "yes",
      });

      cy.visit("/lotse/step/person_a_has_disability");
    });

    it("Should check radio button for label yes", () => {
      cy.get("#person_a_has_disabilityyes").should("be.checked");
    });

    it("Should not check radio button for label no", () => {
      cy.get("#person_a_has_disabilityno").should("not.be.checked");
    });
  });

  context("with person_a_has_disability no", () => {
    beforeEach(() => {
      cy.request("POST", "/testing/set_data/form_data", {
        person_a_has_disability: "no",
      });
      cy.visit("/lotse/step/person_a_has_disability");
    });

    it("Should check radio button for label no", () => {
      cy.get("#person_a_has_disabilityno").should("be.checked");
    });

    it("Should not check radio button for label yes", () => {
      cy.get("#person_a_has_disabilityyes").should("not.be.checked");
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
      cy.visit("/lotse/step/person_a_has_disability");
    });

    it("Should link back to person b page", () => {
      cy.get("a").contains("Zurück").click();
      cy.url().should("include", "/lotse/step/person_a");
    });

    it("Should link forward to telephone number page", () => {
      cy.get("button[type=submit]").click();
      cy.url().should("include", "/lotse/step/person_b");
    });
  });
});
