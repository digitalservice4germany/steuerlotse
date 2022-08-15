describe("Revocation Success", () => {
  beforeEach(() => {
    cy.visit("/unlock_code_revocation/step/unlock_code_success");
  });

  it("links back to revocation input page", () => {
    cy.get("a").contains("Zurück").click();

    cy.url().should("include", "/unlock_code_revocation/step/data_input");
  });

  it("links forward to start page", () => {
    cy.get("a").contains("Weiter").click();

    cy.url().should("eq", Cypress.config().baseUrl + "/");
  });
});
