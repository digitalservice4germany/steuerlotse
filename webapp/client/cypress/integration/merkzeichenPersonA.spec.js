describe("merkzeichenPersonA", () => {
  beforeEach(() => {
    cy.login();
  });

  context("with no data", () => {
    beforeEach(() => {
      cy.visit("/lotse/step/merkzeichen_person_a");
    });

    it("Should redirect to person a has disability page", () => {
      cy.location().should((loc) => {
        expect(loc.pathname.toString()).to.contain(
          "/lotse/step/has_disability_person_a"
        );
      });
    });
  });

  context("with person_a_has_disability no", () => {
    beforeEach(() => {
      cy.request("POST", "/testing/set_data/form_data", {
        person_a_has_disability: "no",
      });
      cy.visit("/lotse/step/merkzeichen_person_a");
    });

    it("Should redirect to person a has disability page", () => {
      cy.location().should((loc) => {
        expect(loc.pathname.toString()).to.contain(
          "/lotse/step/has_disability_person_a"
        );
      });
    });
  });

  context("with person_a_has_disability yes", () => {
    beforeEach(() => {
      cy.request("POST", "/testing/set_data/form_data", {
        person_a_has_disability: "yes",
      });
      cy.visit("/lotse/step/merkzeichen_person_a");
    });

    it("Should not link to next page when submit button clicked", () => {
      cy.get("button[type=submit]").click();
      cy.url().should("include", "/lotse/step/merkzeichen_person_a");
    });
  });

  context("with person a disability data set", () => {
    beforeEach(() => {
      cy.request("POST", "/testing/set_data/form_data", {
        person_a_has_disability: "yes",

        person_a_has_pflegegrad: "no",
        person_a_disability_degree: 25,
        person_a_has_merkzeichen_bl: true,
        person_a_has_merkzeichen_tbl: true,
        person_a_has_merkzeichen_h: false,
        person_a_has_merkzeichen_g: true,
        person_a_has_merkzeichen_ag: false,
      });

      cy.visit("/lotse/step/merkzeichen_person_a");
    });

    it("Should set pflegegrad correctly", () => {
      cy.get("#person_a_has_pflegegrad-yes").should("not.be.checked");
      cy.get("#person_a_has_pflegegrad-no").should("be.checked");
    });

    it("Should set disability degree correctly", () => {
      cy.get("#person_a_disability_degree").should("have.value", 25);
    });

    it("Should set merkzeichen correctly", () => {
      cy.get("#person_a_has_merkzeichen_bl").should("be.checked");
      cy.get("#person_a_has_merkzeichen_tbl").should("be.checked");
      cy.get("#person_a_has_merkzeichen_h").should("not.be.checked");
      cy.get("#person_a_has_merkzeichen_g").should("be.checked");
      cy.get("#person_a_has_merkzeichen_ag").should("not.be.checked");
    });

    it("Should link back to person a has disability page", () => {
      cy.get("a").contains("Zurück").click();
      cy.url().should("include", "/lotse/step/has_disability_person_a");
    });

    it("Should link forward to telephone number page", () => {
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
        person_a_has_disability: "yes",

        person_a_has_pflegegrad: "no",
        person_a_disability_degree: 25,
        person_a_has_merkzeichen_bl: true,
      });
      cy.visit("/lotse/step/merkzeichen_person_a");
    });

    it("Should link back to person a has disability page", () => {
      cy.get("a").contains("Zurück").click();
      cy.url().should("include", "/lotse/step/has_disability_person_a");
    });

    it("Should link forward to person b page", () => {
      cy.get("button[type=submit]").click();
      cy.url().should("include", "/lotse/step/person_b");
    });
  });
});
