/**
 * This global helper function adds a plausible goal with a given name and props. Only if a plausible domain is passed,
 * the goal will be added.
 * @param plausibleDomain - the name of the plausible domain, extracted from the env config.
 * @param name - the goal name.
 * @param props - the variable extra information for the goal.
 */
export default function addPlausibleGoal(plausibleDomain, name, props) {
  if (plausibleDomain !== null) {
    window.plausible(name, props);
  }
}

export function toggleManually(event, moveToNewPage, section, elementIndex) {
  event.preventDefault();
  if (moveToNewPage) {
    window.location = `/hilfebereich#${section}-${elementIndex}`;
  } else {
    window.location = `#${section}`;
    document.getElementById(`button-${section}-${elementIndex}`).click();
  }
}
