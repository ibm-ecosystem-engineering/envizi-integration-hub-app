import React, { Component } from 'react';

import axios from 'axios';
import Spinner from 'react-bootstrap/Spinner';

import Form from "react-bootstrap/Form";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Button from "react-bootstrap/Button";
import Image from "react-bootstrap/Image";
import Collapse from "react-bootstrap/Collapse";
import Container from "react-bootstrap/Container";
import '../common.css'; // Import the CSS file for styling
import './turbo.css'; // Import the CSS file for styling
import locationJsonData from "../../data/0006-Locations.json";
import accountsJsonData from "../../data/0049-Accounts.json";

import DataTable from '../../custom/DataTable/DataTable';

import Main from "../main/main";

import { useState } from 'react'

class TurboMain extends Component {

  constructor() {
    super();
    this.state = {
      loading: true,
      configData: null,
      locationData: [],
      accountsData: [],
    }
  }

  getStartDateForDisplay() {
    var returnValue = ""
    if (this.state.configData) 
      if ("turbo" in this.state.configData)
        if ("parameters" in this.state.configData.turbo)
          if ("start_date" in this.state.configData.turbo.parameters)
              returnValue = this.state.configData?.turbo.parameters.start_date

    return returnValue;
  }

  getEndDateForDisplay() {
    var returnValue = ""
    if (this.state.configData) 
      if ("turbo" in this.state.configData)
        if ("parameters" in this.state.configData.turbo)
          if ("end_date" in this.state.configData.turbo.parameters)
              returnValue = this.state.configData?.turbo.parameters.end_date

    return returnValue;
  }

  handleLoad() {
    const headers = {
      'Authorization': 'Bearer xxxxx',
      'Access-Control-Allow-Origin': '*',
    };

    // var myURL = "http://localhost:3001";
    var myURL = "";
    console.log("myURL -->" + myURL);

    axios.post(myURL + '/api/config/load', {}, { headers })
      .then(response => {
        this.setState((prevData) => {
          const newData = { ...prevData }
          newData.configData = response.data;
          newData.loading = false;
          newData.locationData = [];
          newData.accountsData = [];
          return newData
        })
      })
      .catch(error => {
        console.log(error);
        this.setState((prevData) => {
          const newData = { ...prevData }
          newData.configData = {}
          newData.loading = false;
          return newData
        })
      })
  }

  componentDidMount() {
    this.handleLoad()
  }
  handleInputChange = (event, section1, section2, field) => {
    const { value } = event.target;
    this.setState((prevData) => {
      const newData = { ...prevData }
      newData.configData[section1][section2][field] = value
      return newData
    })

  }
  handleCommon = (event, myAPI) => {
    event.preventDefault();

    this.setState((prevData) => {
      const newData = { ...prevData }
      newData.loading = true;
      return newData
    })

    const headers = {
      'Authorization': 'Bearer xxxxx',
      'Access-Control-Allow-Origin': '*',
    };

    // var myURL = "http://localhost:3001";
    var myURL = "";
    console.log("myURL -->" + myURL);

    axios.post(myURL + myAPI, this.state.configData, { headers })
      .then(response => {
        console.log("Output of the API Call ---> " + response.data);
        this.setState((prevData) => {
          const newData = { ...prevData }
          newData.configData = response.data.inputPayload;
          newData.locationData = response.data.locationData;
          newData.accountsData = response.data.accountsData;
          newData.loading = false;
          return newData
        })
      })
      .catch(error => {
        console.log(error);
        this.setState((prevData) => {
          const newData = { ...prevData }
          newData.loading = false;
          return newData
        })
      })
  }


  handleIngest = (event) => {
    return this.handleCommon(event, '/api/turbo/queryForIngest')
  }
  handleView = (event) => {
    return this.handleCommon(event, '/api/turbo/queryForView')
  }

  render() {

    return (
      <div style={{ overflowY: "auto", width: "100%", height: "80%", background: "white" }}>
        <Container>
          <Row>
            <Col className="section-page">
              <Container>
                <Row>
                  <Col >
                    <div className="section-heading-page">Turbonomic</div>
                  </Col>
                </Row>
                <Row>
                  <Col ><div className="section-title2">Integrate your Turbonomoic Sustainablity data into Envizi ESG Suite </div></Col>
                </Row>
              </Container>
            </Col>
          </Row>

          <Row>
            <Col className="section">
              <Container>
                <Row>
                  <Col >
                    <div className="section-heading">Filter</div>
                  </Col>
                </Row>
                <Row>
                  <Col className='form-group-col-class' >
                    <Form.Group className='form-group-class' >
                      <Form.Label className='form-label-class'>Start Date:</Form.Label>
                      <Form.Control type="text" htmlSize="50" value={this.getStartDateForDisplay()} onChange={(e) => this.handleInputChange(e, 'turbo', 'parameters', 'start_date')} />
                    </Form.Group>
                  </Col>
                  <Col md="2"> </Col>
                  <Col className='form-group-col-class' >
                    <Form.Group className='form-group-class' >
                      <Form.Label className='form-label-class'>End Date:</Form.Label>
                      <Form.Control type="text" htmlSize="50" value={this.getEndDateForDisplay()} onChange={(e) => this.handleInputChange(e, 'turbo', 'parameters', 'end_date')} />
                    </Form.Group>
                  </Col>
                  <Col md="5"> </Col>
                </Row>
                <Row className="justify-content-md-center">
                  <Col md="8"> </Col>
                  <Col><Button type="submit" className="btn-success buttons" disabled={this.state.loading}  onClick={(e) => this.handleView(e)} >&nbsp;&nbsp;View In screen</Button></Col>
                  <Col><Button type="submit" className="btn-success buttons" disabled={this.state.loading}  onClick={(e) => this.handleIngest(e)} >&nbsp;&nbsp;Ingest to Envizi</Button></Col>
                </Row>
                <Row className="justify-content-md-center">
                  <Col>
                    {this.state.loading && (
                      <div><p>&nbsp;</p>
                        <Spinner animation="border" role="status" variant="primary">
                          <span className="visually-hidden">Loading...</span>
                        </Spinner>
                      </div>
                    )}
                  </Col>
                </Row>
              </Container>
            </Col>
          </Row>
          <DataTable jsonData={this.state.locationData} headingText={"Locations"} />
          <DataTable jsonData={this.state.accountsData} headingText={"Accounts"} />
        </Container>
      </div>
    );
  }
}
export default TurboMain;
