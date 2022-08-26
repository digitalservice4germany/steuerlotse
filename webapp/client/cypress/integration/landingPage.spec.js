describe("Landing page", () => {
  it("Clicking 1st box", () => {
    cy.visit("/");
    // Clicking 1st box
    cy.get("h2").contains("Ich bin neu hier").parent().click();

    // Should redirect to retirement page
    cy.url().should("include", "/neuhier");
  });

  it("Clicking 2nd box", () => {
    cy.visit("/");
    // Clicking 1st box
    cy.get("h2")
      .contains("Ich habe bereits einen Freischaltcode")
      .parent()
      .click();

    // Should redirect to retirement page
    cy.url().should("include", "/unlock_code_activation/step/data_input");
  });

  it("eligibility process should be disabled", () => {
    cy.get("span")
      .contains(/^Nutzung prüfen$/)
      .should("have.class", "inactive");
  });

  it("registration should be disabled", () => {
    cy.get("span")
      .contains(/^Registrieren$/)
      .should("have.class", "inactive");
  });
});
