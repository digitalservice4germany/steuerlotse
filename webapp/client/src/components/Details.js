import React, { useState } from "react";
import PropTypes from "prop-types";
import styled from "styled-components";
import Collapse from "react-bootstrap/Collapse";

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
    display: inline-block;
    margin: 0 var(--spacing-01);
    height: var(--lineheight-default);
    font-size: var(--text-medium);
    font-weight: var(--font-bold);
  }

  @media (max-width: 1024px) {
    &.details-card .card-header span {
      font-size: var(--text-base);
    }
  }

  &.details-card .card-header button {
    padding: 0;
    text-align: left;
    color: var(--text-color);
    background: inherit;
    border: 0;
    outline: none;
    box-shadow: none;
  }

  &.details-card .card-header [aria-expanded="false"] {
    color: var(--link-color);
  }

  &.details-card .card-header [aria-expanded="false"] :hover {
    color: var(--link-hover-color);
  }

  &.details-card .card-header button:focus span {
    color: var(--focus-text-color);
    background: var(--focus-color);
  }

  &.details-card .details-icon {
    width: 12px;
    min-width: 12px;
    height: var(--lineheight-default);
    padding: 0;
  }

  &.details-card [aria-expanded="false"]:hover .details-icon {
    background: url(${rightArrowHover}) no-repeat left;
  }

  &.details-card [aria-expanded="false"] button:focus .details-icon {
    background: url(${rightArrowFocus}) no-repeat left;
  }

  &.details-card [aria-expanded="false"] .details-icon {
    background: url(${rightArrow}) no-repeat left;
  }

  &.details-card [aria-expanded="true"] .details-icon {
    background: url(${downArrow}) no-repeat left;
  }

  &.details-card .card-body {
    border: 0;
    padding: 0 0 var(--spacing-04) 0;
  }

  &.details-card .card-body .block-quote-line {
    width: 2px;
    min-width: 2px;
    margin: 0 var(--spacing-03) 0 5px;
    background-color: var(--border-color);
  }

  &.details-card .details-content {
    padding: var(--spacing-02) 1em var(--spacing-02) 0;
  }

  &.details-card .details-content :last-child {
    margin-bottom: 0;
  }
`;

function Details({ children, title, detailsId }) {
  const [open, setOpen] = useState(false);
  const toggle = () => setOpen(!open);

  const detailsBodyId = `details-body-${detailsId}`;
  const headingId = `heading-${detailsId}`;

  return (
    <DetailsCard className="details-card ml-0 pl-0">
      <div className="card">
        <div className="card-header unstyled-card-header d-sm-flex justify-content-between align-items-center cursor-pointer mb-0">
          <button
            onClick={toggle}
            className="w-100"
            type="button"
            aria-expanded={open}
            aria-controls={detailsBodyId}
          >
            <div id={headingId} className="row details-row">
              <i className="details-icon" />
              <span className="mb-0">{title}</span>
            </div>
          </button>
        </div>
        <Collapse in={open}>
          <div
            id={detailsBodyId}
            aria-labelledby={headingId}
            className="card-body pt-0"
          >
            <div className="row details-row">
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
        </Collapse>
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
