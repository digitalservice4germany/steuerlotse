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

    /*     it("success alert message is displayed", () => {
      cy.visit("/lotse/step/ack");
      cy.get("div[class*=alert-success]").contains(
        "Herzlichen Glückwunsch! Sie sind mit Ihrer Steuererklärung fertig!"
      );
    }); */

    it("logout to login page", () => {
      cy.visit("/lotse/step/ack");
      cy.get("a").contains("Abmelden").click();

      cy.url().should("eq", Cypress.config().baseUrl + "/");

      cy.get("div[class*=alert-success]").contains(
        "Sie haben sich erfolgreich abgemeldet."
      );
    });
  });

  context("desktop buttons", () => {
    beforeEach(() => {
      cy.login();
      cy.visit("/lotse/step/ack");
    });
    it("posting to facebook is possible", () => {
      cy.contains("Auf Facebook teilen")
        .closest("a")
        .should("have.attr", "href")
        .and("include", "facebook");
    });

    it("posting to facebook in new tab possible", () => {
      // https://docs.cypress.io/guides/references/trade-offs#Multiple-tabs
      cy.contains("Auf Facebook teilen")
        .closest("a")
        .should("have.attr", "target", "_blank");
    });

    it("posting to email is possible", () => {
      cy.contains("E-Mail schreiben")
        .closest("a")
        .should("have.attr", "href")
        .and("include", "mailto");
    });

    it("whatsapp button does not exist", () => {
      cy.get(".whatsapp").should("not.exist");
    });
  });

  context("mobile buttons", () => {
    beforeEach(() => {
      cy.viewport(390, 844); // iphone 12 Pro, just visualization
      cy.login();
      cy.visit("/lotse/step/ack", {
        onBeforeLoad: (win) => {
          Object.defineProperty(win.navigator, "userAgent", {
            // this is needed for isMobile to work in the test
            value:
              "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1",
          });
        },
      });
    });

    it("posting to whatsapp is possible", () => {
      cy.contains("In Whatsapp senden")
        .closest("a")
        .should("have.attr", "href")
        .and("include", "wa.me");
    });
  });
});
