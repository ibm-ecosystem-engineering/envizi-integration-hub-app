import React, { Component } from 'react';

import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Container from "react-bootstrap/Container";
import Image from 'react-bootstrap/Image';

import './home.css'; // Import the CSS file for styling
import greenIcon from '../../images/green.jpg'; // Import the image file
import archImage from '../../images/arch.png'; // Import the image file

class HomeMain extends Component {

  render() {
    return (
      <div>
        <Container>
        <Row>
            <Col >
              <div className='mySectionTitle'>Welcome to Envizi Integration Hub !</div>
            </Col>
        </Row>
        <Row>
            <Col >
              <div className='mySectionTitle2'>Envizi Integration Hub Connects Envizi with external systems such as Turbonomic and more</div>
            </Col>
        </Row>
          <Row>
          <Col class="align-middle">
              <div className='mySectionTitle21'><Image src={archImage} height="270" alt="Logo" /></div>
            </Col>
            <Col>
              <div className='mySectionText'>Envizi Integration Hub facilitates the integration of data from various external systems into the IBM Envizi ESG Suite.</div>

              <div className='mySectionText'>It connects to external systems, such as Turbonomic, retrieves emissions data, converts this data into the Universal Account Setup and Data Loading format (UDC), and then dispatches it to an S3 bucket configured within the IBM Envizi ESG Suite.</div>

              <div className='mySectionText'>Configuration settings are accessible through the Config menu.</div>

              <div className='mySectionText'>This Integration Hub can be expanded to include integration with numerous other external systems that need to interface with the IBM Envizi ESG Suite.</div>
            </Col>
          </Row>
        </Container>
      </div>
    );
  }
}
export default HomeMain;
