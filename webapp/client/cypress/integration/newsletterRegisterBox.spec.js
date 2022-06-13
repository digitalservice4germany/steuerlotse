describe("NewsletterRegisterBox", () => {
  beforeEach(() => {
    cy.visit("/unlock_code_request/step/unlock_code_success");
  });

  it("Should link to data privacy page", () => {
    cy.get("a").contains("Datenschutzerklärung").click();
    cy.url().should("include", "/datenschutz");
  });

  it("Should display error email empty", () => {
    cy.get("button").contains("E-Mails abonnieren").click();
    // we should have visible errors now
    cy.get(".invalid-feedback").should(
      "contain",
      " Dieses Feld darf nicht leer sein."
    );

    // and still be on the same URL
    cy.url().should("include", "/unlock_code_request/step/unlock_code_success");
  });

  it("Should display success message", () => {
    cy.get("input[id=email]").type("test@test.de");
    cy.get("button").contains("E-Mails abonnieren").click();

    // we should see success message
    cy.get("div[id=success]").should("exist");

    // and still be on the same URL
    cy.url().should("include", "/unlock_code_request/step/unlock_code_success");
  });
});
