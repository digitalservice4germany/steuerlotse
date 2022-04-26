import React, { useState } from "react";
import PropTypes from "prop-types";
import styled from "styled-components";
import { Accordion, Card } from "react-bootstrap";
import plusIcon from "../assets/icons/plus.svg";
import minusIcon from "../assets/icons/minus.svg";

const CardElement = styled.div`
  border: 0;
  border-bottom: 1px solid var(--link-underline-color) !important;
  border-radius: 0;
  background: inherit;
  padding-bottom: 0.75rem;
`;

const CardHeader = styled.div`
  padding: 0.75rem 0;
  text-align: left;
  color: var(--text-color);
  background: inherit;
  border: 0;
`;

const CardHeaderElement = styled.div`
  text-align: left;
  color: var(--text-color);
  background: inherit;
  border: 0;
`;

const ExpandButton = styled.button`
  border: 0;
  background: inherit;
`;

const CardBody = styled.div`
  border: 0;
  padding: 1em 1em var(--spacing-01) var(--spacing-01);
`;

const CardHeaderSpan = styled.span`
  font-size: var(--text-medium);
  font-family: var(--font-bold);
  display: inline;
`;

export default function AccordionComponent({ title, intro, items }) {
  const [toggle, setToggle] = useState();

  return (
    <>
      {title.length > 0 && <h2 className="mt-5">{title}</h2>}
      {intro.length > 0 && <p className="mt-3 pb-2">{intro}</p>}
      <Accordion>
        {items.map((item, index) => [
          <Card key={`card-${index}`} as={CardElement} className="mt-2">
            <Card.Header as={CardHeader} className="d-sm-flex collapsed w-100">
              <Accordion.Toggle
                as={CardHeaderElement}
                className="justify-content-between row w-100"
                variant="link"
                eventKey={`${index}`}
                onClick={() => {
                  if (toggle === index) setToggle(-1);
                  else setToggle(index);
                }}
              >
                <ExpandButton className="col text-left">
                  <CardHeaderSpan>{item.title}</CardHeaderSpan>
                </ExpandButton>
                <ExpandButton className="col-1">
                  {toggle === index ? (
                    <img src={minusIcon} alt="collapse" />
                  ) : (
                    <img src={plusIcon} alt="expand" />
                  )}
                </ExpandButton>
              </Accordion.Toggle>
            </Card.Header>

            <Accordion.Collapse eventKey={`${index}`}>
              <Card.Body as={CardBody}>{item.detail}</Card.Body>
            </Accordion.Collapse>
          </Card>,
        ])}
      </Accordion>
    </>
  );
}

AccordionComponent.propTypes = {
  title: PropTypes.string,
  intro: PropTypes.string,
  items: PropTypes.arrayOf(
    PropTypes.exact({
      title: PropTypes.string,
      detail: PropTypes.oneOfType([PropTypes.string, PropTypes.element]),
    })
  ).isRequired,
};

AccordionComponent.defaultProps = {
  title: "",
  intro: "",
};
