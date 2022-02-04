describe("FahrtkostenpauschalePersonA", () => {
  beforeEach(() => {
    cy.login();
  });

  context("with no data", () => {
    beforeEach(() => {
      cy.visit("/lotse/step/person_b_requests_fahrtkostenpauschale");
    });

    it("Should redirect to familienstand page", () => {
      cy.location().should((loc) => {
        expect(loc.pathname.toString()).to.contain("/lotse/step/familienstand");
      });
    });
  });

  context("with married data", () => {
    beforeEach(() => {
      cy.request("POST", "/testing/set_session_data/form_data", {
        familienstand: "married",
        familienstand_married_lived_separated: "no",
        familienstand_confirm_zusammenveranlagung: true,
      });
      cy.visit("/lotse/step/person_b_requests_fahrtkostenpauschale");
    });

    it("Should redirect to has disability page", () => {
      cy.location().should((loc) => {
        expect(loc.pathname.toString()).to.contain(
          "/lotse/step/has_disability_person_b"
        );
      });
    });
  });

  context("with has disability no", () => {
    beforeEach(() => {
      cy.request("POST", "/testing/set_session_data/form_data", {
        familienstand: "married",
        familienstand_married_lived_separated: "no",
        familienstand_confirm_zusammenveranlagung: true,
        person_b_has_disability: "no",
      });

      cy.visit("/lotse/step/person_b_requests_fahrtkostenpauschale");
    });

    it("Should redirect to has disability page", () => {
      cy.location().should((loc) => {
        expect(loc.pathname.toString()).to.contain(
          "/lotse/step/has_disability_person_b"
        );
      });
    });
  });

  context("with no data for merkzeichen", () => {
    beforeEach(() => {
      cy.request("POST", "/testing/set_session_data/form_data", {
        familienstand: "married",
        familienstand_married_lived_separated: "no",
        familienstand_confirm_zusammenveranlagung: true,
        person_b_has_disability: "yes",
      });

      cy.visit("/lotse/step/person_b_requests_fahrtkostenpauschale");
    });

    it("Should redirect to merkzeichen page", () => {
      cy.location().should((loc) => {
        expect(loc.pathname.toString()).to.contain(
          "/lotse/step/merkzeichen_person_b"
        );
      });
    });
  });

  context("with merkzeichen data", () => {
    beforeEach(() => {
      cy.request("POST", "/testing/set_session_data/form_data", {
        familienstand: "married",
        familienstand_married_lived_separated: "no",
        familienstand_confirm_zusammenveranlagung: true,
        person_b_has_disability: "yes",
        person_b_disability_degree: "80",
        person_b_has_merkzeichen_g: true,
      });

      cy.visit("/lotse/step/person_b_requests_fahrtkostenpauschale");
    });

    it("Should not check radio button for label yes", () => {
      cy.get("#person_b_requests_fahrtkostenpauschale-yes").should(
        "not.be.checked"
      );
    });

    it("Should not check radio button for label no", () => {
      cy.get("#person_b_requests_fahrtkostenpauschale-no").should(
        "not.be.checked"
      );
    });

    it("Should show fahrtkostenpauschale on page", () => {
      cy.contains("900 Euro");
    });

    it("Should stay on page and show error when submit button clicked", () => {
      cy.get("button[type=submit]").click();
      cy.url().should(
        "include",
        "/lotse/step/person_b_requests_fahrtkostenpauschale"
      );
      cy.get(
        "[role=alert][for=person_b_requests_fahrtkostenpauschale]"
      ).contains("Diese Angabe wird benötigt, um fortfahren zu können");
    });
  });

  context("with person_b_requests_fahrtkostenpauschale yes", () => {
    beforeEach(() => {
      cy.request("POST", "/testing/set_session_data/form_data", {
        familienstand: "married",
        familienstand_married_lived_separated: "no",
        familienstand_confirm_zusammenveranlagung: true,
        person_b_has_disability: "yes",
        person_b_has_pflegegrad: "yes",
        person_b_disability_degree: "20",
        person_b_has_merkzeichen_g: true,
        person_b_requests_pauschbetrag: "yes",
        person_b_requests_fahrtkostenpauschale: "yes",
      });

      cy.visit("/lotse/step/person_b_requests_fahrtkostenpauschale");
    });

    it("Should check radio button for label yes", () => {
      cy.get("#person_b_requests_fahrtkostenpauschale-yes").should(
        "be.checked"
      );
    });

    it("Should not check radio button for label no", () => {
      cy.get("#person_b_requests_fahrtkostenpauschale-no").should(
        "not.be.checked"
      );
    });

    it("Should link back to request pauschbetrag person b page", () => {
      cy.get("a").contains("Zurück").click();
      cy.url().should("include", "/lotse/step/person_b_requests_pauschbetrag");
    });

    it("Should link forward to telephone_number page", () => {
      cy.get("button[type=submit]").click();
      cy.url().should("include", "/lotse/step/telephone_number");
    });
  });

  context("with person_b_requests_fahrtkostenpauschale no", () => {
    beforeEach(() => {
      cy.request("POST", "/testing/set_session_data/form_data", {
        familienstand: "married",
        familienstand_married_lived_separated: "no",
        familienstand_confirm_zusammenveranlagung: true,
        person_b_has_disability: "yes",
        person_b_disability_degree: "20",
        person_b_has_pflegegrad: "yes",
        person_b_has_merkzeichen_g: true,
        person_b_requests_pauschbetrag: "yes",
        person_b_requests_fahrtkostenpauschale: "no",
      });
      cy.visit("/lotse/step/person_b_requests_fahrtkostenpauschale");
    });

    it("Should check radio button for label no", () => {
      cy.get("#person_b_requests_fahrtkostenpauschale-no").should("be.checked");
    });

    it("Should not check radio button for label yes", () => {
      cy.get("#person_b_requests_fahrtkostenpauschale-yes").should(
        "not.be.checked"
      );
    });

    it("Should link forward to telephone_number page", () => {
      cy.get("button[type=submit]").click();
      cy.url().should("include", "/lotse/step/telephone_number");
    });
  });
});
