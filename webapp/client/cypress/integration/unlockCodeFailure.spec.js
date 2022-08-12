describe("Unlock Code Failure", () => {
  it("registration is disabled", () => {
    cy.visit("unlock_code_request/step/unlock_code_failure");
    cy.url().should("eq", Cypress.config().baseUrl + "/");
  });
});
