import React from "react";
import { SocialIcon } from "react-social-icons";
import { isMobile } from "react-device-detect";
import styled from "styled-components";
import PropTypes from "prop-types";

const FacebookIcon = styled(SocialIcon)`
  // This is needed for the hover effect on the background when going over the icon
  .social-svg-icon:hover + .social-svg-mask {
    fill: #2f4779 !important;
  }

  .social-svg-mask:hover {
    fill: #2f4779 !important;
  }
`;

const WhatsappIcon = styled(SocialIcon)`
  .social-svg-icon:hover + .social-svg-mask {
    fill: #25c05f !important;
  }

  .social-svg-mask:hover {
    fill: #25c05f !important;
  }
`;

const EmailIcon = styled(SocialIcon)`
  .social-svg-icon:hover + .social-svg-mask {
    fill: #6b6b6d !important;
  }

  .social-svg-mask:hover {
    fill: #6b6b6d !important;
  }
`;

function sendGoal(plausibleDomain, iconName, sourcePage) {
  if (plausibleDomain !== null) {
    window.plausible(`${iconName} icon clicked`, {
      props: { method: sourcePage },
    });
  }
}

export default function ShareIcons({
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
  console.log(`isMobile=${isMobile}`);
  return (
    <div>
      <FacebookIcon
        className="mr-2"
        network="facebook"
        url={facebookFeedUrl}
        target="_blank"
        onClick={() => sendGoal(plausibleDomain, "Facebook", sourcePage)}
      />
      {isMobile && (
        <WhatsappIcon
          className="mr-2"
          network="whatsapp"
          url={whatsappText}
          onClick={() => sendGoal(plausibleDomain, "Whatsapp", sourcePage)}
        />
      )}
      <EmailIcon
        network="email"
        url={mailto}
        onClick={() => sendGoal(plausibleDomain, "Email", sourcePage)}
      />
    </div>
  );
}

ShareIcons.propTypes = {
  promoteUrl: PropTypes.string.isRequired,
  shareText: PropTypes.string.isRequired,
  mailSubject: PropTypes.string.isRequired,
  sourcePage: PropTypes.string.isRequired,
  plausibleDomain: PropTypes.string,
};

ShareIcons.defaultProps = {
  plausibleDomain: null,
};
