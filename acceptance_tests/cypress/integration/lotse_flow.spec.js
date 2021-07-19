/// <reference types="cypress" />

const authPassword = Cypress.env('STAGING_AUTH_PASSWORD')
Cypress.config('baseUrl', `https://lotse:${authPassword}@www-staging.stl.ds4g.dev`)

const unlockCodeData = {
    idnr: '09531672807',
    dob: '22.12.1972',
}

const taxReturnData = {
    unlockCode1: 'DBNH',
    unlockCode2: 'B8JS',
    unlockCode3: '9JE7',
    taxNr: '19811310010',
    marriedDate: '01.01.1990',
    iban: 'DE02500105170137075030',
    personA: {
        idnr: '04452397687',
        dob: '01.01.1990',
        firstName: 'Erika',
        lastName: 'Musterfrau',
        street: 'Musterstr.',
        streetNumber: '1',
        streetNumberExt: 'a',
        addressExt: 'Seitenflügel',
        postalCode: '11111',
        town: 'Musterhausen',
        behGrad: '25',
    },
    personB: {
        idnr: '02293417683',
        dob: '25.02.1951',
        firstName: 'Gerta',
        lastName: 'Mustername',
        street: 'Musterstr.',
        streetNumber: '1',
        postalCode: '11111',
        town: 'Musterhausen',
    },
    stmind: {
        vorsorge: {
            summe: '111.11',
        },
        krankheitskosten: {
            summe: '1011.11',
            anspruch: '1011.12',
        },
        pflegekosten: {
            summe: '2022.21',
            anspruch: '2022.22',
        },
        behAufw: {
            summe: '3033.31',
            anspruch: '3033.32',
        },
        behKfz: {
            summe: '4044.41',
            anspruch: '4044.42',
        },
        bestattung: {
            summe: '5055.51',
            anspruch: '5055.52',
        },
        aussergbelaSonst: {
            summe: '6066.61',
            anspruch: '6066.62',
        },
        haushaltsnahe: {
            entries: ["Gartenarbeiten", "Regenrinne"],
            summe: '500.00'
        },
        handwerker: {
            entries: ["Renovierung", "Badezimmer"],
            summe: '200.00',
            lohnEtcSumme: '100.00',
        },
        religion: {
            paidSumme: '444.44',
            reimbursedSumme: '555.55',
        },

        spenden: {
            inland: '222.22',
            inlandParteien: '333.33'
        }
    }
}

const older_date = '31.12.2019'
const recent_date = '01.01.2020'
const one_day_into_the_tax_year = '02.01.2020'

const submitBtnSelector = '[name="next_button"]'
const overviewBtnSelector = '[name="overview_button"]'
const login = function () {
    // Log in
    cy.get('.nav-link').contains('Ihre Steuererklärung').click()
    cy.get('#idnr').type(taxReturnData.personA.idnr)
    cy.get('#unlock_code_1').type(taxReturnData.unlockCode1)
    cy.get('#unlock_code_2').type(taxReturnData.unlockCode2)
    cy.get('#unlock_code_3').type(taxReturnData.unlockCode3)
    cy.get(submitBtnSelector).click()  // Submit form
    cy.get(submitBtnSelector).click()  // Skip confirmation
}

context('Acceptance tests', () => {
    beforeEach(() => {
        cy.visit('/')
    });

    it('Check that registration and revocation are clickable', () => {
        cy.get('a').contains(/^Registrieren$/)
            .should('have.class', 'nav-link')
            .should('not.have.class', 'inactive')
        cy.get('a').contains(/^Freischaltcode Stornierung$/)
            .should('not.have.class', 'inactive')
    })

    context('When I am logged in', () => {
        beforeEach(() => {
            login()
        })

        it('Check that registration and revocation are disabled', () => {
            cy.get('span').contains(/^Registrieren$/)
                .should('have.class', 'nav-link')
                .should('have.class', 'inactive')
            cy.get('span').contains(/^Freischaltcode Stornierung$/)
                .should('have.class', 'inactive')
        })

        it('Enter different familienstands', () => {
            cy.visit('/lotse/step/familienstand?link_overview=True')

            // Single
            cy.get('#familienstand-0').check()
            cy.get('#familienstand_date').should('not.be.visible')

            // Married
            cy.get('#familienstand-1').check()
            cy.get('#familienstand_date').clear().type(older_date)
            cy.get('label[for=familienstand_married_lived_separated-no]').click()
            cy.get('label[for=familienstand_confirm_zusammenveranlagung]').should('be.visible')

            cy.get('label[for=familienstand_married_lived_separated-yes]').click()
            cy.get('#familienstand_married_lived_separated_since').clear().type(older_date)
            cy.get('div[id=familienstand_zusammenveranlagung_field]').should('not.be.visible')

            cy.get('label[for=familienstand_married_lived_separated-yes]').click()
            cy.get('#familienstand_married_lived_separated_since').clear().type(one_day_into_the_tax_year)
            cy.get('div[id=familienstand_zusammenveranlagung_field]').should('be.visible')

            // Married -> different -> married
            cy.get('#familienstand-1').check()
            cy.get('#familienstand_date').clear().type(older_date)
            cy.get('label[for=familienstand_married_lived_separated-no]').click()
            cy.get('div[id=familienstand_confirm_zusammenveranlagung_field]').should('be.visible')
            cy.get('label[for=familienstand_confirm_zusammenveranlagung]').first().click()
            cy.get('#familienstand_confirm_zusammenveranlagung').should('be.checked')
            cy.get('#familienstand-0').check()
            cy.get('#familienstand-1').check()
            cy.get('div[id=familienstand_confirm_zusammenveranlagung_field]').should('not.be.visible')
            cy.get('label[for=familienstand_married_lived_separated-no]').click()
            cy.get('div[id=familienstand_confirm_zusammenveranlagung_field]').should('be.visible')
            cy.get('#familienstand_confirm_zusammenveranlagung').should('not.be.checked')

            // Widowed
            cy.get('#familienstand-2').check()
            cy.get('#familienstand_date').clear().type(older_date)
            cy.get('#familienstand_widowed_lived_separated').should('not.be.visible')

            cy.get('#familienstand_date').clear().type(recent_date)
            cy.get('label[for=familienstand_widowed_lived_separated-no]').click()
            cy.get('label[for=familienstand_confirm_zusammenveranlagung]').first().click()

            cy.get('label[for=familienstand_widowed_lived_separated-yes]').click()
            cy.get('#familienstand_widowed_lived_separated_since').clear().type(older_date)
            cy.get('div[id=familienstand_zusammenveranlagung_field]').should('not.be.visible')

            cy.get('label[for=familienstand_widowed_lived_separated-yes]').click()
            cy.get('#familienstand_widowed_lived_separated_since').clear().type(one_day_into_the_tax_year)
            cy.get('div[id=familienstand_zusammenveranlagung_field]').should('be.visible')

            // Divorced
            cy.get('#familienstand-3').check()
            cy.get('#familienstand_date').clear().type(older_date)
            cy.get('div[id=familienstand_zusammenveranlagung_field]').should('not.be.visible')
        })

        context('Submitting tax returns', () => {
            beforeEach(() => {
                // Step 1: accept opt-ins
                cy.get('label[for=declaration_incomes]').first().click()
                cy.get(submitBtnSelector).click()
                cy.get('label[for=declaration_edaten]').first().click()
                cy.get(submitBtnSelector).click()
                cy.get(submitBtnSelector).click()
            });

            it('for one person without deductions', () => {
                // Step 2
                cy.get('#familienstand-0').check()
                cy.get(submitBtnSelector).click()
                cy.get('select[id=bundesland]').select('BY')
                cy.get('#steuernummer').type(taxReturnData.taxNr)
                cy.get(submitBtnSelector).click()
                cy.get('#person_a_idnr').type(taxReturnData.personA.idnr)
                cy.get('#person_a_dob').type(taxReturnData.personA.dob)
                cy.get('#person_a_first_name').type(taxReturnData.personA.firstName)
                cy.get('#person_a_last_name').type(taxReturnData.personA.lastName)
                cy.get('#person_a_street').type(taxReturnData.personA.street)
                cy.get('#person_a_street_number').type(taxReturnData.personA.streetNumber)
                cy.get('#person_a_plz').type(taxReturnData.personA.postalCode)
                cy.get('#person_a_town').type(taxReturnData.personA.town)
                cy.get(submitBtnSelector).click()

                cy.get('label[for=is_person_a_account_holder]').first().click()
                cy.get('#iban').type(taxReturnData.iban)
                cy.get(submitBtnSelector).click()

                // Step 3
                cy.get('#steuerminderung-1').click()
                cy.get(submitBtnSelector).click()

                // Step 4
                cy.get('label[for=confirm_complete_correct]').first().click()
                cy.get(submitBtnSelector).click()
                cy.get('label[for=confirm_data_privacy]').first().click()
                cy.get('label[for=confirm_terms_of_service]').first().click()
                cy.get(submitBtnSelector).click()

                // Verify success.
                cy.get('body').contains('Ihre Informationen wurden erfolgreich verschickt.')
                // Get PDF - can't click on it as it opens a new window, so we request it directly
                cy.request('/download_pdf/print.pdf').its('body').should('not.be.empty')
                cy.get(submitBtnSelector).click()
                cy.get('body').contains('Herzlichen Glückwunsch!')
            });

            it('for a married couple with deductions', () => {
                // Step 2
                cy.get('#familienstand-1').check()
                cy.get('#familienstand_date').type(taxReturnData.marriedDate)
                cy.get('label[for=familienstand_married_lived_separated-no]').click()
                cy.get('label[for=familienstand_confirm_zusammenveranlagung]').first().click()
                cy.get(submitBtnSelector).click()
                cy.get('select[id=bundesland]').select('BY')
                cy.get('#steuernummer').type(taxReturnData.taxNr)
                cy.get(submitBtnSelector).click()
                cy.get('#person_a_idnr').type(taxReturnData.personA.idnr)
                cy.get('#person_a_dob').type(taxReturnData.personA.dob)
                cy.get('#person_a_first_name').type(taxReturnData.personA.firstName)
                cy.get('#person_a_last_name').type(taxReturnData.personA.lastName)
                cy.get('#person_a_street').type(taxReturnData.personA.street)
                cy.get('#person_a_street_number').type(taxReturnData.personA.streetNumber)
                cy.get('#person_a_street_number_ext').type(taxReturnData.personA.streetNumberExt)
                cy.get('#person_a_address_ext').type(taxReturnData.personA.addressExt)
                cy.get('#person_a_plz').type(taxReturnData.personA.postalCode)
                cy.get('#person_a_town').type(taxReturnData.personA.town)
                cy.get('#person_a_beh_grad').type(taxReturnData.personA.behGrad)
                cy.get('label[for=person_a_blind]').first().click()
                cy.get('label[for=person_a_gehbeh]').first().click()
                cy.get(submitBtnSelector).click()
                cy.get('#person_b_idnr').type(taxReturnData.personB.idnr)
                cy.get('#person_b_dob').type(taxReturnData.personB.dob)
                cy.get('#person_b_first_name').type(taxReturnData.personB.firstName)
                cy.get('#person_b_last_name').type(taxReturnData.personB.lastName)
                cy.get('#person_b_same_address-1').click()
                cy.get('#person_b_street').type(taxReturnData.personB.street)
                cy.get('#person_b_street_number').type(taxReturnData.personB.streetNumber)
                cy.get('#person_b_plz').type(taxReturnData.personB.postalCode)
                cy.get('#person_b_town').type(taxReturnData.personB.town)
                cy.get('select[id=person_b_religion]').select('ev')
                cy.get(submitBtnSelector).click()

                cy.get('label[for=is_person_a_account_holder-0]').first().click()
                cy.get('#iban').type(taxReturnData.iban)
                cy.get(submitBtnSelector).click()

                // Step 3
                cy.get('#steuerminderung-0').click()
                cy.get(submitBtnSelector).click()
                cy.get('#stmind_vorsorge_summe').type(taxReturnData.stmind.vorsorge.summe)
                cy.get(submitBtnSelector).click()

                cy.get('#stmind_krankheitskosten_summe').type(taxReturnData.stmind.krankheitskosten.summe)
                cy.get('#stmind_krankheitskosten_anspruch').type(taxReturnData.stmind.krankheitskosten.anspruch)
                cy.get('#stmind_pflegekosten_summe').type(taxReturnData.stmind.pflegekosten.summe)
                cy.get('#stmind_pflegekosten_anspruch').type(taxReturnData.stmind.pflegekosten.anspruch)
                cy.get('#stmind_beh_aufw_summe').type(taxReturnData.stmind.behAufw.summe)
                cy.get('#stmind_beh_aufw_anspruch').type(taxReturnData.stmind.behAufw.anspruch)
                cy.get('#stmind_beh_kfz_summe').type(taxReturnData.stmind.behKfz.summe)
                cy.get('#stmind_beh_kfz_anspruch').type(taxReturnData.stmind.behKfz.anspruch)
                cy.get('#stmind_bestattung_summe').type(taxReturnData.stmind.bestattung.summe)
                cy.get('#stmind_bestattung_anspruch').type(taxReturnData.stmind.bestattung.anspruch)
                cy.get('#stmind_aussergbela_sonst_summe').type(taxReturnData.stmind.aussergbelaSonst.summe)
                cy.get('#stmind_aussergbela_sonst_anspruch').type(taxReturnData.stmind.aussergbelaSonst.anspruch)
                cy.get(submitBtnSelector).click()

                cy.get('#stmind_haushaltsnahe_entries-div').children().should('have.length', 1)
                cy.get('button[id=stmind_haushaltsnahe_entries-add]').click()
                cy.get('#stmind_haushaltsnahe_entries-div').children().should('have.length', 2)
                cy.get('#stmind_haushaltsnahe_entries-div').children().eq(0).type(taxReturnData.stmind.haushaltsnahe.entries[0])
                cy.get('#stmind_haushaltsnahe_entries-div').children().eq(1).type(taxReturnData.stmind.handwerker.entries[1])
                cy.get('#stmind_haushaltsnahe_summe').type(taxReturnData.stmind.haushaltsnahe.summe)
                cy.get(submitBtnSelector).click()

                cy.get('#stmind_handwerker_entries-div').children().should('have.length', 1)
                cy.get('button[id=stmind_handwerker_entries-add]').click()
                cy.get('#stmind_handwerker_entries-div').children().should('have.length', 2)
                cy.get('#stmind_handwerker_entries-div').children().eq(0).type(taxReturnData.stmind.handwerker.entries[0])
                cy.get('#stmind_handwerker_entries-div').children().eq(1).type(taxReturnData.stmind.handwerker.entries[1])
                cy.get('#stmind_handwerker_summe').type(taxReturnData.stmind.handwerker.summe)
                cy.get('#stmind_handwerker_lohn_etc_summe').type(taxReturnData.stmind.handwerker.lohnEtcSumme)
                cy.get(submitBtnSelector).click()

                cy.get('#stmind_religion_paid_summe').type(taxReturnData.stmind.religion.paidSumme)
                cy.get('#stmind_religion_reimbursed_summe').type(taxReturnData.stmind.religion.reimbursedSumme)
                cy.get(submitBtnSelector).click()

                cy.get('#stmind_spenden_inland').type(taxReturnData.stmind.spenden.inland)
                cy.get('#stmind_spenden_inland_parteien').type(taxReturnData.stmind.spenden.inlandParteien)
                cy.get(submitBtnSelector).click()

                // Step 4
                cy.get('label[for=confirm_complete_correct]').first().click()
                cy.get(submitBtnSelector).click()
                cy.get('label[for=confirm_data_privacy]').first().click()
                cy.get('label[for=confirm_terms_of_service]').first().click()
                cy.get(submitBtnSelector).click()

                // Verify success.
                cy.get('body').contains('Ihre Informationen wurden erfolgreich verschickt.')
                // Get PDF - can't click on it as it opens a new window, so we request it directly
                cy.request('/download_pdf/print.pdf').its('body').should('not.be.empty')
                cy.get(submitBtnSelector).click()
                cy.get('body').contains('Herzlichen Glückwunsch!')
            });

            afterEach(() => {
                // Logout and verify I do not have access anymore
                cy.get(submitBtnSelector).click()
                cy.location('pathname').should('eq', '/')
                cy.contains('Sie haben sich erfolgreich abgemeldet.')

                cy.visit('/lotse/step/summary')
                cy.contains('Sie müssen eingeloggt sein')
                cy.visit('/unlock_code_activation/step/data_input')
                cy.get('#idnr').should('have.value', '')
                cy.get('#unlock_code').should('have.value', '')
            });
        });
        // These tests could be split. However, to avoid hitting rate limits, keep it simple, and reduce the run time it is one test.
        it('Submit forms and check different redirects', () => {
            // No relationship set
            // Redirect person_b
            cy.visit('/lotse/step/person_b?link_overview=True')
            cy.location().should((loc) => {
                expect(loc.pathname.toString()).to.contain('/lotse/step/familienstand');
            });

            // Set relationship single -> Redirect person_b
            cy.visit('/lotse/step/familienstand')
            cy.get('#familienstand-0').check()
            cy.get(submitBtnSelector).click()
            cy.visit('/lotse/step/person_b?link_overview=True')
            cy.location().should((loc) => {
                expect(loc.pathname.toString()).to.contain('/lotse/step/familienstand');
            });

            // Set relationship widowed older -> Redirect person_b
            cy.visit('/lotse/step/familienstand')
            cy.get('#familienstand-2').check()
            cy.get('#familienstand_date').clear().type(older_date)
            cy.get(submitBtnSelector).click()
            cy.visit('/lotse/step/person_b?link_overview=True')
            cy.location().should((loc) => {
                expect(loc.pathname.toString()).to.contain('/lotse/step/familienstand');
            });

            // Set relationship widowed recent + zusammenveranlagung yes -> No redirect person_b
            cy.visit('/lotse/step/familienstand')
            cy.get('#familienstand-2').check()
            cy.get('#familienstand_date').clear().type(recent_date)
            cy.get('label[for=familienstand_widowed_lived_separated-no]').click()
            cy.get('label[for=familienstand_confirm_zusammenveranlagung]').first().click()
            cy.get(submitBtnSelector).click()
            cy.visit('/lotse/step/person_b?link_overview=True')
            cy.location().should((loc) => {
                expect(loc.pathname.toString()).to.contain('/lotse/step/person_b');
            });

            // Set relationship divorced -> Redirect person_b
            cy.visit('/lotse/step/familienstand')
            cy.get('#familienstand-3').check()
            cy.get('#familienstand_date').clear().type(recent_date)
            cy.get(submitBtnSelector).click()
            cy.visit('/lotse/step/person_b?link_overview=True')
            cy.location().should((loc) => {
                expect(loc.pathname.toString()).to.contain('/lotse/step/familienstand');
            });
            cy.visit('/lotse/step/familienstand')
            cy.get('#familienstand-3').check()
            cy.get('#familienstand_date').clear().type(older_date)
            cy.get(submitBtnSelector).click()
            cy.visit('/lotse/step/person_b?link_overview=True')
            cy.location().should((loc) => {
                expect(loc.pathname.toString()).to.contain('/lotse/step/familienstand');
            });

            // Set relationship married + separated + zusammenveranlagung-> No redirect person_b
            cy.visit('/lotse/step/familienstand')
            cy.get('#familienstand-1').check()
            cy.get('#familienstand_date').type(taxReturnData.marriedDate)
            cy.get('label[for=familienstand_married_lived_separated-yes]').click()
            cy.get('#familienstand_married_lived_separated_since').clear().type(one_day_into_the_tax_year)
            cy.get('label[for=familienstand_zusammenveranlagung-yes]').click()
            cy.get(submitBtnSelector).click()
            cy.visit('/lotse/step/person_b?link_overview=True')
            cy.location().should((loc) => {
                expect(loc.pathname.toString()).to.contain('/lotse/step/person_b');
            });

            // Set relationship married + separated + no zusammenveranlagung-> Redirect person_b
            cy.visit('/lotse/step/familienstand')
            cy.get('#familienstand-1').check()
            cy.get('#familienstand_date').type(taxReturnData.marriedDate)
            cy.get('label[for=familienstand_married_lived_separated-yes]').click()
            cy.get('#familienstand_married_lived_separated_since').clear().type(one_day_into_the_tax_year)
            cy.get('label[for=familienstand_zusammenveranlagung-no]').click()
            cy.get(submitBtnSelector).click()
            cy.visit('/lotse/step/person_b?link_overview=True')
            cy.location().should((loc) => {
                expect(loc.pathname.toString()).to.contain('/lotse/step/familienstand');
            });

            // No steuerminderung set
            // Redirect spenden
            cy.visit('/lotse/step/spenden?link_overview=True')
            cy.location().should((loc) => {
                expect(loc.pathname.toString()).to.contain('/lotse/step/steuerminderung_yesno');
            });

            // Set steuerminderung no
            cy.visit('/lotse/step/steuerminderung_yesno')
            cy.get('#steuerminderung-1').click()
            cy.get(submitBtnSelector).click()

            // Redirect vorsorge
            cy.visit('/lotse/step/vorsorge?link_overview=True')
            cy.location().should((loc) => {
                expect(loc.pathname.toString()).to.contain('/lotse/step/steuerminderung_yesno');
            });

            // Redirect ausserg_bela
            cy.visit('/lotse/step/ausserg_bela?link_overview=True')
            cy.location().should((loc) => {
                expect(loc.pathname.toString()).to.contain('/lotse/step/steuerminderung_yesno');
            });

            // Redirect haushaltsnahe
            cy.visit('/lotse/step/haushaltsnahe?link_overview=True')
            cy.location().should((loc) => {
                expect(loc.pathname.toString()).to.contain('/lotse/step/steuerminderung_yesno');
            });

            // Redirect gem_haushalt
            cy.visit('/lotse/step/gem_haushalt?link_overview=True')
            cy.location().should((loc) => {
                expect(loc.pathname.toString()).to.contain('/lotse/step/steuerminderung_yesno');
            });

            // Redirect religion
            cy.visit('/lotse/step/religion?link_overview=True')
            cy.location().should((loc) => {
                expect(loc.pathname.toString()).to.contain('/lotse/step/steuerminderung_yesno');
            });

            // Redirect spenden
            cy.visit('/lotse/step/spenden?link_overview=True')
            cy.location().should((loc) => {
                expect(loc.pathname.toString()).to.contain('/lotse/step/steuerminderung_yesno');
            });


            // Set steuerminderung yes
            cy.visit('/lotse/step/steuerminderung_yesno')
            cy.get('#steuerminderung-0').click()
            cy.get(submitBtnSelector).click()

            // No redirect vorsorge
            cy.visit('/lotse/step/vorsorge?link_overview=True')
            cy.location().should((loc) => {
                expect(loc.pathname.toString()).to.contain('/lotse/step/vorsorge');
            });

            // Redirect gem_haushalt
            cy.visit('/lotse/step/gem_haushalt?link_overview=True')
            cy.location().should((loc) => {
                expect(loc.pathname.toString()).to.contain('/lotse/step/familienstand');
            });


            // Set familienstand divorced
            cy.visit('/lotse/step/familienstand')
            cy.get('#familienstand-3').check()
            cy.get('#familienstand_date').clear().type(taxReturnData.marriedDate)
            cy.get(submitBtnSelector).click()

            // Redirect gem_haushalt
            cy.visit('/lotse/step/gem_haushalt?link_overview=True')
            cy.location().should((loc) => {
                expect(loc.pathname.toString()).to.contain('/lotse/step/haushaltsnahe');
            });


            // Set haushaltsnahe
            cy.get('#stmind_haushaltsnahe_entries-div').children().eq(0).type(taxReturnData.stmind.haushaltsnahe.entries[0])
            cy.get('#stmind_haushaltsnahe_summe').type(taxReturnData.stmind.haushaltsnahe.summe)
            cy.get(submitBtnSelector).click()

            // No redirect gem_haushalt
            cy.visit('/lotse/step/gem_haushalt?link_overview=True')
            cy.location().should((loc) => {
                expect(loc.pathname.toString()).to.contain('/lotse/step/gem_haushalt');
            });
        });
    });

    // Commented out, because it we otherwise run into ELSTER rate limits for FSC requests/revocations.
    // it('Request unlock code, then revoke it again', () => {
    //   // Go to login screen, then to request form
    //   cy.get('.nav-link').contains('Meine Steuererklärung').click()
    //   cy.get('a').contains('Freischaltcode Beantragen').click()

    //   // Fill and submit request form
    //   cy.get('#idnr').type(unlockCodeData.idnr)
    //   cy.get('#dob').type(unlockCodeData.dob)
    //   cy.get(submitBtnSelector).click()
    //   cy.get('body').contains('Freischaltcode wurde angefordert')

    //   // Return to login screen, then go to revocation form
    //   cy.get('.nav-link').contains('Meine Steuererklärung').click()
    //   cy.get('a').contains('Freischaltcode stornieren').click()

    //   // Fill and submit revocation form
    //   cy.get('#idnr').type(unlockCodeData.idnr)
    //   cy.get('#dob').type(unlockCodeData.dob)
    //   cy.get(submitBtnSelector).click()
    //   cy.get('body').contains('Stornierung erfolgreich')
    //});
});
