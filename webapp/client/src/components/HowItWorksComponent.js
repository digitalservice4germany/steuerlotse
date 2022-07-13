import PropTypes from "prop-types";
import styled from "styled-components";

const Box = styled.div`
  border-left: ${(props) =>
    props.border ? "none" : "2px solid var(--beige-500)"};
`;

const InnerBox = styled.div`
  padding-left: var(--spacing-09);
  display: flex;
  position: relative;
  justify-content: space-between;
  padding-bottom: 100px;
`;

const Icon = styled.img`
  position: absolute;
  top: 0;
  left: -26.5px;
  border-radius: 100%;
  height: 50px;
  width: 50px;
`;

const Figure = styled.figure`
  width: 100%;
  max-width: 476px;
  border-radius: 50px;
  box-shadow: 20px 20px 50px rgba(0, 0, 0, 0.35);

  @media (max-width: 768px) {
    max-width: 180px;
  }
  img {
    width: 100%;
    height: auto;
    object-fit: contain;
  }
`;

const Headline3 = styled.h3`
  font-size: var(--text-2xl);
  margin-bottom: var(--spacing-06);

  @media (max-width: 768px) {
    font-size: var(--text-medium-big);
  }
`;

const Column = styled.div`
  margin-right: 3rem;
  max-width: 253px;

  @media (max-width: 768px) {
    margin-right: 2rem;
    max-width: 200px;
  }

  @media (max-width: 575px) {
    margin-right: 0;
  }
`;

const InnerContent = styled.div`
  display: flex;
  flex-wrap: wrap;

  @media (max-width: 768px) {
    margin-right: var(--spacing-06);
  }

  @media (max-width: 575px) {
    justify-content: start;
  }
`;

export default function HowItWorksComponent({
  heading,
  text,
  icon,
  image,
  variant,
}) {
  return (
    <Box border={variant}>
      <InnerBox>
        <Icon src={icon.iconSrc} alt={icon.altText} />
        <InnerContent>
          <Column>
            <Headline3>{heading}</Headline3>
            {text && <p>{text}</p>}
          </Column>
          <Figure className="info-box__figure">
            <picture>
              <source media="(min-width: 769px)" srcSet={image.srcSetDesktop} />
              <source media="(min-width: 320px)" srcSet={image.srcSetMobile} />
              <img src={image.src} alt={image.alt} srcSet={image.srcSet} />
            </picture>
          </Figure>
        </InnerContent>
      </InnerBox>
    </Box>
  );
}

HowItWorksComponent.propTypes = {
  heading: PropTypes.string,
  text: PropTypes.string,
  icon: PropTypes.shape({
    iconSrc: PropTypes.string,
    altText: PropTypes.string,
  }),
  image: PropTypes.shape({
    src: PropTypes.string,
    srcSet: PropTypes.string,
    srcSetDesktop: PropTypes.string,
    srcSetMobile: PropTypes.string,
    alt: PropTypes.string,
  }),
  variant: PropTypes.string,
};

HowItWorksComponent.defaultProps = {
  heading: null,
  text: null,
  icon: null,
  image: null,
  variant: null,
};
