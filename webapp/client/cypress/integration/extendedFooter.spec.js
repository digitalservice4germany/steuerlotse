describe("Extended footer is not disabled", () => {
  afterEach(() => {
    cy.extended_footer_is_disabled(false);
  });

  context("start page", () => {
    it("Should not disable extended footer", () => {
      cy.visit("/");
    });
  });

  context("information page", () => {
    it("Should not disable extended footer", () => {
      cy.visit("/sofunktionierts");
    });
  });

  context("registration page", () => {
    it("Should not disable extended footer", () => {
      cy.visit("/unlock_code_request/step/data_input");
    });
  });

  context("data protection page", () => {
    it("Should not disable extended footer", () => {
      cy.visit("/datenschutz");
    });
  });

  context("terms and conditions page", () => {
    it("Should not disable extended footer", () => {
      cy.visit("/agb");
    });
  });

  context("imprint page", () => {
    it("Should not disable extended footer", () => {
      cy.visit("/impressum");
    });
  });

  context("accessibility page", () => {
    it("Should not disable extended footer", () => {
      cy.visit("/barrierefreiheit");
    });
  });

  context("contact page", () => {
    it("Should not disable extended footer", () => {
      cy.visit("/kontakt");
    });
  });

  context("unlock code revocation page", () => {
    it("Should not disable extended footer", () => {
      cy.visit("/unlock_code_revocation/step/data_input");
    });
  });

  context("about page", () => {
    it("Should not disable extended footer", () => {
      cy.visit("/ueber");
    });
  });

  context("digital service page", () => {
    it("Should not disable extended footer", () => {
      cy.visit("/digitalservice");
    });
  });

  context("unlock code activation page", () => {
    it("Should not disable extended footer", () => {
      cy.visit("/unlock_code_activation/step/data_input");
    });
  });
});

describe("Extended footer is disabled", () => {
  afterEach(() => {
    cy.extended_footer_is_disabled(true);
  });

  context("within eligibility steps", () => {
    const eligibility_step = "/eligibility/step/";

    it("Welcome page", () => {
      cy.visit(eligibility_step + "welcome");
    });

    it("Marital status page", () => {
      cy.visit(eligibility_step + "marital_status");
    });

    it("Separated page", () => {
      cy.visit(eligibility_step + "separated");
    });

    it("Single alimony page", () => {
      cy.visit(eligibility_step + "single_alimony");
    });

    it("Divorced joint taxes page", () => {
      cy.visit(eligibility_step + "divorced_joint_taxes");
    });

    it("Married alimony page", () => {
      cy.visit(eligibility_step + "married_alimony");
    });

    it("User A has elster account page", () => {
      cy.visit(eligibility_step + "user_a_has_elster_account");
    });

    it("Pension page", () => {
      cy.visit(eligibility_step + "pension");
    });

    it("Investment income page", () => {
      cy.visit(eligibility_step + "investment_income");
    });

    it("Employment income page", () => {
      cy.visit(eligibility_step + "employment_income");
    });

    it("Income other page", () => {
      cy.visit(eligibility_step + "income_other");
    });

    it("Foreign country page", () => {
      cy.visit(eligibility_step + "foreign_country");
    });

    it("Success page", () => {
      cy.visit(eligibility_step + "success");
    });

    it("Foreign country failure page", () => {
      cy.visit(eligibility_step + "foreign_country_failure");
    });

    it("Income other failure page", () => {
      cy.visit(eligibility_step + "income_other_failure");
    });

    it("Marginal employment page", () => {
      cy.visit(eligibility_step + "marginal_employment");
    });

    it("Marginal employment failure page", () => {
      cy.visit(eligibility_step + "marginal_employment_failure");
    });

    it("Minimal investment income page", () => {
      cy.visit(eligibility_step + "minimal_investment_income");
    });

    it("Taxed investment page", () => {
      cy.visit(eligibility_step + "taxed_investment");
    });

    it("Taxed investment failure page", () => {
      cy.visit(eligibility_step + "taxed_investment_failure");
    });

    it("Cheaper check page", () => {
      cy.visit(eligibility_step + "cheaper_check");
    });

    it("Cheaper check failure page", () => {
      cy.visit(eligibility_step + "cheaper_check_failure");
    });

    it("Pension failure page", () => {
      cy.visit(eligibility_step + "pension_failure");
    });

    it("User B has elster account page", () => {
      cy.visit(eligibility_step + "user_b_has_elster_account");
    });

    it("Married alimony page page", () => {
      cy.visit(eligibility_step + "married_alimony_failure");
    });

    it("Married joint taxes failure page", () => {
      cy.visit(eligibility_step + "married_joint_taxes_failure");
    });

    it("Separated lived together page", () => {
      cy.visit(eligibility_step + "separated_lived_together");
    });

    it("Separated joint taxes page", () => {
      cy.visit(eligibility_step + "separated_joint_taxes");
    });

    it("Single elster account page", () => {
      cy.visit(eligibility_step + "single_elster_account");
    });
  });

  context("within tax declaration form steps", () => {
    beforeEach(() => {
      cy.login();
    });

    const form_step = "/lotse/step/";

    it("Declaration incomes page", () => {
      cy.visit(form_step + "decl_incomes");
    });

    it("Declaration edaten page", () => {
      cy.visit(form_step + "decl_edaten");
    });

    it("Session note page", () => {
      cy.visit(form_step + "session_note");
    });

    it("Marital status page", () => {
      cy.visit(form_step + "familienstand");
    });

    it("Tax number page", () => {
      cy.visit(form_step + "steuernummer");
    });

    it("Person A page", () => {
      cy.visit(form_step + "person_a");
    });

    it("Person A has disability page", () => {
      cy.visit(form_step + "has_disability_person_a");
    });

    it("Person A markers page", () => {
      cy.visit(form_step + "merkzeichen_person_a");
    });

    it("Person A no flat rate page", () => {
      cy.visit(form_step + "person_a_no_pauschbetrag");
    });

    it("Person A requests flat rate page", () => {
      cy.visit(form_step + "person_a_requests_pauschbetrag");
    });

    it("Person A requests flat rate for travel expenses page", () => {
      cy.visit(form_step + "person_a_requests_fahrtkostenpauschale");
    });

    it("Person B page", () => {
      cy.visit(form_step + "person_a");
    });

    it("Person B has disability page", () => {
      cy.visit(form_step + "has_disability_person_b");
    });

    it("Person B markers page", () => {
      cy.visit(form_step + "merkzeichen_person_b");
    });

    it("Person B no flat rate page", () => {
      cy.visit(form_step + "person_b_no_pauschbetrag");
    });

    it("Person B requests flat rate page", () => {
      cy.visit(form_step + "person_b_requests_pauschbetrag");
    });

    it("Person B requests flat rate for travel expenses page", () => {
      cy.visit(form_step + "person_b_requests_fahrtkostenpauschale");
    });

    it("Telephone number page", () => {
      cy.visit(form_step + "telephone_number");
    });

    it("IBAN page", () => {
      cy.visit(form_step + "iban");
    });

    it("Select stmind page", () => {
      cy.visit(form_step + "select_stmind");
    });

    it("Provision page", () => {
      cy.visit(form_step + "vorsorge");
    });

    it("Exceptional costs page", () => {
      cy.visit(form_step + "ausserg_bela");
    });

    it("haushaltsnahe_handwerker page", () => {
      cy.visit(form_step + "haushaltsnahe_handwerker");
    });

    it("Donations page", () => {
      cy.visit(form_step + "spenden");
    });

    it("Religion page", () => {
      cy.visit(form_step + "religion");
    });

    it("Summary page", () => {
      cy.visit(form_step + "summary");
    });

    it("Confirmation page", () => {
      cy.visit(form_step + "confirmation");
    });

    it("Filing page", () => {
      cy.visit(form_step + "filing");
    });

    it("Ack page", () => {
      cy.visit(form_step + "ack");
    });
  });
});
