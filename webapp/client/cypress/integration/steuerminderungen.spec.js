describe("Steuerminderungen", () => {
  context("when no steuerminderungen selected", () => {
    beforeEach(() => {
      cy.login();
    });

    it("next page should be summary", () => {
      cy.visit("/lotse/step/select_stmind");
      cy.extended_footer_is_disabled(true);
      cy.get("[name=next_button]").click();
      cy.location().should((loc) => {
        expect(loc.pathname.toString()).to.contain("/lotse/step/summary");
      });
    });

    it("vorsorge should be skipped", () => {
      cy.visit("/lotse/step/vorsorge");
      cy.extended_footer_is_disabled(true);
      cy.location().should((loc) => {
        expect(loc.pathname.toString()).to.contain("/lotse/step/select_stmind");
      });
      cy.get("div[role=alert]").should("exist");
    });

    it("ausserg_bela should be skipped", () => {
      cy.visit("/lotse/step/ausserg_bela");
      cy.extended_footer_is_disabled(true);
      cy.location().should((loc) => {
        expect(loc.pathname.toString()).to.contain("/lotse/step/select_stmind");
      });
      cy.get("div[role=alert]").should("exist");
    });

    it("haushaltsnahe_handwerker should be skipped", () => {
      cy.visit("/lotse/step/haushaltsnahe_handwerker");
      cy.extended_footer_is_disabled(true);
      cy.location().should((loc) => {
        expect(loc.pathname.toString()).to.contain("/lotse/step/select_stmind");
      });
      cy.get("div[role=alert]").should("exist");
    });

    it("religion should be skipped", () => {
      cy.visit("/lotse/step/religion");
      cy.extended_footer_is_disabled(true);
      cy.location().should((loc) => {
        expect(loc.pathname.toString()).to.contain("/lotse/step/select_stmind");
      });
      cy.get("div[role=alert]").should("exist");
    });

    it("spenden should be skipped", () => {
      cy.visit("/lotse/step/spenden");
      cy.extended_footer_is_disabled(true);
      cy.location().should((loc) => {
        expect(loc.pathname.toString()).to.contain("/lotse/step/select_stmind");
      });
      cy.get("div[role=alert]").should("exist");
    });
  });

  context("when parts of steuerminderungen selected", () => {
    beforeEach(() => {
      cy.login();
      cy.visit("/lotse/step/select_stmind");
      cy.extended_footer_is_disabled(true);
    });

    it("correct steps displayed if only first step selected", () => {
      cy.get("label[for=stmind_select_vorsorge]").click();
      cy.get("[name=next_button]").click();
      cy.location().should((loc) => {
        expect(loc.pathname.toString()).to.contain("/lotse/step/vorsorge");
      });
      cy.get("[name=next_button]").click();
      cy.location().should((loc) => {
        expect(loc.pathname.toString()).to.contain("/lotse/step/summary");
      });
    });

    it("correct steps displayed if only last step selected", () => {
      cy.get("label[for=stmind_select_religion]").click();
      cy.get("[name=next_button]").click();
      cy.location().should((loc) => {
        expect(loc.pathname.toString()).to.contain("/lotse/step/religion");
      });
      cy.get("[name=next_button]").click();
      cy.location().should((loc) => {
        expect(loc.pathname.toString()).to.contain("/lotse/step/summary");
      });
    });

    it("correct steps displayed if only step in the middle selected", () => {
      cy.get("label[for=stmind_select_ausserg_bela]").click();
      cy.get("[name=next_button]").click();
      cy.location().should((loc) => {
        expect(loc.pathname.toString()).to.contain("/lotse/step/ausserg_bela");
      });
      cy.get("[name=next_button]").click();
      cy.location().should((loc) => {
        expect(loc.pathname.toString()).to.contain("/lotse/step/summary");
      });
    });

    it("correct steps displayed if multiple consecutive steps selected", () => {
      cy.get("label[for=stmind_select_spenden]").click();
      cy.get("label[for=stmind_select_religion]").click();
      cy.get("[name=next_button]").click();
      cy.location().should((loc) => {
        expect(loc.pathname.toString()).to.contain("/lotse/step/spenden");
      });
      cy.get("[name=next_button]").click();
      cy.location().should((loc) => {
        expect(loc.pathname.toString()).to.contain("/lotse/step/religion");
      });
      cy.get("[name=next_button]").click();
      cy.location().should((loc) => {
        expect(loc.pathname.toString()).to.contain("/lotse/step/summary");
      });
    });

    it("correct steps displayed if multiple non-consecutive steps selected", () => {
      cy.get("label[for=stmind_select_ausserg_bela]").click();
      cy.get("label[for=stmind_select_spenden]").click();
      cy.get("[name=next_button]").click();
      cy.location().should((loc) => {
        expect(loc.pathname.toString()).to.contain("/lotse/step/ausserg_bela");
      });
      cy.get("[name=next_button]").click();
      cy.location().should((loc) => {
        expect(loc.pathname.toString()).to.contain("/lotse/step/spenden");
      });
      cy.get("[name=next_button]").click();
      cy.location().should((loc) => {
        expect(loc.pathname.toString()).to.contain("/lotse/step/summary");
      });
    });
  });

  context("when all steuerminderungen selected", () => {
    beforeEach(() => {
      cy.login();
      cy.visit("/lotse/step/select_stmind");
      cy.extended_footer_is_disabled(true);
      cy.get("label[for=stmind_select_vorsorge]").click();
      cy.get("label[for=stmind_select_ausserg_bela]").click();
      cy.get("label[for=stmind_select_handwerker]").click();
      cy.get("label[for=stmind_select_spenden]").click();
      cy.get("label[for=stmind_select_religion]").click();
      cy.get("[name=next_button]").click();
    });

    it("page order should be correct", () => {
      cy.visit("/lotse/step/select_stmind");
      cy.get("[name=next_button]").click();
      cy.location().should((loc) => {
        expect(loc.pathname.toString()).to.contain("/lotse/step/vorsorge");
      });
      cy.get("[name=next_button]").click();
      cy.location().should((loc) => {
        expect(loc.pathname.toString()).to.contain("/lotse/step/ausserg_bela");
      });
      cy.get("[name=next_button]").click();
      cy.location().should((loc) => {
        expect(loc.pathname.toString()).to.contain(
          "/lotse/step/haushaltsnahe_handwerker"
        );
      });
      cy.get("[name=next_button]").click();
      cy.location().should((loc) => {
        expect(loc.pathname.toString()).to.contain("/lotse/step/spenden");
      });
      cy.get("[name=next_button]").click();
      cy.location().should((loc) => {
        expect(loc.pathname.toString()).to.contain("/lotse/step/religion");
      });
      cy.get("[name=next_button]").click();
      cy.location().should((loc) => {
        expect(loc.pathname.toString()).to.contain("/lotse/step/summary");
      });
    });

    it("vorsorge should not be skipped", () => {
      cy.visit("/lotse/step/vorsorge");
      cy.location().should((loc) => {
        expect(loc.pathname.toString()).to.contain("/lotse/step/vorsorge");
      });
      cy.get("div[role=alert]").should("not.exist");
    });

    it("ausserg_bela should not be skipped", () => {
      cy.visit("/lotse/step/ausserg_bela");
      cy.location().should((loc) => {
        expect(loc.pathname.toString()).to.contain("/lotse/step/ausserg_bela");
      });
      cy.get("div[role=alert]").should("not.exist");
    });

    it("haushaltsnahe_handwerker should not be skipped", () => {
      cy.visit("/lotse/step/haushaltsnahe_handwerker");
      cy.location().should((loc) => {
        expect(loc.pathname.toString()).to.contain(
          "/lotse/step/haushaltsnahe_handwerker"
        );
      });
      cy.get("div[role=alert]").should("not.exist");
    });

    it("religion should not be skipped", () => {
      cy.visit("/lotse/step/religion");
      cy.location().should((loc) => {
        expect(loc.pathname.toString()).to.contain("/lotse/step/religion");
      });
      cy.get("div[role=alert]").should("not.exist");
    });

    it("spenden should not be skipped", () => {
      cy.visit("/lotse/step/spenden");
      cy.location().should((loc) => {
        expect(loc.pathname.toString()).to.contain("/lotse/step/spenden");
      });
      cy.get("div[role=alert]").should("not.exist");
    });
  });
});

describe("Gemeinsamer Haushalt", () => {
  context("when single", () => {
    beforeEach(() => {
      cy.login();
      cy.visit("/lotse/step/familienstand");
      cy.extended_footer_is_disabled(true);
      cy.get("label[for=familienstand-0]").click();
      cy.get("[name=next_button]").click();
    });

    context("when haushaltsnahe_handwerker selected", () => {
      beforeEach(() => {
        cy.visit("/lotse/step/select_stmind");
        cy.extended_footer_is_disabled(true);
        cy.get("label[for=stmind_select_handwerker]").click();
        cy.get("[name=next_button]").click();
      });

      context("haushaltsnahe filled", () => {
        beforeEach(() => {
          cy.visit("/lotse/step/haushaltsnahe_handwerker");
          cy.extended_footer_is_disabled(true);
          cy.get("#stmind_haushaltsnahe_entries-div")
            .children()
            .should("have.length", 1);
          cy.get("button[id=stmind_haushaltsnahe_entries-add]").click();
          cy.get("#stmind_haushaltsnahe_entries-div")
            .children()
            .eq(0)
            .type("Gartenarbeit");
          cy.get("#stmind_haushaltsnahe_summe").type("300");
          cy.get("[name=next_button]").click();
        });

        it("gem_haushalt should not be skipped", () => {
          cy.visit("/lotse/step/gem_haushalt");
          cy.extended_footer_is_disabled(true);
          cy.location().should((loc) => {
            expect(loc.pathname.toString()).to.contain(
              "/lotse/step/gem_haushalt"
            );
          });
        });
      });

      context("handwerker filled", () => {
        beforeEach(() => {
          cy.visit("/lotse/step/haushaltsnahe_handwerker");
          cy.extended_footer_is_disabled(true);
          cy.get("button[id=stmind_handwerker_entries-add]").click();
          cy.get("#stmind_handwerker_entries-div")
            .children()
            .eq(0)
            .type("Badezimmer");
          cy.get("#stmind_handwerker_summe").type("15");
          cy.get("#stmind_handwerker_lohn_etc_summe").type("10");
          cy.get("[name=next_button]").click();
        });

        it("gem_haushalt should not be skipped", () => {
          cy.visit("/lotse/step/gem_haushalt");
          cy.extended_footer_is_disabled(true);
          cy.location().should((loc) => {
            expect(loc.pathname.toString()).to.contain(
              "/lotse/step/gem_haushalt"
            );
          });
        });
      });

      it("gem_haushalt should be skipped", () => {
        cy.visit("/lotse/step/gem_haushalt");
        cy.extended_footer_is_disabled(true);
        cy.location().should((loc) => {
          expect(loc.pathname.toString()).to.contain(
            "/lotse/step/haushaltsnahe_handwerker"
          );
        });
        cy.get("div[role=alert]").should("exist");
      });
    });

    it("gem_haushalt should be skipped", () => {
      cy.visit("/lotse/step/gem_haushalt");
      cy.extended_footer_is_disabled(true);
      cy.location().should((loc) => {
        expect(loc.pathname.toString()).to.contain("/lotse/step/select_stmind");
      });
      cy.get("div[role=alert]").should("exist");
    });
  });
  context("when married", () => {
    beforeEach(() => {
      cy.login();
      cy.visit("/lotse/step/familienstand");
      cy.extended_footer_is_disabled(true);
      cy.get("label[for=familienstand-1]").click();
      cy.get("#familienstand_date_1").type("1");
      cy.get("#familienstand_date_2").type("1");
      cy.get("#familienstand_date_3").type("1980");
      cy.get("label[for=familienstand_married_lived_separated-no]").click();
      cy.get("label[for=familienstand_confirm_zusammenveranlagung]")
        .first()
        .click();
      cy.get("[name=next_button]").click();
    });

    it("gem_haushalt should be skipped", () => {
      cy.visit("/lotse/step/gem_haushalt");
      cy.extended_footer_is_disabled(true);
      cy.location().should((loc) => {
        expect(loc.pathname.toString()).to.contain("/lotse/step/familienstand");
      });
      cy.get("div[role=alert]").should("exist");
    });
  });
});
