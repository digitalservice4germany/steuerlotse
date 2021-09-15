/// <reference types="cypress" />
// ***********************************************************
// This example plugins/index.js can be used to load plugins
//
// You can change the location of this file or turn off loading
// the plugins file with the 'pluginsFile' configuration option.
//
// You can read more here:
// https://on.cypress.io/plugins-guide
// ***********************************************************

// This function is called when a project is opened or re-opened (e.g. due to
// the project's config changing)

/**
 * @type {Cypress.PluginConfig}
 */
// eslint-disable-next-line no-unused-vars
module.exports = (on, config) => {
  // `on` is used to hook into various events Cypress emits
  // `config` is the resolved Cypress config
}
const { downloadFile } = require('cypress-downloadfile/lib/addPlugin');
const fs = require('fs');
const pdf  = require('pdf-parse');

const parsePdf = async (pdfName) => {
  let dataBuffer = fs.readFileSync(pdfName);
  return await pdf(dataBuffer);
}

module.exports = (on, config) => {
  on('task', { downloadFile })
  on('task', {getPdfContent (pdfName) { return parsePdf(pdfName) } } );
  on('task', {removeDownloadFolder (folderToRemove) { 
	return new Promise((resolve, reject) => {
      fs.rmdir(folderToRemove, { maxRetries: 5, recursive: true }, (err) => {
        if (err) {
          console.error(err)
          return reject(err)
        }
        resolve(null)
      })
    })  }});
}
