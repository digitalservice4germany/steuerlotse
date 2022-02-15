describe("Login Failure", () => {
  beforeEach(() => {
    cy.visit("/unlock_code_activation/step/unlock_code_failure");
    cy.extended_footer_is_disabled(false);
  });

  it("links back to login input page", () => {
    cy.get("a").contains("Zurück").click();

    cy.url().should("include", "/unlock_code_activation/step/data_input");
  });

  it("has no forward link", () => {
    cy.get("a").contains("Weiter").should("not.exist");
  });
});
