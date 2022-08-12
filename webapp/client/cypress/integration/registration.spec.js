describe("Registration", () => {
  it("registration is disabled", () => {
    cy.visit("/unlock_code_request/step/data_input");
    cy.url().should("eq", Cypress.config().baseUrl + "/");
  });
});
