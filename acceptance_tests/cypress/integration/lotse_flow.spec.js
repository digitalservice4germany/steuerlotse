/// <reference types="cypress" />

const authPassword = Cypress.env('STAGING_AUTH_PASSWORD')
Cypress.config('baseUrl', `https://lotse:${authPassword}@www-staging.stl.ds4g.dev`)

const unlockCodeData = {
    idnr1: '09',
    idnr2: '531',
    idnr3: '672',
    idnr4: '807',
    dobDay: '22',
    dobMonth: '12',
    dobYear: '1972'
}

const taxReturnData = {
    unlockCode1: 'DBNH',
    unlockCode2: 'B8JS',
    unlockCode3: '9JE7',
    taxNr1: '198',
    taxNr2: '113',
    taxNr3: '10010',
    marriedDateDay: '01',
    marriedDateMonth: '01',
    marriedDateYear: '1990',
    telephoneNumber: '089 32168',
    iban: 'DE02500105170137075030',
    personA: {
        idnr1: '04',
        idnr2: '452',
        idnr3: '397',
        idnr4: '687',
        dobDay: '01',
        dobMonth: '01',
        dobYear: '1990',
        firstName: 'Erika',
        lastName: 'Musterfrau',
        street: 'Musterstr.',
        streetNumber: '1',
        streetNumberExt: 'a',
        addressExt: 'Seitenflügel',
        postalCode: '11111',
        town: 'Musterhausen',
        disabilityDegree: '25',
    },
    personB: {
        idnr1: '02',
        idnr2: '293',
        idnr3: '417',
        idnr4: '683',
        dobDay: '25',
        dobMonth: '2',
        dobYear: '1951',
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

const older_date_day = '31'
const older_date_month = '12'
const older_date_year = '2020'
const recent_date_day = '01'
const recent_date_month = '01'
const recent_date_year = '2021'
const one_day_into_the_tax_year_day = '02'
const one_day_into_the_tax_year_month = '01'
const one_day_into_the_tax_year_year = '2021'

const submitBtnSelector = '[name="next_button"]'
const overviewBtnSelector = '[name="overview_button"]'
const login = function () {
    // Log in
    cy.get('.nav-link').contains('Ihre Steuererklärung').click()
    cy.get('#idnr_1').type(taxReturnData.personA.idnr1)
    cy.get('#idnr_2').type(taxReturnData.personA.idnr2)
    cy.get('#idnr_3').type(taxReturnData.personA.idnr3)
    cy.get('#idnr_4').type(taxReturnData.personA.idnr4)
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

    context('When I am logged in', () => {
        beforeEach(() => {
            login()
        })

        it('Enter different familienstands', () => {
            cy.visit('/lotse/step/familienstand?link_overview=True')

            // Single
            cy.get('label[for=familienstand-0]').click()
            cy.get('#familienstand_date').should('not.be.visible')

            // Married
            cy.get('label[for=familienstand-1]').click()
            cy.get('#familienstand_date_1').clear().type(older_date_day)
            cy.get('#familienstand_date_2').clear().type(older_date_month)
            cy.get('#familienstand_date_3').clear().type(older_date_year)
            cy.get('label[for=familienstand_married_lived_separated-no]').click()
            cy.get('label[for=familienstand_confirm_zusammenveranlagung]').should('be.visible')

            cy.get('label[for=familienstand_married_lived_separated-yes]').click()
            cy.get('#familienstand_married_lived_separated_since_1').clear().type(older_date_day)
            cy.get('#familienstand_married_lived_separated_since_2').clear().type(older_date_month)
            cy.get('#familienstand_married_lived_separated_since_3').clear().type(older_date_year)
            cy.get('div[id=familienstand_zusammenveranlagung_field]').should('not.be.visible')

            cy.get('label[for=familienstand_married_lived_separated-yes]').click()
            cy.get('#familienstand_married_lived_separated_since_1').clear().type(one_day_into_the_tax_year_day)
            cy.get('#familienstand_married_lived_separated_since_2').clear().type(one_day_into_the_tax_year_month)
            cy.get('#familienstand_married_lived_separated_since_3').clear().type(one_day_into_the_tax_year_year)
            cy.get('div[id=familienstand_zusammenveranlagung_field]').should('be.visible')

            // Married -> different -> married
            cy.get('label[for=familienstand-1]').click()
            cy.get('#familienstand_date_1').clear().type(older_date_day)
            cy.get('#familienstand_date_2').clear().type(older_date_month)
            cy.get('#familienstand_date_3').clear().type(older_date_year)
            cy.get('label[for=familienstand_married_lived_separated-no]').click()
            cy.get('div[id=familienstand_confirm_zusammenveranlagung_field]').should('be.visible')
            cy.get('label[for=familienstand_confirm_zusammenveranlagung]').first().click()
            cy.get('#familienstand_confirm_zusammenveranlagung').should('be.checked')
            cy.get('label[for=familienstand-0]').click()
            cy.get('label[for=familienstand-1]').click()
            cy.get('div[id=familienstand_confirm_zusammenveranlagung_field]').should('not.be.visible')
            cy.get('label[for=familienstand_married_lived_separated-no]').click()
            cy.get('div[id=familienstand_confirm_zusammenveranlagung_field]').should('be.visible')
            cy.get('#familienstand_confirm_zusammenveranlagung').should('not.be.checked')

            // Widowed
            cy.get('label[for=familienstand-2]').click()
            cy.get('#familienstand_date_1').clear().type(older_date_day)
            cy.get('#familienstand_date_2').clear().type(older_date_month)
            cy.get('#familienstand_date_3').clear().type(older_date_year)
            cy.get('#familienstand_widowed_lived_separated').should('not.be.visible')

            cy.get('#familienstand_date_1').clear().type(recent_date_day)
            cy.get('#familienstand_date_2').clear().type(recent_date_month)
            cy.get('#familienstand_date_3').clear().type(recent_date_year)
            cy.get('label[for=familienstand_widowed_lived_separated-no]').click()
            cy.get('label[for=familienstand_confirm_zusammenveranlagung]').first().click()

            cy.get('label[for=familienstand_widowed_lived_separated-yes]').click()
            cy.get('#familienstand_widowed_lived_separated_since_1').clear().type(older_date_day)
            cy.get('#familienstand_widowed_lived_separated_since_2').clear().type(older_date_month)
            cy.get('#familienstand_widowed_lived_separated_since_3').clear().type(older_date_year)
            cy.get('div[id=familienstand_zusammenveranlagung_field]').should('not.be.visible')

            cy.get('label[for=familienstand_widowed_lived_separated-yes]').click()
            cy.get('#familienstand_widowed_lived_separated_since_1').clear().type(one_day_into_the_tax_year_day)
            cy.get('#familienstand_widowed_lived_separated_since_2').clear().type(one_day_into_the_tax_year_month)
            cy.get('#familienstand_widowed_lived_separated_since_3').clear().type(one_day_into_the_tax_year_year)
            cy.get('div[id=familienstand_zusammenveranlagung_field]').should('be.visible')

            // Divorced
            cy.get('label[for=familienstand-3]').click()
            cy.get('#familienstand_date_1').clear().type(older_date_day)
            cy.get('#familienstand_date_2').clear().type(older_date_month)
            cy.get('#familienstand_date_3').clear().type(older_date_year)
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
                cy.get('label[for=familienstand-0]').click()
                cy.get(submitBtnSelector).click()
                cy.get('label[for=steuernummer_exists-yes]').click()
                cy.get('select[id=bundesland]').select('BY')
                cy.get('#steuernummer_1').type(taxReturnData.taxNr1)
                cy.get('#steuernummer_2').type(taxReturnData.taxNr2)
                cy.get('#steuernummer_3').type(taxReturnData.taxNr3)
                cy.get(submitBtnSelector).click()
                cy.get('#person_a_idnr_1').type(taxReturnData.personA.idnr1)
                cy.get('#person_a_idnr_2').type(taxReturnData.personA.idnr2)
                cy.get('#person_a_idnr_3').type(taxReturnData.personA.idnr3)
                cy.get('#person_a_idnr_4').type(taxReturnData.personA.idnr4)
                cy.get('#person_a_dob_1').clear().type(taxReturnData.personA.dobDay)
                cy.get('#person_a_dob_2').clear().type(taxReturnData.personA.dobMonth)
                cy.get('#person_a_dob_3').type(taxReturnData.personA.dobYear)
                cy.get('#person_a_first_name').type(taxReturnData.personA.firstName)
                cy.get('#person_a_last_name').type(taxReturnData.personA.lastName)
                cy.get('#person_a_street').type(taxReturnData.personA.street)
                cy.get('#person_a_street_number').type(taxReturnData.personA.streetNumber)
                cy.get('#person_a_plz').type(taxReturnData.personA.postalCode)
                cy.get('#person_a_town').type(taxReturnData.personA.town)
                cy.get(submitBtnSelector).click()

                cy.get('label[for=person_a_has_disability-no]').click()
                cy.get(submitBtnSelector).click()

                cy.get('#telephone_number').type(taxReturnData.telephoneNumber)
                cy.get(submitBtnSelector).click()

                cy.get('label[for=is_user_account_holder]').first().click()
                cy.get('#iban').type(taxReturnData.iban, { delay: 50 })
                cy.get(submitBtnSelector).click()

                // Step 3
                // Do not select any stmind
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

            it('for one person without tax number without deductions', () => {
                // Step 2
                cy.get('label[for=familienstand-0]').click()
                cy.get(submitBtnSelector).click()

                cy.get('label[for=steuernummer_exists-no]').click()
                cy.get('select[id=bundesland]').select('BY')
                cy.get('select[id=bufa_nr]').select('9203')
                cy.get('label[for=request_new_tax_number]').first().click()

                cy.get(submitBtnSelector).click()
                cy.get('#person_a_idnr_1').type(taxReturnData.personA.idnr1)
                cy.get('#person_a_idnr_2').type(taxReturnData.personA.idnr2)
                cy.get('#person_a_idnr_3').type(taxReturnData.personA.idnr3)
                cy.get('#person_a_idnr_4').type(taxReturnData.personA.idnr4)
                cy.get('#person_a_dob_1').clear().type(taxReturnData.personA.dobDay)
                cy.get('#person_a_dob_2').clear().type(taxReturnData.personA.dobMonth)
                cy.get('#person_a_dob_3').type(taxReturnData.personA.dobYear)
                cy.get('#person_a_first_name').type(taxReturnData.personA.firstName)
                cy.get('#person_a_last_name').type(taxReturnData.personA.lastName)
                cy.get('#person_a_street').type(taxReturnData.personA.street)
                cy.get('#person_a_street_number').type(taxReturnData.personA.streetNumber)
                cy.get('#person_a_plz').type(taxReturnData.personA.postalCode)
                cy.get('#person_a_town').type(taxReturnData.personA.town)
                cy.get(submitBtnSelector).click()

                cy.get('label[for=person_a_has_disability-no]').click()
                cy.get(submitBtnSelector).click()

                cy.get('#telephone_number').type(taxReturnData.telephoneNumber)
                cy.get(submitBtnSelector).click()

                cy.get('label[for=is_user_account_holder]').first().click()
                cy.get('#iban').type(taxReturnData.iban, { delay: 50 })
                cy.get(submitBtnSelector).click()

                // Step 3
                // Do not select any stmind
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
                cy.downloadFile(Cypress.config('baseUrl') + '/download_pdf/print.pdf',
                    'cypress/fixtures/Download', 'print.pdf')
                cy.task('getPdfContent', 'cypress/fixtures/Download/print.pdf').then(content => {
                    //Test if pdf contains 'Ordnungsbegriff'
                    cy.expect(content.text).contains('Ordnungsbegriff')
                  })


                cy.get(submitBtnSelector).click()
                cy.get('body').contains('Herzlichen Glückwunsch!')
            });

            it('for a married couple with deductions', () => {
                // Step 2
                cy.get('label[for=familienstand-1]').click()
                cy.get('#familienstand_date_1').type(taxReturnData.marriedDateDay)
                cy.get('#familienstand_date_2').type(taxReturnData.marriedDateMonth)
                cy.get('#familienstand_date_3').type(taxReturnData.marriedDateYear)
                cy.get('label[for=familienstand_married_lived_separated-no]').click()
                cy.get('label[for=familienstand_confirm_zusammenveranlagung]').first().click()
                cy.get(submitBtnSelector).click()
                cy.get('label[for=steuernummer_exists-yes]').click()
                cy.get('select[id=bundesland]').select('BY')
                cy.get('#steuernummer_1').type(taxReturnData.taxNr1)
                cy.get('#steuernummer_2').type(taxReturnData.taxNr2)
                cy.get('#steuernummer_3').type(taxReturnData.taxNr3)
                cy.get(submitBtnSelector).click()
                cy.get('#person_a_idnr_1').type(taxReturnData.personA.idnr1)
                cy.get('#person_a_idnr_2').type(taxReturnData.personA.idnr2)
                cy.get('#person_a_idnr_3').type(taxReturnData.personA.idnr3)
                cy.get('#person_a_idnr_4').type(taxReturnData.personA.idnr4)
                cy.get('#person_a_dob_1').type(taxReturnData.personA.dobDay)
                cy.get('#person_a_dob_2').type(taxReturnData.personA.dobMonth)
                cy.get('#person_a_dob_3').type(taxReturnData.personA.dobYear)
                cy.get('#person_a_first_name').type(taxReturnData.personA.firstName)
                cy.get('#person_a_last_name').type(taxReturnData.personA.lastName)
                cy.get('#person_a_street').type(taxReturnData.personA.street)
                cy.get('#person_a_street_number').type(taxReturnData.personA.streetNumber)
                cy.get('#person_a_street_number_ext').type(taxReturnData.personA.streetNumberExt)
                cy.get('#person_a_address_ext').type(taxReturnData.personA.addressExt)
                cy.get('#person_a_plz').type(taxReturnData.personA.postalCode)
                cy.get('#person_a_town').type(taxReturnData.personA.town)
                cy.get(submitBtnSelector).click()

                cy.get('label[for=person_a_has_disability-yes]').click()
                cy.get(submitBtnSelector).click()

                cy.get('label[for=person_a_has_pflegegrad-yes]').click()
                cy.get('#person_a_disability_degree').type(taxReturnData.personA.disabilityDegree)
                cy.get('label[for=person_a_has_merkzeichen_bl]').first().click()
                cy.get('label[for=person_a_has_merkzeichen_h]').first().click()
                cy.get(submitBtnSelector).click()

                cy.get('label[for=person_a_requests_pauschbetrag-yes').click()
                cy.get(submitBtnSelector).click()

                cy.get('label[for=person_a_requests_fahrtkostenpauschale-yes').click()
                cy.get(submitBtnSelector).click()

                cy.get('#person_b_idnr_1').type(taxReturnData.personB.idnr1)
                cy.get('#person_b_idnr_2').type(taxReturnData.personB.idnr2)
                cy.get('#person_b_idnr_3').type(taxReturnData.personB.idnr3)
                cy.get('#person_b_idnr_4').type(taxReturnData.personB.idnr4)
                cy.get('#person_b_dob_1').type(taxReturnData.personB.dobDay)
                cy.get('#person_b_dob_2').type(taxReturnData.personB.dobMonth)
                cy.get('#person_b_dob_3').type(taxReturnData.personB.dobYear)
                cy.get('#person_b_first_name').type(taxReturnData.personB.firstName)
                cy.get('#person_b_last_name').type(taxReturnData.personB.lastName)
                cy.get('label[for=person_b_same_address-1]').click()
                cy.get('#person_b_street').type(taxReturnData.personB.street)
                cy.get('#person_b_street_number').type(taxReturnData.personB.streetNumber)
                cy.get('#person_b_plz').type(taxReturnData.personB.postalCode)
                cy.get('#person_b_town').type(taxReturnData.personB.town)
                cy.get('select[id=person_b_religion]').select('ev')
                cy.get(submitBtnSelector).click()

                cy.get('label[for=person_b_has_disability-yes]').click()
                cy.get(submitBtnSelector).click()

                cy.get('label[for=person_b_has_pflegegrad-yes]').click()
                cy.get('#person_b_disability_degree').type(taxReturnData.personA.disabilityDegree)
                cy.get('label[for=person_b_has_merkzeichen_bl]').first().click()
                cy.get('label[for=person_b_has_merkzeichen_h]').first().click()
                cy.get(submitBtnSelector).click()

                cy.get('#person_b_requests_pauschbetrag-yes').click()
                cy.get(submitBtnSelector).click()

                cy.get('label[for=person_b_requests_fahrtkostenpauschale-yes').click()
                cy.get(submitBtnSelector).click()

                // no telephone number
                cy.get(submitBtnSelector).click()

                cy.get('label[for=account_holder-0]').first().click()
                cy.get('#iban').type(taxReturnData.iban, { delay: 50 })
                cy.get(submitBtnSelector).click()

                // Step 3
                cy.get('label[for=stmind_select_vorsorge]').click()
                cy.get('label[for=stmind_select_ausserg_bela]').click()
                cy.get('label[for=stmind_select_handwerker]').click()
                cy.get('label[for=stmind_select_spenden]').click()
                cy.get('label[for=stmind_select_religion]').click()
                cy.get(submitBtnSelector).click()
                cy.get('#stmind_vorsorge_summe').type(taxReturnData.stmind.vorsorge.summe)
                cy.get(submitBtnSelector).click()

                cy.get('#stmind_krankheitskosten_summe').type(taxReturnData.stmind.krankheitskosten.summe)
                cy.get('#stmind_krankheitskosten_anspruch').type(taxReturnData.stmind.krankheitskosten.anspruch)
                cy.get('#stmind_pflegekosten_summe').type(taxReturnData.stmind.pflegekosten.summe)
                cy.get('#stmind_pflegekosten_anspruch').type(taxReturnData.stmind.pflegekosten.anspruch)
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

                cy.get('#stmind_handwerker_entries-div').children().should('have.length', 1)
                cy.get('button[id=stmind_handwerker_entries-add]').click()
                cy.get('#stmind_handwerker_entries-div').children().should('have.length', 2)
                cy.get('#stmind_handwerker_entries-div').children().eq(0).type(taxReturnData.stmind.handwerker.entries[0])
                cy.get('#stmind_handwerker_entries-div').children().eq(1).type(taxReturnData.stmind.handwerker.entries[1])
                cy.get('#stmind_handwerker_summe').type(taxReturnData.stmind.handwerker.summe)
                cy.get('#stmind_handwerker_lohn_etc_summe').type(taxReturnData.stmind.handwerker.lohnEtcSumme)
                cy.get(submitBtnSelector).click()

                cy.get('#stmind_spenden_inland').type(taxReturnData.stmind.spenden.inland)
                cy.get('#stmind_spenden_inland_parteien').type(taxReturnData.stmind.spenden.inlandParteien)
                cy.get(submitBtnSelector).click()

                cy.get('#stmind_religion_paid_summe').type(taxReturnData.stmind.religion.paidSumme)
                cy.get('#stmind_religion_reimbursed_summe').type(taxReturnData.stmind.religion.reimbursedSumme)
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
                cy.get('#idnr_1').should('have.value', '')
                cy.get('#unlock_code_1').should('have.value', '')

                // Clean up
                cy.task('removeDownloadFolder', 'cypress/fixtures')
            });
        });
        // These tests could be split. However, to avoid hitting rate limits, keep it simple, and reduce the run time it is one test.
        it('Submit forms and check different redirects', () => {
            // No relationship set
            // Redirect person_b
            cy.visit('/lotse/step/person_b?link_overview=True')

            // Set relationship single -> Redirect person_b
            // This make no sense at all because of the precondition of person b
            cy.visit('/lotse/step/familienstand')
            cy.get('label[for=familienstand-0]').click()
            cy.get(submitBtnSelector).click()
            cy.visit('/lotse/step/person_a?link_overview=True')

            // Set relationship widowed older -> Redirect person_b
            cy.visit('/lotse/step/familienstand')
            cy.get('label[for=familienstand-2]').click()
            cy.get('#familienstand_date_1').clear().type(older_date_day)
            cy.get('#familienstand_date_2').clear().type(older_date_month)
            cy.get('#familienstand_date_3').clear().type(older_date_year)
            cy.get(submitBtnSelector).click()
            cy.visit('/lotse/step/person_b?link_overview=True')
            cy.location().should((loc) => {
                expect(loc.pathname.toString()).to.contain('/lotse/step/familienstand');
            });

            // Set relationship widowed recent + zusammenveranlagung yes -> No redirect person_b
            cy.visit('/lotse/step/familienstand')
            cy.get('label[for=familienstand-2]').click()
            cy.get('#familienstand_date_1').clear().type(recent_date_day)
            cy.get('#familienstand_date_2').clear().type(recent_date_month)
            cy.get('#familienstand_date_3').clear().type(recent_date_year)
            cy.get('label[for=familienstand_widowed_lived_separated-no]').click()
            cy.get('label[for=familienstand_confirm_zusammenveranlagung]').first().click()
            cy.get(submitBtnSelector).click()
            cy.visit('/lotse/step/person_b?link_overview=True')
            cy.location().should((loc) => {
                expect(loc.pathname.toString()).to.contain('/lotse/step/person_b');
            });

            // Set relationship divorced -> Redirect person_b
            cy.visit('/lotse/step/familienstand')
            cy.get('label[for=familienstand-3]').click()
            cy.get('#familienstand_date_1').clear().type(recent_date_day)
            cy.get('#familienstand_date_2').clear().type(recent_date_month)
            cy.get('#familienstand_date_3').clear().type(recent_date_year)
            cy.get(submitBtnSelector).click()
            cy.visit('/lotse/step/person_b?link_overview=True')
            cy.location().should((loc) => {
                expect(loc.pathname.toString()).to.contain('/lotse/step/familienstand');
            });
            cy.visit('/lotse/step/familienstand')
            cy.get('label[for=familienstand-3]').click()
            cy.get('#familienstand_date_1').clear().type(older_date_day)
            cy.get('#familienstand_date_2').clear().type(older_date_month)
            cy.get('#familienstand_date_3').clear().type(older_date_year)
            cy.get(submitBtnSelector).click()
            cy.visit('/lotse/step/person_b?link_overview=True')
            cy.location().should((loc) => {
                expect(loc.pathname.toString()).to.contain('/lotse/step/familienstand');
            });

            // Set relationship married + separated + zusammenveranlagung-> No redirect person_b
            cy.visit('/lotse/step/familienstand')
            cy.get('label[for=familienstand-1]').click()
            cy.get('#familienstand_date_1').clear().type(taxReturnData.marriedDateDay)
            cy.get('#familienstand_date_2').clear().type(taxReturnData.marriedDateMonth)
            cy.get('#familienstand_date_3').clear().type(taxReturnData.marriedDateYear)
            cy.get('label[for=familienstand_married_lived_separated-yes]').click()
            cy.get('#familienstand_married_lived_separated_since_1').clear().type(one_day_into_the_tax_year_day)
            cy.get('#familienstand_married_lived_separated_since_2').clear().type(one_day_into_the_tax_year_month)
            cy.get('#familienstand_married_lived_separated_since_3').clear().type(one_day_into_the_tax_year_year)
            cy.get('label[for=familienstand_zusammenveranlagung-yes]').click()
            cy.get(submitBtnSelector).click()
            cy.visit('/lotse/step/person_b?link_overview=True')
            cy.location().should((loc) => {
                expect(loc.pathname.toString()).to.contain('/lotse/step/person_b');
            });

            // Set relationship married + separated + no zusammenveranlagung-> Redirect person_b
            cy.visit('/lotse/step/familienstand')
            cy.get('label[for=familienstand-1]').click()
            cy.get('#familienstand_date_1').clear().type(taxReturnData.marriedDateDay)
            cy.get('#familienstand_date_2').clear().type(taxReturnData.marriedDateMonth)
            cy.get('#familienstand_date_3').clear().type(taxReturnData.marriedDateYear)
            cy.get('label[for=familienstand_married_lived_separated-yes]').click()
            cy.get('#familienstand_married_lived_separated_since_1').clear().type(one_day_into_the_tax_year_day)
            cy.get('#familienstand_married_lived_separated_since_2').clear().type(one_day_into_the_tax_year_month)
            cy.get('#familienstand_married_lived_separated_since_3').clear().type(one_day_into_the_tax_year_year)
            cy.get('label[for=familienstand_zusammenveranlagung-no]').click()
            cy.get(submitBtnSelector).click()
            cy.visit('/lotse/step/person_b?link_overview=True')
            cy.location().should((loc) => {
                expect(loc.pathname.toString()).to.contain('/lotse/step/familienstand');
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
