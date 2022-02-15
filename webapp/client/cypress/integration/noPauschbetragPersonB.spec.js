describe("NoPauschbetragPage for person B", () => {
  beforeEach(() => {
    cy.login();
  });

  context("with no data", () => {
    beforeEach(() => {
      cy.visit("/lotse/step/person_b_no_pauschbetrag");
      cy.extended_footer_is_disabled(true);
    });

    it("Should redirect to familienstand page", () => {
      cy.url().should("include", "/lotse/step/familienstand");
    });
  });

  context("With joint taxes", () => {
    beforeEach(() => {
      cy.request("POST", "/testing/set_session_data/form_data", {
        familienstand: "married",
        familienstand_date: "02.09.2000",
        familienstand_married_lived_separated: "no",
        familienstand_confirm_zusammenveranlagung: true,
      });
      cy.visit("/lotse/step/person_b_no_pauschbetrag");
      cy.extended_footer_is_disabled(true);
    });

    it("Should redirect to person b has disability page", () => {
      cy.url().should("include", "/lotse/step/has_disability_person_b");
    });
  });

  context("with joint taxes and person b has no disability data", () => {
    beforeEach(() => {
      cy.request("POST", "/testing/set_session_data/form_data", {
        familienstand: "married",
        familienstand_date: "02.09.2000",
        familienstand_married_lived_separated: "no",
        familienstand_confirm_zusammenveranlagung: true,
        person_b_has_disability: "no",
      });
      cy.visit("/lotse/step/person_b_no_pauschbetrag");
      cy.extended_footer_is_disabled(true);
    });

    it("Should redirect to person b has disability page", () => {
      cy.url().should("include", "/lotse/step/has_disability_person_b");
    });
  });

  context(
    "with joint taxes and person b has disability but no merkzeichen set",
    () => {
      beforeEach(() => {
        cy.request("POST", "/testing/set_session_data/form_data", {
          familienstand: "married",
          familienstand_date: "02.09.2000",
          familienstand_married_lived_separated: "no",
          familienstand_confirm_zusammenveranlagung: true,
          person_b_has_disability: "yes",
          person_b_disability_degree: 60,
        });
        cy.visit("/lotse/step/person_b_no_pauschbetrag");
        cy.extended_footer_is_disabled(true);
      });

      it("Should redirect to person b merkzeichen page", () => {
        cy.url().should("include", "/lotse/step/merkzeichen_person_b");
      });
    }
  );

  context("with joint taxes and person b has pauschbetrag claim", () => {
    // There is no possible combination to only have a fahrtkostenpauschbetrag claim.
    beforeEach(() => {
      cy.request("POST", "/testing/set_session_data/form_data", {
        familienstand: "married",
        familienstand_date: "02.09.2000",
        familienstand_married_lived_separated: "no",
        familienstand_confirm_zusammenveranlagung: true,
        person_b_has_disability: "yes",
        person_b_has_pflegegrad: "no",
        person_b_disability_degree: 60,
      });
      cy.visit("/lotse/step/person_b_no_pauschbetrag");
      cy.extended_footer_is_disabled(true);
    });

    it("Should redirect to person b merkzeichen page", () => {
      cy.url().should("include", "/lotse/step/merkzeichen_person_b");
    });
  });

  context(
    "with joint taxes and person b has pauschbetrag and fahrtkostenpauschbetrag claim",
    () => {
      beforeEach(() => {
        cy.request("POST", "/testing/set_session_data/form_data", {
          familienstand: "married",
          familienstand_date: "02.09.2000",
          familienstand_married_lived_separated: "no",
          familienstand_confirm_zusammenveranlagung: true,
          person_b_has_disability: "yes",
          person_b_has_pflegegrad: "no",
          person_b_disability_degree: 80,
        });
        cy.visit("/lotse/step/person_b_no_pauschbetrag");
        cy.extended_footer_is_disabled(true);
      });

      it("Should redirect to person b merkzeichen page", () => {
        cy.url().should("include", "/lotse/step/merkzeichen_person_b");
      });
    }
  );

  context(
    "with joint taxes and person b has no pauschbetrag or fahrtkostenpauschale claim",
    () => {
      beforeEach(() => {
        cy.request("POST", "/testing/set_session_data/form_data", {
          familienstand: "married",
          familienstand_date: "02.09.2000",
          familienstand_married_lived_separated: "no",
          familienstand_confirm_zusammenveranlagung: true,
          person_b_has_disability: "yes",
          person_b_requests_pauschbetrag: "yes",
          person_b_has_pflegegrad: "no",
        });
        cy.visit("/lotse/step/person_b_no_pauschbetrag");
        cy.extended_footer_is_disabled(true);
      });

      it("Should not redirect", () => {
        cy.url().should("include", "/lotse/step/person_b_no_pauschbetrag");
      });

      it("Should link back to merkzeichen page", () => {
        cy.get("a").contains("Zurück").click();
        cy.url().should("include", "/lotse/step/merkzeichen_person_b");
      });

      it("Should link forward to telephone number page", () => {
        cy.get("a").contains("Weiter").click();
        cy.url().should("include", "/lotse/step/telephone_number");
      });
    }
  );
});
