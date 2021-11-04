describe("DeclarationIncomes", () => {
  beforeEach(() => {
    cy.login();
    cy.visit("/lotse/step/decl_incomes");
  });

  it("submitting an empty form", () => {
    // Submit empty form
    cy.get("button[type=submit]").click();

    // Should have error in the right place.
    cy.get("[role=alert][for=declaration_incomes]").contains(
      "Sie müssen dieses Feld auswählen, um weiter zu machen"
    );
  });

  it("submitting a complete and correct form", () => {
    // Check box
    cy.get("label[for=declaration_incomes].checkmark").click();

    // Submit
    cy.get("button[type=submit]").click();

    // Should be on correct next page
    cy.url().should("include", "/lotse/step/decl_edaten");
  });
});
