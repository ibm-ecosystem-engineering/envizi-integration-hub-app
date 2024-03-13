import React, { Component } from 'react';
import { useEffect } from 'react';

import axios from 'axios';
import Spinner from 'react-bootstrap/Spinner';

import Form from "react-bootstrap/Form";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Button from "react-bootstrap/Button";
import Image from "react-bootstrap/Image";
import Collapse from "react-bootstrap/Collapse";
import Container from "react-bootstrap/Container";


import Main from "../main/main";

import configJsonData from "../../data/envizi-config.json";
import { useState } from 'react'
import Card from 'react-bootstrap/Card';
import './excel.css';

import { API_URL } from '../../common-constants';

import DraggableListDisplay from "./DraggableList";

import Notification from "../notification/Notification";


class ExcelMain extends React.Component {

  constructor() {
    super();
    this.state = {
      loading: false,
      selectedFileCONFIG: null,
      selectedFilePOC: null,
      selectedFileASDL: null,
      resultContentCONFIG: null,
      resultContentPOC: [],
      resultContentASDL: [],
      resultContentPOCIngest: "",
      resultContentASDLIngest: "",
    }
  }

  handleFileChangeCONFIG = (event) => {
    this.setState((prevData) => {
      const newData = { ...prevData }
      newData.selectedFileCONFIG = event.target.files[0];
      newData.resultContentCONFIG = null;
      return newData
    })
  };

  handleFileChangePOC = (event) => {
    this.setState((prevData) => {
      const newData = { ...prevData }
      newData.selectedFilePOC = event.target.files[0];
      newData.resultContentPOC = null;
      return newData
    })
  };

  handleFileChangeASDL = (event) => {
    this.setState((prevData) => {
      const newData = { ...prevData }
      newData.selectedFileASDL = event.target.files[0];
      newData.resultContentASDL = null;
      return newData
    })
  };

  setLoading = (value) => {
    this.setState((prevData) => {
      const newData = { ...prevData }
      newData.loading = value;
      return newData
    })
  };

  handleIngestCONFIG = async () => {
    this.setLoading(true);

    try {
      var urlFinal = API_URL + '/api/excel/uploadConfigConnector'
      const formData = new FormData();
      formData.append('file', this.state.selectedFileCONFIG);

      const response = await axios.post(urlFinal, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      console.log('File uploaded successfully:', response.data);

      this.setState((prevData) => {
        const newData = { ...prevData }
        newData.resultContentCONFIG = response.data;
        newData.loading = false;
        return newData
      })
    } catch (error) {
      console.error("Error uploading file", error);
      this.setLoading(false);
    }
  }

  handleUploadPOC = async () => {
    this.setLoading(true);
    try {
      var urlFinal = API_URL + '/api/excel/loadTemplatePOC'

      const formData = new FormData();
      formData.append('file', this.state.selectedFilePOC);

      const response = await axios.post(urlFinal, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      console.log('File uploaded successfully:', response.data);

      this.setState((prevData) => {
        const newData = { ...prevData }
        newData.resultContentPOC = response.data;
        newData.loading = false;
        return newData
      })
    } catch (error) {
      console.error("Error uploading file", error);
      this.setLoading(false);
    }
  }

  handleUploadASDL = async () => {
    this.setLoading(true);
    try {
      var urlFinal = API_URL + '/api/excel/loadTemplateASDL'

      const formData = new FormData();
      formData.append('file', this.state.selectedFileASDL);

      const response = await axios.post(urlFinal, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      console.log('File uploaded successfully:', response.data);

      this.setState((prevData) => {
        const newData = { ...prevData }
        newData.resultContentASDL = response.data;
        newData.loading = false;
        return newData
      })
    } catch (error) {
      console.error("Error uploading file", error);
      this.setLoading(false);
    }
  }

  handleIngestPOC = async () => {
    this.setLoading(true);

    const headers = {
      'Authorization': 'Bearer xxxxx',
      'Access-Control-Allow-Origin': '*',
    };

    const myData = {
      "template_columns" : this.state.resultContentPOC.template_array,
      "uploaded_columns" : this.state.resultContentPOC.uploaded_array,
      "uploadedFile" : this.state.resultContentPOC.uploadedFile,
    }

    axios.post(API_URL + '/api/excel/ingestTemplatePOC', myData, { headers })
      .then(response => {
        console.log("Output of the API Call ---> " + response.data);
        const returnData = response.data;
        this.setState((prevData) => {
          const newData = { ...prevData }
          newData.resultContentPOC = response.data;
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

  handleIngestASDL = async () => {
    this.setLoading(true);

    const headers = {
      'Authorization': 'Bearer xxxxx',
      'Access-Control-Allow-Origin': '*',
    };

    const myData = {
      "template_columns" : this.state.resultContentASDL.template_array,
      "uploaded_columns" : this.state.resultContentASDL.uploaded_array,
      "uploadedFile" : this.state.resultContentASDL.uploadedFile,
    }

    axios.post(API_URL + '/api/excel/ingestTemplateASDL', myData, { headers })
      .then(response => {
        console.log("Output of the API Call ---> " + response.data);
        const returnData = response.data;
        this.setState((prevData) => {
          const newData = { ...prevData }
          newData.resultContentASDL = response.data;
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


    return (

      <div style={{ overflowY: "auto", width: "100%", height: "80%", background: "white" }}>
        


        <Form onSubmit={this.handleSubmit}>
          <Container>
            <Row>
              <Col className="section-page">
                <Container>
                  <Row>
                    <Col >
                      <div className="section-heading-page">Excel Template Processing</div>
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
                      <div className="section-heading">Config Connector & UDC Template</div>
                    </Col>
                  </Row>
                  <Row>
                    <Col>&nbsp;&nbsp;
                    </Col>
                  </Row>
                  <Row>
                    <Col className="instruction-label">Select the excel template to upload
                    </Col>
                  </Row>
                  <Row>
                    <Col md="6" className='instruction-label' >
                      <input type="file" className='file-class' onClick={this.handleFileChangeCONFIG}  onChange={this.handleFileChangeCONFIG} />
                    </Col>
                    <Col md="3" className='instruction-label' >
                      <Button className="btn-success button-excel" onClick={() => { this.handleIngestCONFIG(); }}>
                        Upload & Ingest
                      </Button>
                    </Col>
                  </Row>
                  <Row>
                    <Col className='instruction-msg' >
                    {this.state.resultContentCONFIG ? (<span>{this.state.resultContentCONFIG.msg}</span>) : ( <span></span> )}
                    </Col>
                  </Row>
                </Container>
              </Col>
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
            <Row>
              <Col className="section">
                <Container>
                  <Row>
                    <Col>
                      <div className="section-heading">POC Account Setup and Data Load</div>
                    </Col>
                  </Row>
                  <Row>
                    <Col>&nbsp;&nbsp;
                    </Col>
                  </Row>

                  <Row>
                    <Col className="instruction-label">Select the excel template to upload
                    </Col>
                  </Row>
                  <Row>
                    <Col md="6" className='instruction-label' >
                      <input type="file" className='file-class' onClick={this.handleFileChangePOC} onChange={this.handleFileChangePOC} />
                    </Col>
                    <Col md="3" className='instruction-label' >
                      <Button className="btn-success button-excel" onClick={() => { this.handleUploadPOC(); }}>
                        Upload
                      </Button>
                    </Col>
                  </Row>
                  <Row>
                    <Col className='instruction-msg' >
                      {this.state.resultContentPOC ? (<span>{this.state.resultContentPOC.msg}</span>) : ( <span></span> )}
                    </Col>
                  </Row>
                  {this.state.resultContentPOC && this.state.resultContentPOC.template_array ? (
             
                  <Row>
                    <Col>
                          <Row>
                            <Col><div>Map the columns between the uploaded Excel file and the template</div>
                            </Col>
                          </Row>
                          <Row>
                            <Col md="6" className='form-group-col-class' >
                              <DraggableListDisplay data1={this.state.resultContentPOC.template_array} data2={this.state.resultContentPOC.uploaded_array} />
                            </Col>
                          </Row>
                          <Row>
                            <Col md="6" className='form-group-col-class' >
                            </Col>
                            <Col md="3" className='form-group-col-class' >
                              <Button className="btn-success button-excel" onClick={this.handleIngestPOC}>
                                Ingest
                              </Button>
                            </Col>
                          </Row>
                    </Col>
                  </Row>
                      ) : (<span></span>)}
                      <Row>
                    <Col className='instruction-msg' >
                    {this.state.resultContentPOCIngest}
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
                      <div className="section-heading">Account Setup and Data Load PM&C</div>
                    </Col>
                  </Row>
                  <Row>
                    <Col>&nbsp;&nbsp;
                    </Col>
                  </Row>

                  <Row>
                    <Col className="instruction-label">Select the excel template to upload
                    </Col>
                  </Row>
                  <Row>
                    <Col md="6" className='instruction-label' >
                      <input type="file" className='file-class'  onClick={this.handleFileChangeASDL} onChange={this.handleFileChangeASDL} />
                    </Col>
                    <Col md="3" className='instruction-label' >
                      <Button className="btn-success button-excel" onClick={this.handleUploadASDL}>
                        Upload
                      </Button>
                    </Col>
                  </Row>
                  <Row>
                    <Col className='instruction-msg' >
                      {this.state.resultContentASDL ? (<span>{this.state.resultContentASDL.msg}</span>) : ( <span></span> )}
                    </Col>
                  </Row>
                  {this.state.resultContentASDL && this.state.resultContentASDL.template_array ? (
                  <Row>
                    <Col>
                          <Row>
                            <Col><div>Map the columns between the uploaded Excel file and the template</div>
                            </Col>
                          </Row>
                          <Row>
                            <Col md="6" className='form-group-col-class' >
                              <DraggableListDisplay data1={this.state.resultContentASDL.template_array} data2={this.state.resultContentASDL.uploaded_array} />
                            </Col>
                          </Row>
                          <Row>
                            <Col md="6" className='form-group-col-class' >
                            </Col>
                            <Col md="3" className='form-group-col-class' >
                              <Button className="btn-success button-excel" onClick={this.handleIngestASDL}>
                                Ingest
                              </Button>
                            </Col>
                          </Row>
                    </Col>
                    </Row>
                  ) : (<span></span>)}
                  <Row>
                    <Col className='instruction-msg' >
                    {this.state.resultContentASDLIngest}
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
                </div>
              </Col>
            </Row>
          </Container>
        </Form>
      </div>
    );
  }
}

export default ExcelMain;
