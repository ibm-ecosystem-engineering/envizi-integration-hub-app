'use client';
import React, { Component } from 'react';
import { unstable_noStore as noStore } from 'next/cache';

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
import { API_URL } from '../../components/common-constants.js';
import DataTable from '../../components/DataTable/DataTable';
import EnvUtility from '../../components/EnvUtility/EnvUtility';

import Image from 'next/image.js';
import '../../components/css/common.css'; // Import the CSS file for styling
import invoiceImage from './images/invoice.png'; // Import the image file

class ConfigPage extends Component {
  constructor() {
    super();
    this.state = {
      loading: true,
      configData: null,
      loadingInvoice: false,
      resultProcessInvoice: '',
      loadingUtility: false,
      resultProcessUtility: '',
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
          className="landing-page__banner  my-title-image"
        >
          <span className="SubHeaderTitle">Configuration Settings</span>
        </Column>
        <Column lg={16} md={8} sm={4} className="landing-page__r2">
          <Tabs defaultSelectedIndex={0}>
            <TabList className="tabs-group" aria-label="Page navigation">
              <Tab>Envizi</Tab>
              <Tab>Turbonomic</Tab>
              <Tab>Invoices</Tab>
            </TabList>
            <TabPanels>
              <TabPanel>
                {!this.state.loading && this.state.configData && (
                  <div className="my-component">
                    <section className="top-section">
                      <div className="text-sub-heading">Envizi S3 Access</div>
                      <div className="text-sub-heading-label2">
                        Envizi AWS S3 access details
                      </div>
                      <div className="upload-section">
                        <table>
                          <tr>
                            <td className="my-textbox-row">
                              <TextInput
                                class="my-textbox"
                                labelText="Aws Bucket Name"
                                value={
                                  this.state.configData.envizi.access
                                    .bucket_name
                                }
                                onChange={(e) =>
                                  this.handleInputChange(
                                    e,
                                    'envizi',
                                    'access',
                                    'bucket_name'
                                  )
                                }
                              />
                            </td>
                          </tr>
                          <tr>
                            <td className="my-textbox-row">
                              <TextInput
                                class="my-textbox"
                                labelText="Aws Folder Name"
                                value={
                                  this.state.configData.envizi.access
                                    .folder_name
                                }
                                onChange={(e) =>
                                  this.handleInputChange(
                                    e,
                                    'envizi',
                                    'access',
                                    'folder_name'
                                  )
                                }
                              />
                            </td>
                          </tr>
                          <tr>
                            <td className="my-textbox-row">
                              <TextInput
                                class="my-textbox"
                                labelText="Enter Aws Access Key"
                                type="password"
                                value={
                                  this.state.configData.envizi.access.access_key
                                }
                                onChange={(e) =>
                                  this.handleInputChange(
                                    e,
                                    'envizi',
                                    'access',
                                    'access_key'
                                  )
                                }
                              />
                            </td>
                          </tr>
                          <tr>
                            <td className="my-textbox-row">
                              <TextInput
                                class="my-textbox"
                                labelText="Aws Secret Key"
                                type="password"
                                value={
                                  this.state.configData.envizi.access.secret_key
                                }
                                onChange={(e) =>
                                  this.handleInputChange(
                                    e,
                                    'envizi',
                                    'access',
                                    'secret_key'
                                  )
                                }
                              />
                            </td>
                          </tr>
                        </table>
                      </div>
                    </section>
                    <section className="top-section">
                      <div className="text-sub-heading">Envizi Parameters</div>
                      <div className="text-sub-heading-label2">
                        Envizi Parameters details
                      </div>
                      <div className="upload-section">
                        <table>
                          <tr>
                            <td className="my-textbox-row">
                              <TextInput
                                class="my-textbox"
                                labelText="Org Name"
                                value={
                                  this.state.configData.envizi.parameters
                                    .org_name
                                }
                                onChange={(e) =>
                                  this.handleInputChange(
                                    e,
                                    'envizi',
                                    'parameters',
                                    'org_name'
                                  )
                                }
                              />
                            </td>
                          </tr>
                          <tr>
                            <td className="my-textbox-row">
                              <TextInput
                                class="my-textbox"
                                labelText="Org Link"
                                value={
                                  this.state.configData.envizi.parameters
                                    .org_link
                                }
                                onChange={(e) =>
                                  this.handleInputChange(
                                    e,
                                    'envizi',
                                    'parameters',
                                    'org_link'
                                  )
                                }
                              />
                            </td>
                          </tr>
                          <tr>
                            <td className="my-textbox-row">
                              <TextInput
                                class="my-textbox"
                                labelText="Prefix"
                                value={
                                  this.state.configData.envizi.parameters.prefix
                                }
                                onChange={(e) =>
                                  this.handleInputChange(
                                    e,
                                    'envizi',
                                    'parameters',
                                    'prefix'
                                  )
                                }
                              />
                            </td>
                          </tr>
                        </table>
                      </div>
                    </section>
                    <section className="top-section">
                      <div className="text-sub-heading">Envizi API</div>
                      <div className="text-sub-heading-label2">
                        Envizi API details
                      </div>
                      <div className="upload-section">
                        <table>
                          <tr>
                            <td className="my-textbox-row">
                              <TextInput
                                class="my-textbox"
                                labelText="API URL"
                                value={this.state.configData.envizi.api.url}
                                onChange={(e) =>
                                  this.handleInputChange(
                                    e,
                                    'envizi',
                                    'api',
                                    'url'
                                  )
                                }
                              />
                            </td>
                          </tr>
                          <tr>
                            <td className="my-textbox-row">
                              <TextInput
                                class="my-textbox"
                                labelText="API Token"
                                type="password"
                                value={this.state.configData.envizi.api.token}
                                onChange={(e) =>
                                  this.handleInputChange(
                                    e,
                                    'envizi',
                                    'api',
                                    'token'
                                  )
                                }
                              />
                            </td>
                          </tr>
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
              </TabPanel>
              <TabPanel>
                {!this.state.loading && this.state.configData && (
                  <div className="my-component">
                    <section className="top-section">
                      <div className="text-sub-heading">Turbonomic Access</div>
                      <div className="text-sub-heading-label2">
                        Turbonomic Access details
                      </div>
                      <div className="upload-section">
                        <table>
                          <tr>
                            <td className="my-textbox-row">
                              <TextInput
                                class="my-textbox"
                                labelText="URL"
                                value={this.state.configData.turbo.access.url}
                                onChange={(e) =>
                                  this.handleInputChange(
                                    e,
                                    'turbo',
                                    'access',
                                    'url'
                                  )
                                }
                              />
                            </td>
                          </tr>
                          <tr>
                            <td className="my-textbox-row">
                              <TextInput
                                class="my-textbox"
                                labelText="User"
                                value={this.state.configData.turbo.access.user}
                                onChange={(e) =>
                                  this.handleInputChange(
                                    e,
                                    'turbo',
                                    'access',
                                    'user'
                                  )
                                }
                              />
                            </td>
                          </tr>
                          <tr>
                            <td className="my-textbox-row">
                              <TextInput
                                class="my-textbox"
                                labelText="Password"
                                type="password"
                                value={
                                  this.state.configData.turbo.access.password
                                }
                                onChange={(e) =>
                                  this.handleInputChange(
                                    e,
                                    'turbo',
                                    'access',
                                    'password'
                                  )
                                }
                              />
                            </td>
                          </tr>
                        </table>
                      </div>
                    </section>

                    <section className="top-section">
                      <div className="text-sub-heading">
                        Turbonomic Parameters
                      </div>
                      <div className="text-sub-heading-label2">
                        Turbonomic Parameters details
                      </div>
                      <div className="upload-section">
                        <table>
                          <tr>
                            <td className="my-textbox-row">
                              <TextInput
                                class="my-textbox"
                                labelText="Group Name"
                                value={
                                  this.state.configData.turbo.parameters.group
                                }
                                onChange={(e) =>
                                  this.handleInputChange(
                                    e,
                                    'turbo',
                                    'parameters',
                                    'group'
                                  )
                                }
                              />
                            </td>
                          </tr>
                          <tr>
                            <td className="my-textbox-row">
                              <TextInput
                                class="my-textbox"
                                labelText="Sub Group Name"
                                value={
                                  this.state.configData.turbo.parameters
                                    .sub_group
                                }
                                onChange={(e) =>
                                  this.handleInputChange(
                                    e,
                                    'turbo',
                                    'parameters',
                                    'sub_group'
                                  )
                                }
                              />
                            </td>
                          </tr>
                        </table>
                      </div>
                    </section>
                    <section className="top-section">
                      <div className="text-sub-heading">Turbonomic Filter</div>
                      <div className="text-sub-heading-label2">
                        Turbonomic Filter details
                      </div>
                      <div className="upload-section">
                        <table>
                          <tr>
                            <td className="my-textbox-row">
                              <TextInput
                                class="my-textbox"
                                labelText="Start Date"
                                value={
                                  this.state.configData.turbo.parameters
                                    .start_date
                                }
                                onChange={(e) =>
                                  this.handleInputChange(
                                    e,
                                    'turbo',
                                    'parameters',
                                    'start_date'
                                  )
                                }
                              />
                            </td>
                          </tr>
                          <tr>
                            <td className="my-textbox-row">
                              <TextInput
                                class="my-textbox"
                                labelText="End Date"
                                value={
                                  this.state.configData.turbo.parameters
                                    .end_date
                                }
                                onChange={(e) =>
                                  this.handleInputChange(
                                    e,
                                    'turbo',
                                    'parameters',
                                    'end_date'
                                  )
                                }
                              />
                            </td>
                          </tr>
                        </table>
                      </div>
                    </section>
                    <section className="top-section">
                      <div className="text-sub-heading">
                        Turbonomic related Account Styles
                      </div>
                      <div className="text-sub-heading-label2">
                        Turbonomic related Account Styles details
                      </div>
                      <div className="upload-section">
                        <DataTable
                          jsonData={this.state.configData.turbo.account_styles}
                          headingText={'Turbonomic Account Styles'}
                        />
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
              </TabPanel>
              <TabPanel>
                {!this.state.loading && this.state.configData && (
                  <div className="my-component">
                    {/* Section at the top */}
                    {/* <section className="header-section">
                      <div className="text-heading">Configuration</div>
                      <div className="text-heading-label">
                        Configuration for Watson Discovery and Invoice Processing
                      </div>
                    </section> */}

                    <section className="top-section">
                      <div className="text-sub-heading">Discovery</div>
                      <div className="text-sub-heading-label2">
                        Watson Discovery configuration for Invoice and Utility
                        Bill Processing
                      </div>
                      <div className="upload-section">
                        <table>
                          <tr>
                            <td className="my-textbox-row">
                              <TextInput
                                class="my-textbox"
                                labelText="API Key"
                                type="password"
                                value={
                                  this.state.configData.discovery.access.api_key
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
                        </table>
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
                        </table>
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
              </TabPanel>
            </TabPanels>
          </Tabs>
        </Column>
      </Grid>
    );
  }
}
export default ConfigPage;
