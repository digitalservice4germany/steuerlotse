describe("Revocation", () => {
  context("Simple form input", () => {
    beforeEach(() => {
      cy.visit("/unlock_code_revocation/step/data_input");
      cy.fixture("user").as("user");
    });

    it("should show an error for invalid tax ID", function () {
      // incorrect username on purpose
      cy.get("input[id=idnr_1]").clear().type("12");
      cy.get("input[id=idnr_2]").clear().type("345");
      cy.get("input[id=idnr_3]").clear().type("678");
      cy.get("input[id=idnr_4]").clear().type("901");
      cy.get("input[id=dob_1]").clear().type(this.user.dob.day);
      cy.get("input[id=dob_2]").clear().type(this.user.dob.month);
      cy.get("input[id=dob_3]")
        .clear()
        .type(this.user.dob.year + "{enter}");

      // we should have visible errors now
      cy.get(".invalid-feedback").should(
        "contain",
        "Keine korrekte Steuer-Identifikationsnummer. Prüfen Sie Ihre Angabe."
      );

      // and still be on the same URL
      cy.url().should("include", "/unlock_code_revocation/step/data_input");
    });

    it("should show an error for invalid date of birth", function () {
      // incorrect username on purpose
      cy.get("input[id=idnr_1]").clear().type(this.user.idnr[0]);
      cy.get("input[id=idnr_2]").clear().type(this.user.idnr[1]);
      cy.get("input[id=idnr_3]").clear().type(this.user.idnr[2]);
      cy.get("input[id=idnr_4]").clear().type(this.user.idnr[3]);
      cy.get("input[id=dob_1]").clear().type("40");
      cy.get("input[id=dob_2]").clear().type("11");
      cy.get("input[id=dob_3]")
        .clear()
        .type("1965" + "{enter}");

      // we should have visible errors now
      cy.get(".invalid-feedback").should(
        "contain",
        "Das ist kein korrektes Datum. Prüfen Sie Ihre Angabe."
      );

      // and still be on the same URL
      cy.url().should("include", "/unlock_code_revocation/step/data_input");
    });
  });

  context("with registered tax ID", () => {
    let idnr = ["09", "953", "674", "813"];
    let dob = {
      day: "1",
      month: "2",
      year: "1951",
    };

    beforeEach(() => {
      cy.register(idnr, dob);
      cy.visit("/unlock_code_revocation/step/data_input");
    });

    it("should redirect to success page", function () {
      cy.get("input[id=idnr_1]").clear().type(idnr[0]);
      cy.get("input[id=idnr_2]").clear().type(idnr[1]);
      cy.get("input[id=idnr_3]").clear().type(idnr[2]);
      cy.get("input[id=idnr_4]").clear().type(idnr[3]);
      cy.get("input[id=dob_1]").clear().type(dob.day);
      cy.get("input[id=dob_2]").clear().type(dob.month);
      cy.get("input[id=dob_3]")
        .clear()
        .type(dob.year + "{enter}");

      // we should be redirected
      cy.url().should(
        "include",
        "/unlock_code_revocation/step/unlock_code_success"
      );

      // and our cookie should be set
      cy.getCookie("session").should("exist");
    });
  });

  context("with unregistered tax ID", () => {
    let idnr = ["08", "842", "569", "173"];
    let dob = {
      day: "1",
      month: "2",
      year: "1951",
    };

    beforeEach(() => {
      cy.visit("/unlock_code_revocation/step/data_input");
    });

    it("should redirect to failure page", function () {
      cy.get("input[id=idnr_1]").clear().type(idnr[0]);
      cy.get("input[id=idnr_2]").clear().type(idnr[1]);
      cy.get("input[id=idnr_3]").clear().type(idnr[2]);
      cy.get("input[id=idnr_4]").clear().type(idnr[3]);
      cy.get("input[id=dob_1]").clear().type(dob.day);
      cy.get("input[id=dob_2]").clear().type(dob.month);
      cy.get("input[id=dob_3]")
        .clear()
        .type(dob.year + "{enter}");

      // we should be redirected
      cy.url().should(
        "include",
        "/unlock_code_revocation/step/unlock_code_failure"
      );

      // and our cookie should be set
      cy.getCookie("session").should("exist");
    });
  });
});
