describe("Filing", () => {
  beforeEach(() => {
    cy.login();
  });

  context("success", () => {
    beforeEach(() => {
      cy.fixture("est_sample_data_single_user").then((est_data) => {
        cy.request("POST", "/testing/set_session_data/form_data", est_data);
      });
      cy.visit("/lotse/step/filing");
    });

    it("downloading pdf is possible", () => {
      cy.get("a")
        .contains("Übersicht speichern")
        .should("have.attr", "href")
        .and("include", "download_pdf/print.pdf")
        .then((href) => {
          cy.request(href).its("body").should("not.be.empty");
        });
    });

    it("going to next step is possible", () => {
      cy.get("a").contains("Weiter").click();
      cy.url().should("include", "/lotse/step/ack");
    });
  });

  context("failure", () => {
    beforeEach(() => {
      cy.fixture("est_sample_data_single_user").then((est_data) => {
        est_data["person_a_dob"] = "2052-12-01";
        cy.request("POST", "/testing/set_session_data/form_data", est_data);
      });
      cy.visit("/lotse/step/filing");
    });

    it("validation problem is rendered", () => {
      cy.get("p[class*=result-text]").should("exist");
    });

    it("mailto within text is rendered", () => {
      cy.get("a")
        .contains("kontakt@steuerlotse-rente.de")
        .should("have.attr", "href")
        .and("include", "mailto:kontakt@steuerlotse-rente.de");
    });

    it("text us button is rendered", () => {
      cy.get("a")
        .contains("Schreiben Sie uns")
        .should("have.attr", "href")
        .and("include", "mailto:kontakt@steuerlotse-rente.de");
    });
  });
});
