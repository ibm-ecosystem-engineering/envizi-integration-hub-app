'use client';
import React, { Component } from 'react';

import { Tabs, Tab, TabList, TabPanels, TabPanel } from '@carbon/react';
import { Loading, Button, Grid, Column } from 'carbon-components-react';

import axios from 'axios';

import { API_URL } from '../../components/common-constants.js';
import DataTable from '../../components/DataTable/DataTable';

import '../../components/css/common.css'; // Import the CSS file for styling

import TemplateMapPOC from './TemplateMapPOC.js';
import TemplateMapASDL from './TemplateMapASDL.js';

class ExcelPage extends Component {
  constructor() {
    super();
    this.state = {
      loading: false,
      selectedFileCONFIG: null,
      selectedFilePOC: null,
      selectedFileASDL: null,

      resultUploadCONFIG: null,
      resultUploadPOC: null,
      resultUploadASDL: null,

      resultIngestCONFIG: null,
      resultIngestPOC: null,
      resultIngestASDL: null,

      resultContentInvoice: '',
      childDataPOC: null,

      locations: [],
      accounts: [],
    };
  }

  handleFileChangeCONFIG = (event) => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.selectedFileCONFIG = event.target.files[0];
      newData.resultUploadCONFIG = null;
      newData.resultIngestCONFIG = null;
      return newData;
    });
  };

  handleFileChangePOC = (event) => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.selectedFilePOC = event.target.files[0];
      newData.resultUploadPOC = null;
      newData.resultIngestPOC = null;
      return newData;
    });
  };

  handleFileChangeASDL = (event) => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.selectedFileASDL = event.target.files[0];
      newData.resultUploadASDL = null;
      newData.resultIngestASDL = null;
      return newData;
    });
  };

  setLoading = (value) => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.loading = value;
      return newData;
    });
  };

  handleIngestCONFIG = async () => {
    this.setLoading(true);

    try {
      var my_URL =
        this.envUtility.getAPIUrl() + '/api/excel/uploadConfigConnector';
      const formData = new FormData();
      formData.append('file', this.state.selectedFileCONFIG);

      const response = await axios.post(my_URL, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      this.setState((prevData) => {
        const newData = { ...prevData };
        newData.resultUploadCONFIG = response.data;
        newData.loading = false;
        return newData;
      });
    } catch (error) {
      console.error('Error uploading file', error);
      this.setLoading(false);
    }
  };

  handleUploadPOC = async () => {
    this.setLoading(true);
    try {
      var my_URL = this.envUtility.getAPIUrl() + '/api/excel/loadTemplatePOC';
      const formData = new FormData();
      formData.append('file', this.state.selectedFilePOC);

      const response = await axios.post(my_URL, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      this.setState((prevData) => {
        const newData = { ...prevData };
        newData.resultUploadPOC = response.data;
        newData.loading = false;
        return newData;
      });
    } catch (error) {
      console.error('Error uploading file', error);
      this.setLoading(false);
    }
  };

  handleUploadASDL = async () => {
    this.setLoading(true);
    try {
      var my_URL = this.envUtility.getAPIUrl() + '/api/excel/loadTemplateASDL';
      const formData = new FormData();
      formData.append('file', this.state.selectedFileASDL);

      const response = await axios.post(my_URL, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      this.setState((prevData) => {
        const newData = { ...prevData };
        newData.resultUploadASDL = response.data;
        newData.loading = false;
        return newData;
      });
    } catch (error) {
      console.error('Error uploading file', error);
      this.setLoading(false);
    }
  };

  handleIngestPOC = async () => {
    this.setLoading(true);

    const headers = {
      Authorization: 'Bearer xxxxx',
      'Access-Control-Allow-Origin': '*',
    };

    const myData = {
      template_columns: this.state.resultUploadPOC.template_columns,
      uploaded_columns: this.state.resultUploadPOC.uploaded_columns,
      uploadedFile: this.state.resultUploadPOC.uploadedFile,
      data_mapping: this.state.childDataPOC,
    };

    var my_URL = this.envUtility.getAPIUrl() + '/api/excel/ingestTemplatePOC';
    axios
      .post(my_URL, myData, { headers })
      .then((response) => {
        this.setState((prevData) => {
          const newData = { ...prevData };
          newData.resultIngestPOC = response.data;
          newData.loading = false;
          return newData;
        });
      })
      .catch((error) => {
        console.log(error);
        this.setState((prevData) => {
          const newData = { ...prevData };
          newData.loading = false;
          return newData;
        });
      });
  };

  handleIngestASDL = async () => {
    this.setLoading(true);

    const headers = {
      Authorization: 'Bearer xxxxx',
      'Access-Control-Allow-Origin': '*',
    };

    const myData = {
      template_columns: this.state.resultUploadASDL.template_columns,
      uploaded_columns: this.state.resultUploadASDL.uploaded_columns,
      uploadedFile: this.state.resultUploadASDL.uploadedFile,
      data_mapping: this.state.childDataPOC,
    };

    var my_URL = this.envUtility.getAPIUrl() + '/api/excel/ingestTemplateASDL';
    axios
      .post(my_URL, myData, { headers })
      .then((response) => {
        this.setState((prevData) => {
          const newData = { ...prevData };
          newData.resultIngestASDL = response.data;
          newData.loading = false;
          return newData;
        });
      })
      .catch((error) => {
        console.log(error);
        this.setState((prevData) => {
          const newData = { ...prevData };
          newData.loading = false;
          return newData;
        });
      });
  };

  handleChildDataChange = (data) => {
    // Update parent state with data from child
    this.setState({ childDataPOC: data });
    console.info(JSON.stringify(this.state.childDataPOC));
  };

  componentDidMount() {
    this.handleLoad();
  }

  handleLoad() {
    this.loadLocations();
    this.loadAccounts();
  }

  loadLocations() {
    const headers = {
      'Access-Control-Allow-Origin': '*',
    };

    var my_URL = this.envUtility.getAPIUrl() + '/api/envizi/locations';
    axios
      .get(my_URL, {}, { headers })
      .then((response) => {
        //Uploaded columns
        let arr1 = [''];
        let arr2 = response.data.data;
        let combinedArray = [...arr1, ...arr2];

        this.setState({ locations: combinedArray });
      })
      .catch((error) => {
        console.log('loadLocations ---: ' + error);
      });
  }

  loadAccounts() {
    const headers = {
      'Access-Control-Allow-Origin': '*',
    };

    var my_URL = this.envUtility.getAPIUrl() + '/api/envizi/accounts';
    axios
      .get(my_URL, {}, { headers })
      .then((response) => {
        //Uploaded columns
        let arr1 = [''];
        let arr2 = response.data.data;
        let combinedArray = [...arr1, ...arr2];

        this.setState({ accounts: combinedArray });
      })
      .catch((error) => {
        console.log('loadAccounts ---: ' + error);
      });
  }

  render() {
    return (
      <Grid>
        <Column
          lg={16}
          md={8}
          sm={4}
          className="landing-page__banner my-title-image"
        >
          <span className="SubHeaderTitle">Excel Data Processing</span>
        </Column>
        <Column lg={16} md={8} sm={4} className="landing-page__r2">
          <Tabs defaultSelectedIndex={0}>
            <TabList className="tabs-group" aria-label="Page navigation">
              <Tab>Config Connector & UDC</Tab>
              <Tab>POC Account Setup and Data Load</Tab>
              <Tab>Account Setup and Data Load PM&C</Tab>
            </TabList>
            <TabPanels>
              <TabPanel>
                <Grid className="my-tabs-group-content">
                  <Column lg={16}>
                    <table className="fin-table">
                      <tbody>
                        <tr>
                          <td>
                            <div className="my-component">
                              <div className="fin-header-section">
                                <div className="fin-text-heading">
                                  Data Upload
                                </div>
                                <div className="fin-text-heading-label">
                                  Upload the Config Connector or UDC Template
                                  excel file
                                </div>
                              </div>
                              <div className="fin-container">
                                <table>
                                  <tbody>
                                    <tr>
                                      <td className="instruction-label">
                                        <input
                                          type="file"
                                          className="file-class"
                                          onClick={this.handleFileChangeCONFIG}
                                          onChange={this.handleFileChangeCONFIG}
                                        />
                                      </td>
                                      <td className="instruction-label">
                                        <Button
                                          size="sm"
                                          className="input-control-lable"
                                          onClick={() => {
                                            this.handleIngestCONFIG();
                                          }}
                                          disabled={this.state.loading}
                                        >
                                          Upload & Ingest
                                        </Button>
                                      </td>
                                    </tr>
                                    <tr>
                                      <td>
                                        <span className="instruction-msg">
                                          {!this.state.loading &&
                                          this.state.resultUploadCONFIG ? (
                                            <span>
                                              {
                                                this.state.resultUploadCONFIG
                                                  .msg
                                              }
                                            </span>
                                          ) : (
                                            <span></span>
                                          )}
                                        </span>
                                      </td>
                                    </tr>
                                  </tbody>
                                </table>
                              </div>
                            </div>
                          </td>
                        </tr>
                        <tr>
                          <td>
                            {this.state.loading && (
                              <div>
                                <p>&nbsp;</p>
                                <Loading description="Loading content..." />
                              </div>
                            )}
                          </td>
                        </tr>
                        <tr>
                          <td>
                            {this.state.resultUploadCONFIG &&
                              this.state.resultUploadCONFIG.processed_data && (
                                <CarbonTable
                                  columns={
                                    this.state.resultUploadCONFIG
                                      .processed_data_columns
                                  }
                                  jsonData={
                                    this.state.resultUploadCONFIG.processed_data
                                  }
                                  headingText1={'Data Ingested'}
                                  headingText2={
                                    'The below data have been pushed to Envizi'
                                  }
                                />
                              )}
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </Column>
                </Grid>
              </TabPanel>

              <TabPanel>
                <Grid className="my-tabs-group-content">
                  <Column
                    md={4}
                    lg={16}
                    sm={4}
                    className="landing-page__tab-content"
                  >
                    <table className="fin-table">
                      <tbody>
                        <tr>
                          <td>
                            <div className="my-component">
                              <div className="fin-header-section">
                                <div className="fin-text-heading">
                                  Data Upload
                                </div>
                                <div className="fin-text-heading-label">
                                  Upload the excel file that contains your data.
                                </div>
                              </div>
                              <div className="fin-container">
                                <table>
                                  <tbody>
                                    <tr>
                                      <td className="instruction-label">
                                        <input
                                          type="file"
                                          className="file-class"
                                          onClick={this.handleFileChangePOC}
                                          onChange={this.handleFileChangePOC}
                                        />
                                      </td>
                                      <td className="instruction-label">
                                        <Button
                                          size="sm"
                                          className="input-control-lable"
                                          onClick={() => {
                                            this.handleUploadPOC();
                                          }}
                                          disabled={this.state.loading}
                                        >
                                          Upload
                                        </Button>
                                      </td>
                                    </tr>
                                    <tr>
                                      <td>
                                        <span className="instruction-msg">
                                          {!this.state.loading &&
                                          this.state.resultUploadPOC ? (
                                            <span>
                                              {this.state.resultUploadPOC.msg}
                                            </span>
                                          ) : (
                                            <span></span>
                                          )}
                                        </span>
                                      </td>
                                    </tr>
                                  </tbody>
                                </table>
                              </div>
                            </div>
                          </td>
                        </tr>
                        <tr>
                          <td>
                            {this.state.loading && (
                              <div>
                                <p>&nbsp;</p>
                                <Loading description="Loading content..." />
                              </div>
                            )}
                          </td>
                        </tr>
                        <tr>
                          {this.state.resultUploadPOC &&
                            this.state.resultUploadPOC.uploaded_columns && (
                              <td>
                                <TemplateMapPOC
                                  onChildDataChange={this.handleChildDataChange}
                                  ingestButtonClickParentMethod={
                                    this.handleIngestPOC
                                  }
                                  uploaded_columns={
                                    this.state.resultUploadPOC.uploaded_columns
                                  }
                                  resultIngestPOC={this.state.resultIngestPOC}
                                  locations={this.state.locations}
                                  accounts={this.state.accounts}
                                ></TemplateMapPOC>
                              </td>
                            )}
                        </tr>

                        <tr>
                          <td>
                            {this.state.resultIngestPOC &&
                              this.state.resultIngestPOC.processed_data && (
                                <CarbonTable
                                  columns={
                                    this.state.resultUploadPOC.template_columns
                                  }
                                  jsonData={
                                    this.state.resultIngestPOC.processed_data
                                  }
                                  headingText1={'Data Ingested'}
                                  headingText2={
                                    'The below data have been pushed to Envizi'
                                  }
                                />
                              )}
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </Column>
                </Grid>
              </TabPanel>

              <TabPanel>
                <Grid className="my-tabs-group-content">
                  <Column
                    md={4}
                    lg={16}
                    sm={4}
                    className="landing-page__tab-content"
                  >
                    <table className="fin-table">
                      <tbody>
                        <tr>
                          <td>
                            <div className="my-component">
                              <div className="fin-header-section">
                                <div className="fin-text-heading">
                                  Data Upload
                                </div>
                                <div className="fin-text-heading-label">
                                  Upload the excel file that contains your data.
                                </div>
                              </div>
                              <div className="fin-container">
                                <table>
                                  <tbody>
                                    <tr>
                                      <td className="instruction-label">
                                        <input
                                          type="file"
                                          className="file-class"
                                          onClick={this.handleFileChangeASDL}
                                          onChange={this.handleFileChangeASDL}
                                        />
                                      </td>
                                      <td className="instruction-label">
                                        <Button
                                          size="sm"
                                          className="input-control-lable"
                                          onClick={() => {
                                            this.handleUploadASDL();
                                          }}
                                          disabled={this.state.loading}
                                        >
                                          Upload
                                        </Button>
                                      </td>
                                    </tr>
                                    <tr>
                                      <td>
                                        <span className="instruction-msg">
                                          {!this.state.loading &&
                                          this.state.resultUploadASDL ? (
                                            <span>
                                              {this.state.resultUploadASDL.msg}
                                            </span>
                                          ) : (
                                            <span></span>
                                          )}
                                        </span>
                                      </td>
                                    </tr>
                                  </tbody>
                                </table>
                              </div>
                            </div>
                          </td>
                        </tr>
                        <tr>
                          <td>
                            {this.state.loading && (
                              <div>
                                <p>&nbsp;</p>
                                <Loading description="Loading content..." />
                              </div>
                            )}
                          </td>
                        </tr>
                        <tr>
                          {this.state.resultUploadASDL &&
                            this.state.resultUploadASDL.uploaded_columns && (
                              <td>
                                <TemplateMapASDL
                                  onChildDataChange={this.handleChildDataChange}
                                  ingestButtonClickParentMethod={
                                    this.handleIngestASDL
                                  }
                                  uploaded_columns={
                                    this.state.resultUploadASDL.uploaded_columns
                                  }
                                  resultIngestASDL={this.state.resultIngestASDL}
                                  locations={this.state.locations}
                                  accounts={this.state.accounts}
                                ></TemplateMapASDL>
                              </td>
                            )}
                        </tr>

                        <tr>
                          <td>
                            {this.state.resultIngestASDL &&
                              this.state.resultIngestASDL.processed_data && (
                                <CarbonTable
                                  columns={
                                    this.state.resultUploadASDL.template_columns
                                  }
                                  jsonData={
                                    this.state.resultIngestASDL.processed_data
                                  }
                                  headingText1={'Data Ingested'}
                                  headingText2={
                                    'The below data have been pushed to Envizi'
                                  }
                                />
                              )}
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </Column>
                </Grid>
              </TabPanel>
            </TabPanels>
          </Tabs>
        </Column>
      </Grid>
    );
  }
}
export default ExcelPage;
