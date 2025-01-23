'use client';
import React, { Component } from 'react';

import {
  Breadcrumb,
  BreadcrumbItem,
  Tabs,
  Tab,
  TabList,
  TabPanels,
  TabPanel,
} from '@carbon/react';
import {
  Loading,
  TextInput,
  Button,
  Grid,
  Row,
  Column,
} from 'carbon-components-react';

import axios from 'axios';

import {
  Advocate,
  Globe,
  AcceleratingTransformation,
} from '@carbon/pictograms-react';

import '../../components/css/common.css'; // Import the CSS file for styling
import CarbonTable from '@/components/CarbonTable/CarbonTable';
import EnvUtility from '../../components/EnvUtility/EnvUtility';

class InvoicePage extends Component {
  constructor() {
    super();
    this.state = {
      loading: true,
      configData: null,
      loadingInvoice: false,
      loadingUtilityBills: false,
      resultProcessInvoice: '',
      resultProcessUtilityBills: '',
    };
    this.envUtility = new EnvUtility();
  }

  handleLoad() {
    const headers = {
      Authorization: 'Bearer xxxxx',
      'Access-Control-Allow-Origin': '*',
    };

    var my_URL = this.envUtility.getAPIUrl() + '/api/config/load';
    axios
      .post(my_URL, {}, { headers })
      .then((response) => {
        const returnData = response.data;
        this.setState((prevData) => {
          const newData = { ...prevData };
          newData.configData = returnData;
          newData.loading = false;
          return newData;
        });
      })
      .catch((error) => {
        console.log(error);
        this.setState((prevData) => {
          const newData = { ...prevData };
          newData.configData = {};
          newData.loading = false;
          return newData;
        });
      });
  }

  componentDidMount() {
    this.handleLoad();
  }

  handleInputChange = (event, section1, section2, field) => {
    const { value } = event.target;
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.configData[section1][section2][field] = value;
      return newData;
    });
  };

  handleUtilityBillsViewInScreenByDiscovery = (event) => {
    event.preventDefault();
    var my_URL = this.envUtility.getAPIUrl() + '/api/utilitybill/viewInScreen';
    this.handleProcessUtilityBills(my_URL);
  };

  handleUtilityBillsIngestToEnviziByDiscovery = (event) => {
    event.preventDefault();
    var my_URL =
      this.envUtility.getAPIUrl() + '/api/utilitybill/ingestToEnvizi';
    this.handleProcessUtilityBills(my_URL);
  };

  handleUtilityBillsViewInScreen = (event) => {
    event.preventDefault();
    var my_URL =
      this.envUtility.getAPIUrl() + '/api/utilitybill/llm/viewInScreen';
    this.handleProcessUtilityBills(my_URL);
  };

  handleUtilityBillsIngestToEnvizi = (event) => {
    event.preventDefault();
    var my_URL =
      this.envUtility.getAPIUrl() + '/api/utilitybill/llm/ingestToEnvizi';
    this.handleProcessUtilityBills(my_URL);
  };

  handleUtilityBillsViewInScreenByDocling = (event) => {
    event.preventDefault();
    var my_URL =
      this.envUtility.getAPIUrl() + '/api/utilitybill/llmdocling/viewInScreen';
    this.handleProcessUtilityBills(my_URL);
  };

  handleUtilityBillsIngestToEnviziByDocling = (event) => {
    event.preventDefault();
    var my_URL =
      this.envUtility.getAPIUrl() +
      '/api/utilitybill/llmdocling/ingestToEnvizi';
    this.handleProcessUtilityBills(my_URL);
  };

  handleProcessUtilityBills = (my_URL) => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.loadingUtilityBills = true;
      newData.resultProcessUtilityBills = '';
      return newData;
    });

    const headers = {
      Authorization: 'Bearer xxxxx',
      'Access-Control-Allow-Origin': '*',
    };

    axios
      .post(my_URL, {}, { headers })
      .then((response) => {
        const returnData = response.data;
        this.setState((prevData) => {
          const newData = { ...prevData };
          newData.resultProcessUtilityBills = returnData;
          newData.loadingUtilityBills = false;
          return newData;
        });
      })
      .catch((error) => {
        console.log(error);
        this.setState((prevData) => {
          const newData = { ...prevData };
          newData.loading = false;
          newData.loadingUtilityBills = false;
          return newData;
        });
      });
  };

  handleProcessInvoices = (event) => {
    event.preventDefault();

    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.loadingInvoice = true;
      newData.resultProcessInvoice = '';
      return newData;
    });

    const headers = {
      Authorization: 'Bearer xxxxx',
      'Access-Control-Allow-Origin': '*',
    };

    var my_URL = this.envUtility.getAPIUrl() + '/api/invoice/export';
    axios
      .post(my_URL, {}, { headers })
      .then((response) => {
        const returnData = response.data;
        this.setState((prevData) => {
          const newData = { ...prevData };
          newData.resultProcessInvoice = returnData;
          newData.loadingInvoice = false;
          return newData;
        });
      })
      .catch((error) => {
        console.log(error);
        this.setState((prevData) => {
          const newData = { ...prevData };
          newData.loading = false;
          newData.loadingInvoice = false;
          return newData;
        });
      });
  };

  handleSubmit = (event) => {
    event.preventDefault();

    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.loading = true;
      return newData;
    });

    const headers = {
      Authorization: 'Bearer xxxxx',
      'Access-Control-Allow-Origin': '*',
    };

    var my_URL = this.envUtility.getAPIUrl() + '/api/config/update';
    axios
      .post(my_URL, this.state.configData, { headers })
      .then((response) => {
        const returnData = response.data;
        this.setState((prevData) => {
          const newData = { ...prevData };
          newData.configData = returnData;
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

  render() {
    return (
      <Grid className="landing-page" fullWidth>
        <Column
          lg={16}
          md={8}
          sm={4}
          className="landing-page__banner my-title-image"
        >
          <span className="SubHeaderTitle">
            Invoice and Utility bills Processing
          </span>
        </Column>
        <Column lg={16} md={8} sm={4} className="landing-page__r2">
          <Tabs defaultSelectedIndex={0}>
            <TabList className="tabs-group" aria-label="Page navigation">
              <Tab>Invoices</Tab>
              <Tab>Utility Bills</Tab>
            </TabList>
            <TabPanels>
              <TabPanel>
                <Grid className="my-tabs-group-content">
                  <Column lg={16} className="landing-page__tab-content">
                    <table className="fin-table">
                      <tbody>
                        <tr>
                          <td>
                            <div className="my-component">
                              <div className="fin-header-section">
                                <div className="fin-text-heading">
                                  Process Invoice
                                </div>
                                <div className="fin-text-heading-label">
                                  To process Scope 3 - Category 1 Purchased
                                  Goods
                                </div>
                              </div>
                              <div className="fin-container">
                                <table>
                                  <tbody>
                                    <tr>
                                      <td className="instruction-label">
                                        Envizi Integration Hub helps to process
                                        the Purchased goods Invoices of your
                                        organziation and create Scope 3 -
                                        Category 1 Purchased Goods Data that can
                                        be feed into Envizi AI-Assist feature.
                                      </td>
                                    </tr>
                                    <tr>
                                      <td className="instruction-label">
                                        <Button
                                          className="fin-button-1"
                                          onClick={this.handleProcessInvoices}
                                          disabled={this.state.loadingInvoice}
                                        >
                                          Process Invoices
                                        </Button>
                                      </td>
                                    </tr>
                                    <tr>
                                      <td>&nbsp;</td>
                                    </tr>
                                    <tr>
                                      <td>
                                        <span className="instruction-msg">
                                          {!this.state.loadingInvoice &&
                                          this.state.resultProcessInvoice ? (
                                            <span>
                                              <p>
                                                {
                                                  this.state
                                                    .resultProcessInvoice.msg
                                                }
                                              </p>
                                              <p></p>
                                              <p>
                                                You can upload this file in the
                                                AI AssistFile Processing section
                                                of Envizi.
                                              </p>
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
                            {this.state.loadingInvoice && (
                              <div>
                                <p>&nbsp;</p>
                                <Loading description="Loading content..." />
                              </div>
                            )}
                          </td>
                        </tr>
                        <tr>
                          <td>
                            <div>
                              {this.state.resultProcessInvoice &&
                                this.state.resultProcessInvoice
                                  .processed_data && (
                                  <CarbonTable
                                    columns={
                                      this.state.resultProcessInvoice
                                        .processed_data_columns
                                    }
                                    jsonData={
                                      this.state.resultProcessInvoice
                                        .processed_data
                                    }
                                    headingText1={'Data Created'}
                                    headingText2={
                                      'The below data have been created for uploading into Envizi'
                                    }
                                  />
                                )}
                            </div>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </Column>
                </Grid>
              </TabPanel>
              <TabPanel>
                <Grid className="my-tabs-group-content">
                  <Column lg={16} className="landing-page__tab-content">
                    <table className="fin-table">
                      <tbody>
                        <tr>
                          <td>
                            <div className="my-component">
                              <div className="fin-header-section">
                                <div className="fin-text-heading">
                                  Process Utility Bills
                                </div>
                                <div className="fin-text-heading-label">
                                  To process the Utility Bills of your
                                  organziation.
                                </div>
                              </div>
                              <div className="fin-container">
                                <table className="fin-table">
                                  <tbody>
                                    <tr>
                                      <td className="instruction-label">
                                        Envizi Integration Hub helps process the
                                        bills of your organization, creates
                                        electricity and water-related data in
                                        the UDC format, and pushes the UDC
                                        format data into S3 data services for
                                        integration with Envizi.
                                      </td>
                                    </tr>
                                    <tr>
                                      <td className="instruction-label">
                                        <Button
                                          className="fin-button-1"
                                          onClick={
                                            this.handleUtilityBillsViewInScreen
                                          }
                                          disabled={
                                            this.state.loadingUtilityBills
                                          }
                                        >
                                          Preview
                                        </Button>
                                        &nbsp;&nbsp;&nbsp;&nbsp;
                                        <Button
                                          className="fin-button-1"
                                          onClick={
                                            this
                                              .handleUtilityBillsIngestToEnvizi
                                          }
                                          disabled={
                                            this.state.loadingUtilityBills
                                          }
                                        >
                                          Ingest into Envizi
                                        </Button>
                                        &nbsp;&nbsp;&nbsp;&nbsp;
                                        <Button
                                          className="fin-button-1"
                                          onClick={
                                            this
                                              .handleUtilityBillsViewInScreenByDiscovery
                                          }
                                          disabled={
                                            this.state.loadingUtilityBills
                                          }
                                        >
                                          Preview by Discovery
                                        </Button>
                                        &nbsp;&nbsp;&nbsp;&nbsp;
                                        <Button
                                          className="fin-button-1"
                                          onClick={
                                            this
                                              .handleUtilityBillsIngestToEnviziByDiscovery
                                          }
                                          disabled={
                                            this.state.loadingUtilityBills
                                          }
                                        >
                                          Ingest into Envizi by Discovery
                                        </Button>
                                        &nbsp;&nbsp;&nbsp;&nbsp;
                                        <Button
                                          className="fin-button-1"
                                          onClick={
                                            this
                                              .handleUtilityBillsViewInScreenByDocling
                                          }
                                          disabled={
                                            this.state.loadingUtilityBills
                                          }
                                        >
                                          Preview by Docling
                                        </Button>
                                        &nbsp;&nbsp;&nbsp;&nbsp;
                                        <Button
                                          className="fin-button-1"
                                          onClick={
                                            this
                                              .handleUtilityBillsIngestToEnviziByDocling
                                          }
                                          disabled={
                                            this.state.loadingUtilityBills
                                          }
                                        >
                                          Ingest into Envizi by Docling
                                        </Button>
                                      </td>
                                    </tr>
                                    <tr>
                                      <td>&nbsp;</td>
                                    </tr>
                                    <tr>
                                      <td>
                                        <span className="instruction-msg">
                                          {!this.state.loadingUtilityBills &&
                                          this.state
                                            .resultProcessUtilityBills ? (
                                            <span>
                                              {
                                                this.state
                                                  .resultProcessUtilityBills.msg
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
                            {this.state.loadingUtilityBills && (
                              <div>
                                <p>&nbsp;</p>
                                <Loading description="Loading content..." />
                              </div>
                            )}
                          </td>
                        </tr>
                        <tr>
                          <td>
                            {this.state.resultProcessUtilityBills &&
                              this.state.resultProcessUtilityBills
                                .processed_data && (
                                <CarbonTable
                                  columns={
                                    this.state.resultProcessUtilityBills
                                      .template_columns
                                  }
                                  jsonData={
                                    this.state.resultProcessUtilityBills
                                      .processed_data
                                  }
                                  headingText1={'Data Created'}
                                  headingText2={
                                    'The below data have been created for uploading into Envizi'
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
export default InvoicePage;
