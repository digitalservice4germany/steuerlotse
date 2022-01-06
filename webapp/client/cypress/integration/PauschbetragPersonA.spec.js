describe("PauschbetragPersonA", () => {
  beforeEach(() => {
    cy.login();
  });

  context("with no data", () => {
    beforeEach(() => {
      cy.visit("/lotse/step/person_a_requests_pauschbetrag");
    });

    it("Should redirect to has disability page", () => {
      cy.location().should((loc) => {
        expect(loc.pathname.toString()).to.contain(
          "/lotse/step/person_a_has_disability"
        );
      });
    });
  });

  context("with has disability no", () => {
    beforeEach(() => {
      cy.request("POST", "/testing/set_data/form_data", {
        person_a_has_disability: "no",
      });

      cy.visit("/lotse/step/person_a_requests_pauschbetrag");
    });

    it("Should redirect to has disability page", () => {
      cy.location().should((loc) => {
        expect(loc.pathname.toString()).to.contain(
          "/lotse/step/person_a_has_disability"
        );
      });
    });
  });

  context("with no data for merkzeichen", () => {
    beforeEach(() => {
      cy.request("POST", "/testing/set_data/form_data", {
        person_a_has_disability: "yes",
      });

      cy.visit("/lotse/step/person_a_requests_pauschbetrag");
    });

    it("Should redirect to merkzeichen page", () => {
      cy.location().should((loc) => {
        expect(loc.pathname.toString()).to.contain(
          "/lotse/step/merkzeichen_person_a"
        );
      });
    });
  });

  context("with merkzeichen data", () => {
    beforeEach(() => {
      cy.request("POST", "/testing/set_data/form_data", {
        person_a_has_disability: "yes",
        person_a_disability_degree: "20",
        person_a_has_merkzeichen_g: true,
      });

      cy.visit("/lotse/step/person_a_requests_pauschbetrag");
    });

    it("Should not check radio button for label yes", () => {
      cy.get("#person_a_requests_pauschbetrag-yes").should("not.be.checked");
    });

    it("Should not check radio button for label no", () => {
      cy.get("#person_a_requests_pauschbetrag-no").should("not.be.checked");
    });

    it("Should stay on page and show error when submit button clicked", () => {
      cy.get("button[type=submit]").click();
      cy.url().should("include", "/lotse/step/person_a_requests_pauschbetrag");
      cy.get("[role=alert][for=person_a_requests_pauschbetrag]").contains(
        "Diese Angabe wird benötigt, um fortfahren zu können"
      );
    });
  });

  context("with person_a_requests_pauschbetrag yes", () => {
    beforeEach(() => {
      cy.request("POST", "/testing/set_data/form_data", {
        person_a_has_disability: "yes",
        person_a_disability_degree: "20",
        person_a_has_merkzeichen_g: true,
        person_a_requests_pauschbetrag: "yes",
      });

      cy.visit("/lotse/step/person_a_requests_pauschbetrag");
    });

    it("Should check radio button for label yes", () => {
      cy.get("#person_a_requests_pauschbetrag-yes").should("be.checked");
    });

    it("Should not check radio button for label no", () => {
      cy.get("#person_a_requests_pauschbetrag-no").should("not.be.checked");
    });

    it("Should link back to merkzeichen person a page", () => {
      cy.get("a").contains("Zurück").click();
      cy.url().should("include", "/lotse/step/merkzeichen_person_a");
    });

    it("Should link forward to telephone_number page", () => {
      cy.get("button[type=submit]").click();
      cy.url().should("include", "/lotse/step/telephone_number");
    });
  });

  context("with person_a_requests_pauschbetrag no", () => {
    beforeEach(() => {
      cy.request("POST", "/testing/set_data/form_data", {
        person_a_has_disability: "yes",
        person_a_disability_degree: "20",
        person_a_has_merkzeichen_g: true,
        person_a_requests_pauschbetrag: "no",
      });
      cy.visit("/lotse/step/person_a_requests_pauschbetrag");
    });

    it("Should check radio button for label no", () => {
      cy.get("#person_a_requests_pauschbetrag-no").should("be.checked");
    });

    it("Should not check radio button for label yes", () => {
      cy.get("#person_a_requests_pauschbetrag-yes").should("not.be.checked");
    });

    it("Should link forward to telephone_number page", () => {
      cy.get("button[type=submit]").click();
      cy.url().should("include", "/lotse/step/telephone_number");
    });
  });

  context("for joint taxes", () => {
    beforeEach(() => {
      cy.request("POST", "/testing/set_data/form_data", {
        familienstand: "married",
        familienstand_married_lived_separated: "no",
        familienstand_confirm_zusammenveranlagung: true,
        person_a_has_disability: "yes",
        person_a_disability_degree: "20",
        person_a_has_merkzeichen_g: true,
        person_a_requests_pauschbetrag: "yes",
      });
      cy.visit("/lotse/step/person_a_requests_pauschbetrag");
    });

    it("Should link forward to person b page", () => {
      cy.get("button[type=submit]").click();
      cy.url().should("include", "/lotse/step/person_b");
    });
  });
});
