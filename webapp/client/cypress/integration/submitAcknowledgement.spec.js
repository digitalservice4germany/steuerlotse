describe("StepAck", () => {
  context("common", () => {
    beforeEach(() => {
      cy.login();
    });

    it("links back to filing page", () => {
      cy.fixture("est_sample_data_single_user").then((est_data) => {
        cy.request("POST", "/testing/set_session_data/form_data", est_data);
      });
      cy.visit("/lotse/step/ack");
      cy.get("a").contains("Zurück").click();
      cy.url().should("include", "/lotse/step/filing");
    });

    it("logout to login page", () => {
      cy.visit("/lotse/step/ack");
      cy.get("a").contains("Abmelden").click();

      cy.url().should("eq", Cypress.config().baseUrl + "/");

      cy.get("div[class*=alert-success]").contains(
        "Sie haben sich erfolgreich abgemeldet."
      );
    });
  });
});
