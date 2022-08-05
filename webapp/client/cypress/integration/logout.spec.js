describe("Logout", () => {
  beforeEach(() => {
    cy.login();
  });

  it("has no back link", () => {
    cy.visit("logout");
    cy.get("a").contains("Zurück").should("not.exist");
  });

  it("logout to login page", () => {
    cy.visit("logout");
    cy.get("button[type=submit]").contains("Abmelden").click();

    cy.url().should("include", "unlock_code_activation/step/data_input");

    cy.get("div[class*=alert-success]").contains(
      "Sie haben sich erfolgreich abgemeldet."
    );
  });

  const loadingSpinnerSelector = '[name="loading_spinner"]';
  const submitBtnSelector = '[name="next_button"]';

  it("logout to start page because of completed tax return", () => {
    cy.fixture("est_sample_data_single_user").then((est_data) => {
      cy.request("POST", "/testing/set_session_data/form_data", est_data);
    });

    cy.visit("/lotse/step/confirmation");

    cy.get(loadingSpinnerSelector).should("not.exist");
    cy.get(submitBtnSelector).contains("Steuererklärung abgeben").click();
    cy.get(loadingSpinnerSelector).should("be.visible");

    cy.url().should("include", "/lotse/step/filing");

    cy.visit("logout");

    cy.url().should("not.contain", "logout");

    cy.get("div[class*=alert-success]").contains(
      "Sie haben sich erfolgreich abgemeldet."
    );
  });
});
