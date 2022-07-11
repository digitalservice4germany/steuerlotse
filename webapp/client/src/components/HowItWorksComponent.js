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
  /* padding-right: var(--spacing-06); */
  /* margin: 0 auto; */
  /* max-width: var(--pages-max-width); */
  display: flex;
  position: relative;
  justify-content: space-between;
  padding-bottom: 100px;
  /* background-color: red; */

  @media (max-width: 1024px) {
    padding-left: var(--spacing-06);
    padding-right: var(--spacing-06);
  }

  @media (max-width: 767px) {
    flex-direction: column;
    padding-left: var(--spacing-03);
    padding-right: var(--spacing-03);
  }
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
  /* margin: 0; */
  align-self: end;
  width: 100%;
  img {
    width: 100%;
    height: auto;
    object-fit: contain;
  }

  @media (max-width: 767px) {
    align-self: center;
  }
`;

const Headline3 = styled.h3`
  max-width: 300px;
`;

const Column = styled.div`
  /* background-color: red; */
  width: 60%;
  margin-right: 3rem;
`;

export default function HowItWorksComponent({
  heading,
  text,
  icon,
  image,
  borderVariant,
}) {
  return (
    <Box border={borderVariant}>
      <InnerBox>
        <Icon src={icon.iconSrc} alt={icon.altText} />
        <Column>
          <Headline3>{heading}</Headline3>
          {text && <p>{text}</p>}
        </Column>
        <Figure className="info-box__figure">
          <picture>
            <source media="(min-width: 1024px)" srcSet={image.srcSetDesktop} />
            <source media="(min-width: 320px)" srcSet={image.srcSetMobile} />
            <img src={image.src} alt={image.alt} srcSet={image.srcSet} />
          </picture>
        </Figure>
      </InnerBox>
    </Box>
  );
}

HowItWorksComponent.propTypes = {
  heading: PropTypes.string,
  text: PropTypes.string,
  icon: PropTypes.string,
  image: PropTypes.string,
  borderVariant: PropTypes.string,
};

HowItWorksComponent.defaultProps = {
  heading: null,
  text: null,
  icon: null,
  image: null,
  borderVariant: null,
};
