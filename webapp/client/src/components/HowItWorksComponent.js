import PropTypes from "prop-types";
import styled from "styled-components";

const Box = styled.div`
  /* background-color: var(--beige-200); */
  /* padding-top: var(--spacing-09); */
  /* margin-top: var(--spacing-10); */
  border-left: ${(props) =>
    props.border ? "none" : "2px solid var(--beige-500)"};
`;

const InnerBox = styled.div`
  padding-left: var(--spacing-09);
  display: flex;
  position: relative;
  justify-content: space-between;
  padding-bottom: 100px;

  @media (max-width: 1024px) {
    padding-left: var(--spacing-09);
  }

  /* @media (max-width: 767px) {
    flex-direction: column;
    padding-left: var(--spacing-03);
    padding-right: var(--spacing-03);
  } */
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
  align-self: end;
  width: 100%;
  max-width: 476px;
  border-radius: 50px;
  box-shadow: 20px 20px 50px rgba(0, 0, 0, 0.35);

  img {
    width: 100%;
    height: auto;
    object-fit: contain;
  }
`;

const Headline3 = styled.h3`
  font-size: var(--text-2xl);
  margin-bottom: var(--spacing-06);
`;

const Column = styled.div`
  margin-right: 3rem;
  max-width: 253px;

  @media (max-width: 768px) {
    margin-right: 2rem;
  }
`;

const InnerContent = styled.div`
  display: flex;

  @media (max-width: 1279px) {
    /* flex-direction: column;
    justify-content: start; */
    display: flex;
    flex-wrap: wrap;
  }

  @media (max-width: 1024px) {
    flex-direction: column;
    justify-content: start;
  }

  @media (max-width: 768px) {
    flex-direction: row;
    flex-wrap: nowrap;
    margin-right: var(--spacing-06);
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
  icon: PropTypes.string,
  image: PropTypes.string,
  variant: PropTypes.string,
};

HowItWorksComponent.defaultProps = {
  heading: null,
  text: null,
  icon: null,
  image: null,
  variant: null,
};
