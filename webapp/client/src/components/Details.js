// TODO: get rid of bootstrap (or use react-bootstrap, reactstrap, etc.)
import "bootstrap"; // For the data-toggle=collapse functionality
import React from "react";
import PropTypes from "prop-types";
import styled from "styled-components";

import downArrow from "../assets/icons/details_arrow_down.svg";
import rightArrow from "../assets/icons/details_arrow_right.svg";
import rightArrowHover from "../assets/icons/details_arrow_right_hover.svg";
import rightArrowFocus from "../assets/icons/details_arrow_right_focus.svg";

const DetailsCard = styled.div`
  &.details-card {
    display: block;
    width: 100%;
    overflow: auto;
  }

  &.details-card .card {
    border: 0;
    border-radius: 0;
    background: inherit;
  }

  &.details-card .card-header {
    border: 0;
    background: inherit;
    align-items: start;
    flex-wrap: nowrap;
  }

  .details-row {
    flex-wrap: nowrap;
    margin: 0;
  }

  &.details-card .card-header span {
    color: var(--text-color);
    font-size: var(--text-medium);
    font-weight: var(--font-bold);
  }

  @media (max-width: 1024px) {
    &.details-card .card-header span {
      font-size: var(--text-base);
    }
  }

  &.details-card .card-header button {
    text-align: left;
    color: var(--text-color);
    background: inherit;
    border: 0;
    outline: none;
    box-shadow: none;
  }

  &.details-card .card-header .collapsed span {
    color: var(--link-color);
  }

  &.details-card .card-header .collapsed span:hover {
    color: var(--link-hover-color);
  }

  &.details-card .card-header button:focus span {
    color: var(--focus-text-color);

    background: var(--focus-color);

    outline: none;
    box-shadow: none;
    border: 0;
  }

  &.details-card .card-header .details-icon {
    width: 14px;
    min-width: 14px;
    height: var(--lineheight-default);
    padding: 0;
    margin-top: 0.375rem;
    background: url(${downArrow}) no-repeat left;
  }

  &.details-card .card-header .collapsed:hover .details-icon {
    background: url(${rightArrowHover}) no-repeat left;
  }

  &.details-card .card-header .collapsed button:focus .details-icon {
    background: url(${rightArrowFocus}) no-repeat left;
  }

  &.details-card .card-header .collapsed .details-icon {
    background: url(${rightArrow}) no-repeat left;
  }

  &.details-card .card-body {
    border: 0;
  }

  &.details-card .details-content {
    padding: 1em 1em 0 0;
  }

  &.card-body-less-padding {
    padding: 1em 1em var(--spacing-01) var(--spacing-01);
  }

  &.details-card .card-body {
    padding: 0 0 var(--spacing-04) 0;
  }

  &.details-card .card-body .block-quote-line {
    width: 2px;
    min-width: 2px;
    margin: 0 var(--spacing-03) 0 5px;
    background-color: var(--border-color);
  }

  &.details-card .card-header button:hover {
    color: var(--link-hover-color);
    outline: none;
  }

  &.details-card .card-header:not(.collapsed) .control-show-more {
    /* We need to still show it to keep focus on the element */
    height: 1px;
    width: 1px;
    min-width: 1px;
    background-color: inherit;
    padding: 0;
    margin: 0;
    overflow: hidden;
    position: absolute;
  }

  &.details-card .card-header.collapsed .control-show-less {
    /* We need to still show it to keep focus on the element */
    height: 1px;
    width: 1px;
    min-width: 1px;
    background-color: inherit;
    padding: 0;
    margin: 0;
    overflow: hidden;
    position: absolute;
  }
`;

function Details({ children, title, detailsId }) {
  const outerDivId = `details-${detailsId}`;
  const detailsBodyId = `details-body-${detailsId}`;
  const headingId = `heading-${detailsId}`;
  return (
    <DetailsCard id={outerDivId} className="details-card ml-0 pl-0">
      <div className="card">
        <div className="card-header unstyled-card-header d-sm-flex justify-content-between align-items-center cursor-pointer mb-0">
          <div
            className="collapsed w-100"
            id={headingId}
            data-toggle="collapse"
            data-target={`#${detailsBodyId}`}
            role="button"
            aria-expanded="false"
            aria-controls={detailsBodyId}
          >
            <div className="row details-row">
              <button
                className="btn details-icon control-show-more"
                type="button"
                tabIndex="-1"
                aria-hidden="true"
              />
              <button
                className="btn details-icon control-show-less"
                type="button"
                tabIndex="-1"
                aria-hidden="true"
              />
              <button className="btn" type="button">
                <span className="mb-0">{title}</span>
              </button>
            </div>
          </div>
        </div>
        <div
          id={detailsBodyId}
          className="collapse"
          aria-labelledby={headingId}
          data-parent={`#${outerDivId}`}
        >
          <div className="card-body container pt-0">
            <div className="details-row row">
              <div className="block-quote-line" />
              <div className="details-content">
                {children.paragraphs.map((paragraph, index) => (
                  // There is no natural key and the list is completely static, so using the index is fine.
                  // eslint-disable-next-line
                  <p key={index}>{paragraph}</p>
                ))}
                {children.listItems && (
                  <ul>
                    {children.listItems.map((listItem, index) => (
                      // There is no natural key and the list is completely static, so using the index is fine.
                      // eslint-disable-next-line
                      <li key={index} className="mb-2">
                        {listItem}
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </DetailsCard>
  );
}

Details.propTypes = {
  children: PropTypes.exact({
    paragraphs: PropTypes.arrayOf(PropTypes.node),
    listItems: PropTypes.arrayOf(PropTypes.node),
  }).isRequired,
  title: PropTypes.string.isRequired,
  detailsId: PropTypes.string.isRequired,
};

export default Details;
