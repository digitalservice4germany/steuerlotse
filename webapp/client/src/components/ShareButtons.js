import React from "react";
import { isMobile } from "react-device-detect";
import styled from "styled-components";
import PropTypes from "prop-types";
import addPlausibleGoal from "../lib/helpers";
import ButtonAnchor from "./ButtonAnchor";

const ButtonGroup = styled.div`
  display: flex;
  flex-direction: column;
  align-items: flex-start;

  a,
  button {
    margin-right: 8px;
    margin-bottom: 8px;
  }

  @media (min-width: 1024px) {
    display: block;
  }
`;
const FacebookButton = styled(ButtonAnchor)`
  background-color: var(--facebook-color);

  &:hover {
    background-color: var(--facebook-hover-color);
    text-decoration: none;

    &:active {
      background-color: var(--facebook-active-hover-color);
    }
  }
`;
const WhatsappButton = styled(ButtonAnchor)`
  background-color: var(--whatsapp-color);

  &:hover {
    background-color: var(--whatsapp-hover-color);
    text-decoration: none;

    &:active {
      background-color: var(--whatsapp-active-hover-color);
    }
  }
`;
const MailButton = styled(ButtonAnchor)`
  background-color: var(--email-color);

  &:hover {
    background-color: var(--email-hover-color);
    text-decoration: none;

    &:active {
      background-color: var(--email-active-hover-color);
    }
  }
`;

export default function ShareButtons({
  promoteUrl,
  shareText,
  mailSubject,
  sourcePage,
  plausibleDomain,
}) {
  const facebookFeedUrl = `https://www.facebook.com/sharer/sharer.php?u=${promoteUrl}&quote=${shareText}`;
  const mailto = `mailto:?subject= ${encodeURIComponent(
    mailSubject
  )}&body=${encodeURIComponent(shareText)}`;
  const whatsappText = `https://wa.me?text=${shareText}`;
  const onClickHandler = () => {
    navigator.clipboard.writeText(window.location.href);
    addPlausibleGoal(plausibleDomain, "Link copied clicked", {
      method: sourcePage,
    });
  };
  const { Text } = ButtonAnchor;

  return (
    <ButtonGroup>
      <FacebookButton
        buttonStyle="narrow"
        url={facebookFeedUrl}
        external
        onClick={() =>
          addPlausibleGoal(plausibleDomain, "Facebook icon clicked", {
            method: sourcePage,
          })
        }
      >
        <Text>Auf Facebook teilen</Text>
      </FacebookButton>
      {isMobile && (
        <WhatsappButton
          buttonStyle="narrow"
          url={whatsappText}
          onClick={() =>
            addPlausibleGoal(plausibleDomain, "Whatsapp icon clicked", {
              method: sourcePage,
            })
          }
        >
          <Text>In Whatsapp senden</Text>
        </WhatsappButton>
      )}
      <MailButton
        buttonStyle="narrow"
        url={mailto}
        onClick={() =>
          addPlausibleGoal(plausibleDomain, "Email icon clicked", {
            method: sourcePage,
          })
        }
      >
        <Text>E-Mail schreiben</Text>
      </MailButton>
      <ButtonAnchor
        buttonStyle="narrow"
        variant="outline"
        onClick={onClickHandler}
      >
        <Text>Link kopieren</Text>
      </ButtonAnchor>
    </ButtonGroup>
  );
}

ShareButtons.propTypes = {
  promoteUrl: PropTypes.string.isRequired,
  shareText: PropTypes.string.isRequired,
  mailSubject: PropTypes.string.isRequired,
  sourcePage: PropTypes.string.isRequired,
  plausibleDomain: PropTypes.string,
};

ShareButtons.defaultProps = {
  plausibleDomain: null,
};
