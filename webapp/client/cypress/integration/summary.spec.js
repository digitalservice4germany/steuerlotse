describe("Summary", () => {
  context("when no fields filled", () => {
    beforeEach(() => {
      cy.login();
    });

    it("shows alert message for page", () => {
      cy.visit("/lotse/step/summary");
      cy.get("div.alert[role=alert]").should("have.length", 2);
    });
  });

  context("when submitting with unfilled field", () => {
    beforeEach(() => {
      cy.login();
      cy.visit("/lotse/step/summary");
    });

    it("redirects to same page", () => {
      cy.get("[name=next_button]").click();
      cy.location().should((loc) => {
        expect(loc.pathname.toString()).to.contain("/lotse/step/summary");
      });
    });

    it("shows alert message for field", () => {
      cy.get("[name=next_button]").click();
      cy.get("div.invalid-feedback[role=alert]").should("have.length", 1);
    });

    it("does not show alert message for page", () => {
      cy.get("[name=next_button]").click();
      cy.get("div.alert[role=alert]").should("not.exist");
    });
  });

  context("when submitting with filled field", () => {
    beforeEach(() => {
      cy.login();
      cy.visit("/lotse/step/summary");
      cy.get("label[for=confirm_complete_correct]").first().click();
    });

    it("redirects to same page", () => {
      cy.get("[name=next_button]").click();
      cy.location().should((loc) => {
        expect(loc.pathname.toString()).to.contain("/lotse/step/summary");
      });
    });

    /* REVERT THIS! */

    /* it("does not show alert message for field", () => {
      cy.get("[name=next_button]").click();
      cy.get("div.invalid-feedback[role=alert]").should("not.exist");
    }); */

    it("shows alert message for page once", () => {
      cy.get("[name=next_button]").click();
      cy.get("div.alert[role=alert]").should("have.length", 2);
    });
  });
});
