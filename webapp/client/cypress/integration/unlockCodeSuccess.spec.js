describe("Unlock Code Success", () => {
  it("registration is disabled", () => {
    cy.visit("unlock_code_request/step/unlock_code_success");
    cy.url().should("eq", Cypress.config().baseUrl + "/");
  });
});
