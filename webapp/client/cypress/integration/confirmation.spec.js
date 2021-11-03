describe("Confirmation", () => {
  beforeEach(() => {
    cy.login();
    cy.visit("/lotse/step/confirmation");
  });

  it("submitting an empty form", () => {
    // Submit empty form
    cy.get("button[type=submit]").contains("Steuererklärung abgeben").click();

    // Should have errors in the right places.
    cy.get("[role=alert][for=confirm_data_privacy]").contains(
      "Sie müssen dieses Feld auswählen, um weiter zu machen"
    );
    cy.get("[role=alert][for=confirm_terms_of_service]").contains(
      "Sie müssen dieses Feld auswählen, um weiter zu machen"
    );
  });

  it("submitting a complete form with missing data", () => {
    // Check boxes
    cy.get("label[for=confirm_data_privacy].checkmark").click();
    cy.get("label[for=confirm_terms_of_service].checkmark").click();

    // Submit
    cy.get("button[type=submit]").contains("Steuererklärung abgeben").click();

    // Should be redirected to summary page because fields before not filled correctly
    cy.url().should("include", "/lotse/step/summary");
  });
});
