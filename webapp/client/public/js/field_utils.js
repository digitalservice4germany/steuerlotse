"use strict";
function assignAssociatedContent(selector='label, .example-input, .additional-input-content, .invalid-feedback') {
  let associated_content = document.querySelectorAll(selector);
    for (let i = 0; i < associated_content.length; i++) {
      if (associated_content[i].getAttribute('for') != '') {
         let elementWithAssociatedContent = document.getElementById(associated_content[i].getAttribute('for'));
         if (elementWithAssociatedContent){
          if (elementWithAssociatedContent.associatedContent){
            elementWithAssociatedContent.associatedContent.push(associated_content[i]);
          } else {
            elementWithAssociatedContent.associatedContent = [associated_content[i]];
          }
         }
      }
    }
}
function deleteSelectOptions(selectInput, defaultOptionText) {
  while (selectInput.options.length) {
    selectInput.remove(0);
    }
  selectInput.options.add(new Option(defaultOptionText, ""));
}

function deleteInput(input){
  if (input.type == "checkbox"){
    input.checked = false;
  } else {
    input.value = '';
  }
}
function hideInput(input) {
  input.style.setProperty("display", "none", "important");
  if (input.associatedContent) {
    input.associatedContent.forEach((associatedElem) =>{
      associatedElem.oldDisplayStyle = "inline-block";
      associatedElem.style.setProperty("display", "none", "important");

    });
  }
}
function hideRequiredInput(input) {
  hideInput(input);
  input.removeAttribute('required');
}
function showInput(input, required=true) {
  input.style.removeProperty('display')
  if (input.associatedContent){
    input.associatedContent.forEach((associatedElem) =>{
      associatedElem.style.removeProperty('display');
    });
  }
}
function showRequiredInput(input) {
  showInput(input);
  input.required = true;
}
