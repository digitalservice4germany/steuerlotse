describe("merkzeichenPersonB", () => {
  beforeEach(() => {
    cy.login();
  });

  context("with no disability data", () => {
    beforeEach(() => {
      cy.request("POST", "/testing/set_data/form_data", {
        familienstand: "married",
        familienstand_married_lived_separated: "no",
        familienstand_confirm_zusammenveranlagung: true,
      });
      cy.visit("/lotse/step/merkzeichen_person_b");
    });

    it("Should redirect to person b has disability page", () => {
      cy.location().should((loc) => {
        expect(loc.pathname.toString()).to.contain(
          "/lotse/step/has_disability_person_b"
        );
      });
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
      cy.visit("/lotse/step/merkzeichen_person_b");
    });

    it("Should redirect to person b has disability page", () => {
      cy.location().should((loc) => {
        expect(loc.pathname.toString()).to.contain(
          "/lotse/step/has_disability_person_b"
        );
      });
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
      cy.visit("/lotse/step/merkzeichen_person_b");
    });

    it("Should stay on page and show error when submit button clicked", () => {
      cy.get("button[type=submit]").click();
      cy.url().should("include", "/lotse/step/merkzeichen_person_b");
      cy.get("[role=alert][for=person_b_has_pflegegrad]").contains(
        "Diese Angabe wird benötigt, um fortfahren zu können"
      );
    });
  });

  context("with person b disability data set", () => {
    beforeEach(() => {
      cy.request("POST", "/testing/set_data/form_data", {
        person_b_has_disability: "yes",

        person_b_has_pflegegrad: "no",
        person_b_disability_degree: 25,
        person_b_has_merkzeichen_bl: true,
        person_b_has_merkzeichen_tbl: true,
        person_b_has_merkzeichen_h: false,
        person_b_has_merkzeichen_g: true,
        person_b_has_merkzeichen_ag: false,
      });

      cy.visit("/lotse/step/merkzeichen_person_b");
    });

    it("Should set pflegegrad correctly", () => {
      cy.get("#person_b_has_pflegegrad-yes").should("not.be.checked");
      cy.get("#person_b_has_pflegegrad-no").should("be.checked");
    });

    it("Should set disability degree correctly", () => {
      cy.get("#person_b_disability_degree").should("have.value", 25);
    });

    it("Should set merkzeichen correctly", () => {
      cy.get("#person_b_has_merkzeichen_bl").should("be.checked");
      cy.get("#person_b_has_merkzeichen_tbl").should("be.checked");
      cy.get("#person_b_has_merkzeichen_h").should("not.be.checked");
      cy.get("#person_b_has_merkzeichen_g").should("be.checked");
      cy.get("#person_b_has_merkzeichen_ag").should("not.be.checked");
    });

    it("Should link back to person b has disability page", () => {
      cy.get("a").contains("Zurück").click();
      cy.url().should("include", "/lotse/step/has_disability_person_a");
    });

    it("Should link forward to telephone number page", () => {
      cy.get("button[type=submit]").click();
      cy.url().should("include", "/lotse/step/telephone_number");
    });
  });
});
