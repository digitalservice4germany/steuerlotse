describe("NoPauschbetragPage for person A", () => {
  beforeEach(() => {
    cy.login();
  });

  context("with no data", () => {
    beforeEach(() => {
      cy.visit("/lotse/step/person_a_no_pauschbetrag");
    });

    it("Should redirect to person a has disability page", () => {
      cy.url().should("include", "/lotse/step/has_disability_person_a");
    });
  });

  context("with person a has no disability data", () => {
    beforeEach(() => {
      cy.request("POST", "/testing/set_data/form_data", {
        person_a_has_disability: "no",
      });
      cy.visit("/lotse/step/person_a_no_pauschbetrag");
    });

    it("Should redirect to person a has disability page", () => {
      cy.url().should("include", "/lotse/step/has_disability_person_a");
    });
  });

  context("with person a has disability but no merkzeichen set", () => {
    beforeEach(() => {
      cy.request("POST", "/testing/set_data/form_data", {
        person_a_has_disability: "yes",
      });
      cy.visit("/lotse/step/person_a_no_pauschbetrag");
    });

    it("Should link back to merkzeichen page", () => {
      cy.get("a").contains("Zurück").click();
      cy.url().should("include", "/lotse/step/merkzeichen_person_a");
    });

    it("Should link forward to telephone number page", () => {
      cy.get("a").contains("Weiter").click();
      cy.url().should("include", "/lotse/step/telephone_number");
    });
  });

  context("with person a has pauschbetrag claim", () => {
    // There is no possible combination to only have a fahrtkostenpauschbetrag claim.
    beforeEach(() => {
      cy.request("POST", "/testing/set_data/form_data", {
        person_a_has_disability: "yes",
        person_a_has_pflegegrad: "no",
        person_a_disability_degree: 60,
      });
      cy.visit("/lotse/step/person_a_no_pauschbetrag");
    });

    it("Should redirect to person a merkzeichen page", () => {
      cy.url().should("include", "/lotse/step/merkzeichen_person_a");
    });
  });

  context(
    "with person a has pauschbetrag and fahrtkostenpauschbetrag claim",
    () => {
      beforeEach(() => {
        cy.request("POST", "/testing/set_data/form_data", {
          person_a_has_disability: "yes",
          person_a_has_pflegegrad: "no",
          person_a_disability_degree: 80,
          person_a_has_merkzeichen_g: true,
        });
        cy.visit("/lotse/step/person_a_no_pauschbetrag");
      });

      it("Should redirect to person a merkzeichen page", () => {
        cy.url().should("include", "/lotse/step/merkzeichen_person_a");
      });
    }
  );

  context(
    "with person a has no pauschbetrag or fahrtkostenpauschbetrag claim",
    () => {
      beforeEach(() => {
        cy.request("POST", "/testing/set_data/form_data", {
          person_a_has_disability: "yes",
          person_a_has_pflegegrad: "no",
        });
        cy.visit("/lotse/step/person_a_no_pauschbetrag");
      });

      it("Should not redirect", () => {
        cy.url().should("include", "/lotse/step/person_a_no_pauschbetrag");
      });

      it("Should link back to merkzeichen page", () => {
        cy.get("a").contains("Zurück").click();
        cy.url().should("include", "/lotse/step/merkzeichen_person_a");
      });

      it("Should link forward to telephone number page", () => {
        cy.get("a").contains("Weiter").click();
        cy.url().should("include", "/lotse/step/telephone_number");
      });

      context("With joint taxes", () => {
        beforeEach(() => {
          cy.request("POST", "/testing/set_data/form_data", {
            familienstand: "married",
            familienstand_date: "02.09.2000",
            familienstand_married_lived_separated: "no",
            familienstand_confirm_zusammenveranlagung: true,
            person_a_has_disability: "yes",
            person_a_has_pflegegrad: "no",
          });
          cy.visit("/lotse/step/person_a_no_pauschbetrag");
        });

        it("Should link forward to person b page", () => {
          cy.get("a").contains("Weiter").click();
          cy.url().should("include", "/lotse/step/person_b");
        });
      });
    }
  );
});
