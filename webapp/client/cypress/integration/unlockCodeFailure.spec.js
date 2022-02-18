describe("Unlock Code Failure", () => {
  beforeEach(() => {
    cy.visit("unlock_code_request/step/unlock_code_failure");
  });

  it("links back to registration page", () => {
    cy.get("a").contains("Zurück").click();

    cy.url().should("include", "unlock_code_request/step/data_input");
  });

  it("has no forward link", () => {
    cy.get("a").contains("Weiter").should("not.exist");
  });
});
