describe("Login", () => {
  context("logging In", () => {
    beforeEach(() => {
      cy.visit("/unlock_code_activation/step/data_input");
      cy.fixture("user").as("user");
    });

    it("should redirect on success", function () {
      cy.get("input[id=idnr_1]").type(this.user.idnr[0]);
      cy.get("input[id=idnr_2]").type(this.user.idnr[1]);
      cy.get("input[id=idnr_3]").type(this.user.idnr[2]);
      cy.get("input[id=idnr_4]").type(this.user.idnr[3]);
      cy.get("input[id=unlock_code_1]").type(this.user.unlockCode[0]);
      cy.get("input[id=unlock_code_2]").type(this.user.unlockCode[1]);
      cy.get("input[id=unlock_code_3]").type(
        this.user.unlockCode[2] + "{enter}"
      );

      // we should be redirected
      cy.url().should("include", "/lotse/step/decl_incomes");

      // and our cookie should be set
      cy.getCookie("session").should("exist");
    });

    it("should show an error for invalid tax IDs", function () {
      // incorrect username on purpose
      cy.get("input[id=idnr_1]").type("12");
      cy.get("input[id=idnr_2]").type("345");
      cy.get("input[id=idnr_3]").type("678");
      cy.get("input[id=idnr_4]").type("901");
      cy.get("input[id=unlock_code_1]").type(this.user.unlockCode[0]);
      cy.get("input[id=unlock_code_2]").type(this.user.unlockCode[1]);
      cy.get("input[id=unlock_code_3]").type(
        this.user.unlockCode[2] + "{enter}"
      );

      // we should have visible errors now
      cy.get(".invalid-feedback").should(
        "contain",
        "Geben Sie bitte eine gültige Steuer-Identifikationsnummer an."
      );

      // and still be on the same URL
      cy.url().should("include", "/unlock_code_activation/step/data_input");
    });
  });

  context("when logged in", () => {
    beforeEach(() => {
      cy.login();
      cy.visit("/lotse/step/start");
    });

    it("registration should be disabled", () => {
      cy.get("span")
        .contains(/^Registrieren$/)
        .should("have.class", "inactive");
    });

    it("unlock code revocation should be disabled", () => {
      cy.get("span")
        .contains(/^Freischaltcode Stornierung$/)
        .should("have.class", "inactive");
    });
  });
});
