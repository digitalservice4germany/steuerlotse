describe("NewsletterRegisterBox", () => {
  beforeEach(() => {
    cy.visit("/unlock_code_request/step/unlock_code_success");
  });

  it("Should link to data privacy page", () => {
    cy.get("a").contains("Datenschutzerklärung").click();
    cy.url().should("include", "/datenschutz");
  });

  it("Should display error email empty", () => {
    cy.get("button").contains("E-Mails abbonieren").click();
    // we should have visible errors now
    cy.get(".invalid-feedback").should(
      "contain",
      " Dieses Feld darf nicht leer sein."
    );

    // and still be on the same URL
    cy.url().should("include", "/unlock_code_request/step/unlock_code_success");
  });
});
