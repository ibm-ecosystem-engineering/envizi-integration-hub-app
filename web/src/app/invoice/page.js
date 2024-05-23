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
import { InfoSection, InfoCard } from '@/components/Info/Info';
import { API_URL } from '../../components/common-constants.js';

import Image from 'next/image.js';
import '../../components/css/common.css'; // Import the CSS file for styling
import invoiceImage from './images/invoice.png'; // Import the image file
import CarbonTable from '@/components/CarbonTable/CarbonTable';

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
  }

  handleLoad() {
    const headers = {
      Authorization: 'Bearer xxxxx',
      'Access-Control-Allow-Origin': '*',
    };

    axios
      .post(API_URL + '/api/config/load', {}, { headers })
      .then((response) => {
        console.log(
          'Output of the API Call ---> ' + JSON.stringify(response.data)
        );
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

  handleProcessUtilityBills = (event) => {
    event.preventDefault();

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
      .post(API_URL + '/api/utilitybill/export', {}, { headers })
      .then((response) => {
        console.log(
          'Output of the utilitybill API Call ---> ' +
            JSON.stringify(response.data)
        );
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

    axios
      .post(API_URL + '/api/invoice/export', {}, { headers })
      .then((response) => {
        console.log(
          'Output of the API Call ---> ' + JSON.stringify(response.data)
        );
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

    axios
      .post(API_URL + '/api/config/update', this.state.configData, { headers })
      .then((response) => {
        console.log(
          'Output of the API Call ---> ' + JSON.stringify(response.data)
        );
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
              <Tab>Config</Tab>
            </TabList>
            <TabPanels>
              <TabPanel>
                <Grid className="my-tabs-group-content">
                  <Column lg={16} className="landing-page__tab-content">
                    <table className='fin-table'>
                    <tbody>
                      <tr>
                        <td>
                          <div className="my-component">
                            <div className="fin-header-section">
                              <div className="fin-text-heading">
                                Process Invoice
                              </div>
                              <div className="fin-text-heading-label">
                              To process Scope 3 - Category 1 Purchased Goods
                              </div>
                            </div>
                            <div className="fin-container">
                              <table>
                                <tbody>
                                <tr>
                                  <td className="instruction-label">
                                  Envizi Integration Hub helps to process the
                            Purchased goods Invoices of your organziation and
                            create Scope 3 - Category 1 Purchased Goods Data
                            that can be feed into Envizi AI-Assist feature.
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
                                        <span >
                                          <p >{this.state.resultProcessInvoice.msg}</p>
                                          <p></p>
                                          <p>You can upload this file in the AI AssistFile Processing section of Envizi.</p>
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
                        <td >
                        <div >
                          {this.state.resultProcessInvoice &&
                            this.state.resultProcessInvoice.processed_data && (
                              <CarbonTable
                                columns={
                                  this.state.resultProcessInvoice
                                    .processed_data_columns
                                }
                                jsonData={
                                  this.state.resultProcessInvoice.processed_data
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
                              To process the Utility Bills of your organziation.
                              </div>
                            </div>
                            <div className="fin-container">
                              <table className='fin-table'>
                              <tbody>
                              <tr>
                                  <td className="instruction-label">
                                  Envizi Integration Hub helps process the bills of your organization, creates electricity and water-related data in the UDC format, and pushes the UDC format data into S3 data services for integration with Envizi.
                                  </td>
                                </tr>
                                <tr>
                                  <td className="instruction-label">
                                    <Button
                                      className="fin-button-1"
                                      onClick={this.handleProcessUtilityBills}
                                      disabled={this.state.loadingUtilityBills}
                                    >
                                      Process Utility Bills
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
                                      this.state.resultProcessUtilityBills ? (
                                        <span>
                                          {
                                            this.state.resultProcessUtilityBills
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
                                    .processed_data_columns
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
              <TabPanel>
                <div className="my-component">
                  {/* Section at the top */}
                  {/* <section className="header-section">
                      <div className="text-heading">Configuration</div>
                      <div className="text-heading-label">
                        Configuration for Watson Discovery and Invoice Processing
                      </div>
                    </section> */}

                  {!this.state.loading && this.state.configData && (
                    <div>
                      <section className="top-section">
                        <div className="text-sub-heading">Discovery</div>
                        <div className="text-sub-heading-label2">
                          Watson Discovery configuration for Invoice and Utility
                          Bill Processing
                        </div>
                        <div className="upload-section">
                          <table >
                          <tbody>
                            <tr>
                              <td className="my-textbox-row">
                                <TextInput
                                  class="my-textbox"
                                  labelText="API Key"
                                  type="password"
                                  value={
                                    this.state.configData.discovery.access
                                      .api_key
                                  }
                                  onChange={(e) =>
                                    this.handleInputChange(
                                      e,
                                      'discovery',
                                      'access',
                                      'api_key'
                                    )
                                  }
                                />
                              </td>
                            </tr>
                            <tr>
                              <td className="my-textbox-row">
                                <TextInput
                                  class="my-textbox"
                                  labelText="Service URL"
                                  value={
                                    this.state.configData.discovery.access
                                      .service_url
                                  }
                                  onChange={(e) =>
                                    this.handleInputChange(
                                      e,
                                      'discovery',
                                      'access',
                                      'service_url'
                                    )
                                  }
                                />
                              </td>
                            </tr>
                          
                            </tbody></table>
                        </div>
                      </section>
                      <section className="top-section">
                        <div className="text-sub-heading">Invoices</div>
                        <div className="text-sub-heading-label2">
                          Watson Discovery and other configuration for Invoice
                          Processing
                        </div>
                        <div className="upload-section">
                          <table>
                          <tbody>
                            <tr>
                              <td className="my-textbox-row">
                                <TextInput
                                  class="my-textbox"
                                  labelText="Project Id"
                                  value={
                                    this.state.configData.discovery.access
                                      .project_id
                                  }
                                  onChange={(e) =>
                                    this.handleInputChange(
                                      e,
                                      'discovery',
                                      'access',
                                      'project_id'
                                    )
                                  }
                                />
                              </td>
                            </tr>
                            <tr>
                              <td className="my-textbox-row">
                                <TextInput
                                  class="my-textbox"
                                  labelText="Collection Id"
                                  value={
                                    this.state.configData.discovery.access
                                      .collection_ids
                                  }
                                  onChange={(e) =>
                                    this.handleInputChange(
                                      e,
                                      'discovery',
                                      'access',
                                      'collection_ids'
                                    )
                                  }
                                />
                              </td>
                            </tr>
                          
                            </tbody></table>
                        </div>
                      </section>
                      <section className="top-section">
                        <div className="text-sub-heading">Utility Bills</div>
                        <div className="text-sub-heading-label2">
                          Watson Discovery and other configuration for Utility
                          Bills Processing
                        </div>
                        <div className="upload-section">
                          <table>
                          <tbody>
                            <tr>
                              <td className="my-textbox-row">
                                <TextInput
                                  class="my-textbox"
                                  labelText="Project Id"
                                  value={
                                    this.state.configData.discovery.access
                                      .project_id2
                                  }
                                  onChange={(e) =>
                                    this.handleInputChange(
                                      e,
                                      'discovery',
                                      'access',
                                      'project_id2'
                                    )
                                  }
                                />
                              </td>
                            </tr>
                            <tr>
                              <td className="my-textbox-row">
                                <TextInput
                                  class="my-textbox"
                                  labelText="Collection Id"
                                  value={
                                    this.state.configData.discovery.access
                                      .collection_ids2
                                  }
                                  onChange={(e) =>
                                    this.handleInputChange(
                                      e,
                                      'discovery',
                                      'access',
                                      'collection_ids2'
                                    )
                                  }
                                />
                              </td>
                            </tr>
                            <tr>
                              <td className="my-textbox-row">
                                <TextInput
                                  class="my-textbox"
                                  labelText="Account Style"
                                  value={
                                    this.state.configData.discovery.utility_bill
                                      .account_style
                                  }
                                  onChange={(e) =>
                                    this.handleInputChange(
                                      e,
                                      'discovery',
                                      'utility_bill',
                                      'account_style'
                                    )
                                  }
                                />
                              </td>
                            </tr>
                            <tr>
                              <td className="my-textbox-row">
                                <TextInput
                                  class="my-textbox"
                                  labelText="Location"
                                  value={
                                    this.state.configData.discovery.utility_bill
                                      .location
                                  }
                                  onChange={(e) =>
                                    this.handleInputChange(
                                      e,
                                      'discovery',
                                      'utility_bill',
                                      'location'
                                    )
                                  }
                                />
                              </td>
                            </tr>
                            </tbody>
                          </table>
                        </div>
                      </section>
                      <section className="top-section">
                        <Button
                          className="fin-button-1"
                          onClick={this.handleSubmit}
                          disabled={this.state.loading}
                        >
                          Save
                        </Button>
                      </section>
                    </div>
                  )}
                </div>
              </TabPanel>
            </TabPanels>
          </Tabs>
        </Column>
      </Grid>
    );
  }
}
export default InvoicePage;
