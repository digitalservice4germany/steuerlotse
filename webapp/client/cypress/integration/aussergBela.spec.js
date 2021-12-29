describe("PersonAHasDisability", () => {
  beforeEach(() => {
    cy.login();
  });

  context("with no data", () => {
    beforeEach(() => {
      cy.visit("/lotse/step/ausserg_bela");
    });

    it("Should redirect back to select_stmind page", () => {
      cy.location().should((loc) => {
        expect(loc.pathname.toString()).to.contain("/lotse/step/select_stmind");
      });
      cy.get("div[role=alert]").should("exist");
    });
  });

  context("with aussergBela selected but no disability data", () => {
    beforeEach(() => {
      cy.request("POST", "/testing/set_data/form_data", {
        stmind_select_ausserg_bela: true,
      });

      cy.visit("/lotse/step/ausserg_bela");
    });

    it("Should show standard Aufwendungs inputs", () => {
      cy.get("#stmind_krankheitskosten_summe").should("exist");
      cy.get("#stmind_krankheitskosten_anspruch").should("exist");

      cy.get("#stmind_pflegekosten_summe").should("exist");
      cy.get("#stmind_pflegekosten_anspruch").should("exist");

      cy.get("#stmind_bestattung_summe").should("exist");
      cy.get("#stmind_bestattung_anspruch").should("exist");

      cy.get("#stmind_aussergbela_sonst_summe").should("exist");
      cy.get("#stmind_aussergbela_sonst_anspruch").should("exist");

      cy.get("#stmind_krankheitskosten_summe").should("exist");
      cy.get("#stmind_krankheitskosten_anspruch").should("exist");
    });

    it("Should not show Behinderungsbedingte Aufwendungen inputs", () => {
      cy.get("#stmind_beh_aufw_summe").should("not.exist");
      cy.get("#stmind_beh_aufw_anspruch").should("not.exist");
    });

    it("Should link back to select_stmind page", () => {
      cy.get("a").contains("Zurück").click();
      cy.url().should("include", "/lotse/step/select_stmind");
    });

    it("Should link forward to summary page", () => {
      cy.get("button[type=submit]").click();
      cy.url().should("include", "/lotse/step/summary");
    });
  });

  context(
    "with aussergBela selected but person a and b have no disability",
    () => {
      beforeEach(() => {
        cy.request("POST", "/testing/set_data/form_data", {
          stmind_select_ausserg_bela: true,
          person_a_has_disability: "no",
          person_b_has_disability: "no",
        });

        cy.visit("/lotse/step/ausserg_bela");
      });

      it("Should not show Behinderungsbedingte Aufwendungen inputs", () => {
        cy.get("#stmind_beh_aufw_summe").should("not.exist");
        cy.get("#stmind_beh_aufw_anspruch").should("not.exist");
      });
    }
  );

  context("with aussergBela selected and person a has disability", () => {
    beforeEach(() => {
      cy.request("POST", "/testing/set_data/form_data", {
        stmind_select_ausserg_bela: true,
        person_a_has_disability: "yes",
      });

      cy.visit("/lotse/step/ausserg_bela");
    });

    it("Should show Behinderungsbedingte Aufwendungen Summe input", () => {
      cy.get("#stmind_beh_aufw_summe").should("exist");
      cy.get("#stmind_beh_aufw_anspruch").should("exist");
    });
  });

  context("with aussergBela selected and person b has disability", () => {
    beforeEach(() => {
      cy.request("POST", "/testing/set_data/form_data", {
        familienstand: "married",
        familienstand_married_lived_separated: "no",
        familienstand_confirm_zusammenveranlagung: true,
        person_a_has_disability: "yes",

        stmind_select_ausserg_bela: true,
        person_a_has_disability: "no",
        person_b_has_disability: "yes",
      });

      cy.visit("/lotse/step/ausserg_bela");
    });

    it("Should show Behinderungsbedingte Aufwendungen inputs", () => {
      cy.get("#stmind_beh_aufw_summe").should("exist");
      cy.get("#stmind_beh_aufw_anspruch").should("exist");
    });
  });
});
