describe("Logout", () => {
  beforeEach(() => {
    cy.login();
    cy.visit("logout");
  });

  it("has no back link", () => {
    cy.get("a").contains("Zurück").should("not.exist");
  });

  it("logout to login page", () => {
    cy.get("button[type=submit]").contains("Abmelden").click();

    cy.url().should("include", "unlock_code_activation/step/data_input");

    cy.get("div[class*=alert-success]").contains(
      "Sie haben sich erfolgreich abgemeldet."
    );
  });
});
