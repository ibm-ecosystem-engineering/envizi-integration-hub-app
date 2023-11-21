import React, { Component } from 'react';

import 'bootstrap/dist/css/bootstrap.min.css';
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import Breadcrumb from 'react-bootstrap/Breadcrumb';
import Card from 'react-bootstrap/Card';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faHome, faUser, faCog, faEnvelope } from '@fortawesome/free-solid-svg-icons';
import './App.css';
import Main from "./components/main/main";
import { Link } from 'react-router-dom';

import Form from 'react-bootstrap/Form';

import Image from 'react-bootstrap/Image';

import { BrowserRouter as Router, Switch, Route,Routes } from 'react-router-dom';
import About from './pages/About';
import Contact from './pages/Contact';

import HomeMain from "./components/home/home";
import TurboMain from "./components/turbo/turbo";
import ConfigMain from "./components/config/config";
import SevOneMain from './components/sevone/sevone';
import enviziIcon from './images/envizi.svg'; // Import the image file
import enviziGreyIcon from './images/envizi_grey.svg'; // Import the image file
import userIcon from './images/user.png'; // Import the image file

class App extends Component {

  constructor(props) {
    super(props);
    this.state = {
      currentPage: 'home',
    };
  }

  changePage = (page) => {
    this.setState({ currentPage: page });
  };

  render() {
    const { currentPage } = this.state;
    const PageComponent = {
      home: HomeMain,
      contact: Contact,
      about: About,
      turbo: TurboMain,
      config: ConfigMain,
      tririga: HomeMain,
      maximo: HomeMain,
      pa: HomeMain,
      sevone: SevOneMain,

    }[currentPage];

  return (
    <div className="App">
      <Navbar fixed="top" className='HeaderClass'>
          <Navbar.Brand>
          &nbsp;&nbsp;<Image src={enviziIcon} height="35" className="HeaderImage" alt="Logo" />
          </Navbar.Brand>
          <Navbar.Brand className='HeaderTitle'>
            Integration Hub
          </Navbar.Brand>
          <Navbar.Collapse className="justify-content-end">
            <Navbar.Text>
              <span className="HeaderRightMenu">Welcome Guest </span> &nbsp; &nbsp;
              <Image src={userIcon} width="30" height="30" roundedCircle />&nbsp; &nbsp;
            </Navbar.Text>
          </Navbar.Collapse>
      </Navbar>
      <div className='SubHeaderClass'>
        <Navbar>
          <div class="container-lm">
            <Nav className="me-auto">
              <Nav.Link href="#turbo" active={currentPage === 'home'} onClick={() => this.changePage('home')}>Home</Nav.Link>
              <Nav.Link href="#turbo" active={currentPage === 'turbo'} onClick={() => this.changePage('turbo')}>Turbonomic</Nav.Link>
              <Nav.Link href="#tririga" active={currentPage === 'tririga'} onClick={() => this.changePage('tririga')}>Tririga</Nav.Link>
              {/* <Nav.Link href="#maximo" active={currentPage === 'maximo'} onClick={() => this.changePage('maximo')}>Maximo</Nav.Link> */}
              {/* <Nav.Link href="#pa" active={currentPage === 'pa'} onClick={() => this.changePage('pa')}>Planning and Analystics</Nav.Link>
              <Nav.Link href="#sevone" active={currentPage === 'sevone'} onClick={() => this.changePage('sevone')}>SevOne</Nav.Link> */}
              <Nav.Link href="#config" active={currentPage === 'config'} onClick={() => this.changePage('config')}>Config</Nav.Link>
            </Nav>
          </div>
        </Navbar>
      </div>
      <div className="MainClass d-flex justify-content-center">
      <PageComponent />
      </div>

      <div class="footer">
        <Row class=".d-flex">
          <Col md="2">
            © Copyright.  All rights reserved.
          </Col>
          <Col md="3" > 
          </Col>
          <Col md="2"> 
          <a target="_blank" className="fontSize12" href="https://www.ibm.com/products/envizi">Envizi</a>
          </Col>
          <Col md="3" > 
          </Col>
          <Col md="2">
            Engineered By  <Image src={enviziGreyIcon}  height="25" />&nbsp; &nbsp;
          </Col>
        </Row>
      </div>
    </div>
  );
}

}

export default App;
