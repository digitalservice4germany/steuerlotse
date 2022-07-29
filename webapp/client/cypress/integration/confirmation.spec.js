describe("Confirmation", () => {
  beforeEach(() => {
    cy.login();
    cy.visit("/lotse/step/confirmation");
  });

  const loadingSpinnerSelector = '[name="loading_spinner"]';

  context("submitting an empty form", () => {
    beforeEach(() => {
      cy.get(loadingSpinnerSelector).should("not.exist");
      cy.get("button[type=submit]").contains("Steuererklärung abgeben").click();
      cy.get(loadingSpinnerSelector).should("be.visible");
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

      cy.get(loadingSpinnerSelector).should("not.exist");
      cy.get("button[type=submit]").contains("Steuererklärung abgeben").click();
      cy.get(loadingSpinnerSelector).should("be.visible");
    });

    it("should be redirected to summary page", () => {
      cy.url().should("include", "/lotse/step/summary");
    });
  });
});
