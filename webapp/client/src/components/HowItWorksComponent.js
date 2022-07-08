import styled from "styled-components";
import OneIcon from "../assets/icons/Icon-1.svg";

const Box = styled.div`
  /* background-color: var(--beige-200); */
  /* padding-top: var(--spacing-09); */
  /* margin-top: var(--spacing-10); */
  border-left: 2px solid black;
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
  left: -3%;
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

export const Headline3 = styled.h3`
  max-width: 300px;
`;

export default function HowItWorksComponent() {
  return (
    <Box>
      <InnerBox>
        <Icon src={OneIcon} alt="icon" />
        <Headline3>
          Finden Sie heraus, ob Sie den Steuerlotsen nutzen können
        </Headline3>
        <Figure className="info-box__figure">
          <picture>
            <img
              src="../images/step1.png"
              alt="Tablets mit Webapp des Steuerlotsen"
            />
          </picture>
        </Figure>
      </InnerBox>
    </Box>
  );
}

HowItWorksComponent.defaultProps = {
  boxHeadline: null,
  boxText: null,
  anchor: {
    url: null,
    text: null,
  },
};
