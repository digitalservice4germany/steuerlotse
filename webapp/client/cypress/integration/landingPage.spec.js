describe("Landing page", () => {
  it("Clicking button to eligibility check", () => {
    cy.visit("/");
    // Clicking button
    cy.get("a").contains("Jetzt prüfen").click();

    // Should redirect to first step of eligibility steps
    cy.url().should("include", "/eligibility/step/tax_year");
  });
});
