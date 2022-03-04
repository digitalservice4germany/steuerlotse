describe("Filing", () => {
  beforeEach(() => {
    cy.login();
  });

  context("success", () => {
    beforeEach(() => {
      cy.fixture("est_data").then((est_data) => {
        cy.request("POST", "/testing/set_session_data/form_data", est_data);
      });
      cy.visit("/lotse/step/filing");
    });

    it("downloading pdf is possible", () => {
      cy.window()
        .document()
        .then(function (doc) {
          doc.addEventListener("click", () => {
            setTimeout(function () {
              doc.location.reload();
            }, 1000);
          });
          // Downloads folder is automatically cleared
          cy.get("a").contains("Übersicht speichern").click();
          cy.readFile("cypress/downloads/AngabenSteuererklaerung.pdf").should(
            "exist"
          );
        });
    });

    it("going to next step is possible", () => {
      cy.get("a").contains("Weiter").click();
      cy.url().should("include", "/lotse/step/ack");
    });
  });

  context("failure", () => {
    beforeEach(() => {
      cy.fixture("est_data").then((est_data) => {
        est_data["produce_validation_error"] = true;
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
