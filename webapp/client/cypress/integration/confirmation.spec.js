describe("Confirmation", () => {
  beforeEach(() => {
    cy.login();
    cy.visit("/lotse/step/confirmation");
  });

  context("submitting an empty form", () => {
    beforeEach(() => {
      cy.get("button[type=submit]").contains("Steuererklärung abgeben").click();
    });

    it("should have errors in the right places.", () => {
      cy.get("[role=alert][for=confirm_data_privacy]").contains(
        "Bestätigen Sie, dass Sie mit den Datenschutzrichtlinien einverstanden sind, um fortfahren zu können."
      );
      cy.get("[role=alert][for=confirm_terms_of_service]").contains(
        "Bestätigen Sie, dass Sie den Nutzungbedingungen zustimmen, um fortfahren zu können."
      );
    });
  });

  context("submitting a complete form with missing data", () => {
    beforeEach(() => {
      cy.get("label[for=confirm_data_privacy].checkmark").click();
      cy.get("label[for=confirm_terms_of_service].checkmark").click();

      cy.get("button[type=submit]").contains("Steuererklärung abgeben").click();
    });

    it("should be redirected to summary page", () => {
      cy.url().should("include", "/lotse/step/summary");
    });
  });

  it("submitting a complete form with full data", () => {
    // TODO implement this once route to set data for functional tests is implemented
  });
});
