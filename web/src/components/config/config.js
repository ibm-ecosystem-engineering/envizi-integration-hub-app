import React, { Component } from 'react';

import axios from 'axios';
import Spinner from 'react-bootstrap/Spinner';

import Form from 'react-bootstrap/Form';
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Button from "react-bootstrap/Button";
import Image from "react-bootstrap/Image";
import Collapse from "react-bootstrap/Collapse";
import Container from "react-bootstrap/Container";
import "./config.css";


import Main from "../main/main";

import { useState } from 'react'

class ConfigMain extends Component {

  constructor() {
    super();
    this.state = {
      loading: true,
      configData: null
    }
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
        console.log("Output of the API Call ---> " + response.data);
        const returnData = response.data;
        this.setState((prevData) => {
          const newData = { ...prevData }
          newData.configData = returnData
          newData.loading = false;
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

  handleSubmit = (event) => {
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

    axios.post(myURL + '/api/config/update', this.state.configData, { headers })
      .then(response => {
        console.log("Output of the API Call ---> " + response.data);
        const returnData = response.data;
        this.setState((prevData) => {
          const newData = { ...prevData }
          newData.configData = returnData
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

  render() {

    if (this.state.loading) {
      return <div>Loading...</div>;
    }

    return (
      <div style={{ overflowY: "auto", width: "100%", height: "80%", background: "white" }}>

        <Form onSubmit={this.handleSubmit}>
          <Container>
          <Row>
              <Col className="section-page">
                <Container>
                  <Row>
                    <Col >
                      <div className="section-heading-page">Configuration Settings</div>
                    </Col>
                  </Row>
                </Container>
              </Col>
            </Row>
            <Row>
              <Col className="section">
                <Container>
                  <Row>
                    <Col >
                      <div className="section-heading">Turbonomic Access</div>
                    </Col>
                  </Row>
                  <Row>
                    <Col md="7" className='form-group-col-class' >
                      <Form.Group className='form-group-class'>
                        <Form.Label className='form-label-class'>URL</Form.Label>
                        <Form.Control type="text" placeholder="Enter URL" value={this.state.configData.turbo.access.url} onChange={(e) => this.handleInputChange(e, 'turbo', 'access', 'url')} />
                      </Form.Group>
                    </Col>
                  </Row>
                  <Row>
                    <Col md="4" className='form-group-col-class' >
                      <Form.Group className='form-group-class'>
                        <Form.Label className='form-label-class'>User</Form.Label>
                        <Form.Control type="text" placeholder="Enter User" value={this.state.configData.turbo.access.user} onChange={(e) => this.handleInputChange(e, 'turbo', 'access', 'user')} />
                      </Form.Group>
                    </Col>
                  </Row>
                  <Row>
                    <Col md="4" className='form-group-col-class' >
                      <Form.Group className='form-group-class'>
                        <Form.Label className='form-label-class'>Password</Form.Label>
                        <Form.Control type="password" placeholder="Enter Password" value={this.state.configData.turbo.access.password} onChange={(e) => this.handleInputChange(e, 'turbo', 'access', 'password')} />
                      </Form.Group>
                    </Col>
                  </Row>
                  <Row>
                    <Col>&nbsp;&nbsp;
                    </Col>
                  </Row>
                </Container>
              </Col>
            </Row>
            <Row>
              <Col className="section">
                <Container>
                  <Row>
                    <Col>
                      <div className="section-heading">Turbonomic Parameters</div>
                    </Col>
                  </Row>
                  <Row>
                    <Col md="4" className='form-group-col-class'>
                      <Form.Group className='form-group-class' >
                        <Form.Label className='form-label-class'>Group Name</Form.Label>
                        <Form.Control type="text" value={this.state.configData.turbo.parameters.group} onChange={(e) => this.handleInputChange(e, 'turbo', 'parameters', 'group')} />
                      </Form.Group>
                    </Col>
                  </Row>
                  <Row>
                    <Col md="4" className='form-group-col-class'>
                      <Form.Group className='form-group-class' >
                        <Form.Label className='form-label-class'>Sub Group Name</Form.Label>
                        <Form.Control type="text" value={this.state.configData.turbo.parameters.sub_group} onChange={(e) => this.handleInputChange(e, 'turbo', 'parameters', 'sub_group')} />
                      </Form.Group>
                    </Col>
                  </Row>
                  <Row>
                    <Col md="4" className='form-group-col-class'>
                      <Form.Group className='form-group-class' >
                        <Form.Label className='form-label-class'>Account Style - Energy Consumption </Form.Label>
                        <Form.Control type="text" value={this.state.configData.turbo.parameters.account_style_energy_consumption} onChange={(e) => this.handleInputChange(e, 'turbo', 'parameters', 'account_style_energy_consumption')} /> 
                      </Form.Group>
                    </Col>
                  </Row>
                  <Row>
                    <Col md="4" className='form-group-col-class'>
                      <Form.Group className='form-group-class' >
                        <Form.Label className='form-label-class'>Account Style - Active Hosts </Form.Label>
                        <Form.Control type="text" value={this.state.configData.turbo.parameters.account_style_active_hosts} onChange={(e) => this.handleInputChange(e, 'turbo', 'parameters', 'account_style_active_hosts')} /> 
                      </Form.Group>
                    </Col>
                  </Row>
                  <Row>
                    <Col md="4" className='form-group-col-class'>
                      <Form.Group className='form-group-class' >
                        <Form.Label className='form-label-class'>Account Style - Active VMs </Form.Label>
                        <Form.Control type="text" value={this.state.configData.turbo.parameters.account_style_active_vms} onChange={(e) => this.handleInputChange(e, 'turbo', 'parameters', 'account_style_active_vms')} /> 
                      </Form.Group>
                    </Col>
                  </Row>
                  <Row>
                    <Col md="4" className='form-group-col-class'>
                      <Form.Group className='form-group-class' >
                        <Form.Label className='form-label-class'>Account Style - Energy Host Intensity </Form.Label>
                        <Form.Control type="text" value={this.state.configData.turbo.parameters.account_style_energy_host_intensity} onChange={(e) => this.handleInputChange(e, 'turbo', 'parameters', 'account_style_energy_host_intensity')} /> 
                      </Form.Group>
                    </Col>
                  </Row>
                  <Row>
                    <Col md="4" className='form-group-col-class'>
                      <Form.Group className='form-group-class' >
                        <Form.Label className='form-label-class'>Account Style - VM Host Density </Form.Label>
                        <Form.Control type="text" value={this.state.configData.turbo.parameters.account_style_vm_host_density} onChange={(e) => this.handleInputChange(e, 'turbo', 'parameters', 'account_style_vm_host_density')} />
                      </Form.Group>
                    </Col>
                  </Row>                                                                        
                  <Row>
                    <Col>&nbsp;&nbsp;
                    </Col>
                  </Row>
                </Container>
              </Col>
            </Row>
            <Row>
              <Col className="section">
                <Container>
                  <Row>
                    <Col>
                      <div className="section-heading">Turbonomic Filter</div>
                    </Col>
                  </Row>
                  <Row>
                    <Col md="4" className='form-group-col-class' >
                      <Form.Group className='form-group-class'>
                        <Form.Label className='form-label-class'>Start Date</Form.Label>
                        <Form.Control type="text" value={this.state.configData.turbo.parameters.start_date} onChange={(e) => this.handleInputChange(e, 'turbo', 'parameters', 'start_date')} />
                      </Form.Group>
                    </Col>
                  </Row>
                  <Row>
                    <Col md="4" className='form-group-col-class' >
                      <Form.Group className='form-group-class'>
                        <Form.Label className='form-label-class'>End Date</Form.Label>
                        <Form.Control type="text" value={this.state.configData.turbo.parameters.end_date} onChange={(e) => this.handleInputChange(e, 'turbo', 'parameters', 'end_date')} />
                      </Form.Group>
                    </Col>
                  </Row>
                  <Row>
                    <Col>&nbsp;&nbsp;
                    </Col>
                  </Row>
                </Container>
              </Col>
            </Row>
            <Row>
              <Col className="section">
                <Container>
                  <Row>
                    <Col >
                      <div className="section-heading">Envizi Access</div>
                    </Col>
                  </Row>
                  <Row>
                    <Col md="7" className='form-group-col-class' >
                      <Form.Group className='form-group-class'>
                        <Form.Label className='form-label-class'>Aws Bucket Name</Form.Label>
                        <Form.Control type="text" placeholder="Enter Aws Bucket Name" value={this.state.configData.envizi.access.bucket_name} onChange={(e) => this.handleInputChange(e, 'envizi', 'access', 'bucket_name')} />
                      </Form.Group>
                    </Col>
                  </Row>
                  <Row>
                    <Col md="7" className='form-group-col-class' >
                      <Form.Group className='form-group-class'>
                        <Form.Label className='form-label-class'>Aws Folder Name</Form.Label>
                        <Form.Control type="text" placeholder="Enter Aws Folder Name" value={this.state.configData.envizi.access.folder_name} onChange={(e) => this.handleInputChange(e, 'envizi', 'access', 'folder_name')} />
                      </Form.Group>
                    </Col>
                  </Row>
                  <Row>
                    <Col md="7" className='form-group-col-class' >
                      <Form.Group className='form-group-class'>
                        <Form.Label className='form-label-class'>Aws Access Key</Form.Label>
                        <Form.Control type="password" placeholder="Enter Aws Access Key" value={this.state.configData.envizi.access.access_key} onChange={(e) => this.handleInputChange(e, 'envizi', 'access', 'access_key')} />
                      </Form.Group>
                    </Col>
                  </Row>
                  <Row>
                    <Col md="7" className='form-group-col-class' >
                      <Form.Group className='form-group-class'>
                        <Form.Label className='form-label-class'>Aws Secret Key</Form.Label>
                        <Form.Control type="password" placeholder="Enter Aws Secret Key" value={this.state.configData.envizi.access.secret_key} onChange={(e) => this.handleInputChange(e, 'envizi', 'access', 'secret_key')} />
                      </Form.Group>
                    </Col>
                  </Row>
                  <Row>
                    <Col>&nbsp;&nbsp;
                    </Col>
                  </Row>
                </Container>
              </Col>
            </Row>
          <Row>
              <Col className="section">
                <Container>
                  <Row>
                    <Col >
                      <div className="section-heading">Envizi Parameters</div>
                    </Col>
                  </Row>
                  <Row>
                    <Col md="7" className='form-group-col-class' >
                      <Form.Group className='form-group-class'>
                        <Form.Label className='form-label-class'>Org Name</Form.Label>
                        <Form.Control type="text" placeholder="Enter Prefix" value={this.state.configData.envizi.parameters.org_name} onChange={(e) => this.handleInputChange(e, 'envizi', 'parameters', 'org_name')} />
                      </Form.Group>
                    </Col>
                  </Row>
                  <Row>
                    <Col md="7" className='form-group-col-class' >
                      <Form.Group className='form-group-class'>
                        <Form.Label className='form-label-class'>Prefix</Form.Label>
                        <Form.Control type="text" placeholder="Enter Prefix" value={this.state.configData.envizi.parameters.prefix} onChange={(e) => this.handleInputChange(e, 'envizi', 'parameters', 'prefix')} />
                      </Form.Group>
                    </Col>
                  </Row>
                  <Row>
                    <Col>&nbsp;&nbsp;
                    </Col>
                  </Row>
                </Container>
              </Col>
            </Row>
          </Container>
          <Container>
            <Row>
              <Col >
                <div className="justify-content-center">
                <Button type="submit" className="btn-success buttons" disabled={this.state.loading} >
                  &nbsp;&nbsp;Save
                </Button>
                </div>
              </Col>
            </Row>
          </Container>
        </Form>
      </div>
    );
  }
}
export default ConfigMain;
