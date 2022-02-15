describe("Revocation Success", () => {
  beforeEach(() => {
    cy.visit("/unlock_code_revocation/step/unlock_code_success");
    cy.extended_footer_is_disabled(false);
  });

  it("links back to revocation input page", () => {
    cy.get("a").contains("Zurück").click();

    cy.url().should("include", "/unlock_code_revocation/step/data_input");
  });

  it("links forward to registration input page", () => {
    cy.get("a").contains("Weiter").click();

    cy.url().should("include", "/unlock_code_request/step/data_input");
  });
});
