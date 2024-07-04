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

import DataTable from '../../components/DataTable/DataTable';
import EnvUtility from '../../components/EnvUtility/EnvUtility';

import '../../components/css/common.css'; // Import the CSS file for styling

class TurboPage extends Component {
  constructor() {
    super();
    this.state = {
      loading: true,
      configData: null,
      locationData: [],
      accountsData: [],
      myAccountsData: null,
    };
    this.envUtility = new EnvUtility();
  }

  getStartDateForDisplay() {
    var returnValue = '';
    if (this.state.configData)
      if ('turbo' in this.state.configData)
        if ('parameters' in this.state.configData.turbo)
          if ('start_date' in this.state.configData.turbo.parameters)
            returnValue = this.state.configData?.turbo.parameters.start_date;

    return returnValue;
  }

  getEndDateForDisplay() {
    var returnValue = '';
    if (this.state.configData)
      if ('turbo' in this.state.configData)
        if ('parameters' in this.state.configData.turbo)
          if ('end_date' in this.state.configData.turbo.parameters)
            returnValue = this.state.configData?.turbo.parameters.end_date;

    return returnValue;
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
        this.setState((prevData) => {
          const newData = { ...prevData };
          newData.configData = response.data;
          newData.loading = false;
          newData.locationData = [];
          newData.accountsData = [];
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
  handleCommon = (event, myAPI) => {
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

    var my_URL = this.envUtility.getAPIUrl() + myAPI;
    axios
      .post(my_URL, this.state.configData, { headers })
      .then((response) => {
        this.setState((prevData) => {
          const newData = { ...prevData };
          newData.configData = response.data.inputPayload;
          newData.locationData = response.data.locationData;
          newData.accountsData = response.data.accountsData;
          newData.myAccountsData = response.data.myAccountsData;
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

  handleIngest = (event) => {
    return this.handleCommon(event, '/api/turbo/queryForIngest');
  };
  handleView = (event) => {
    return this.handleCommon(event, '/api/turbo/queryForView');
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
          <span className="SubHeaderTitle">Turbonomic Integration</span>
        </Column>
        <Column lg={16} md={8} sm={4} className="landing-page__r2">
          <div className="my-component">
            <section className="top-section">
              <div className="text-sub-heading">Turbonomic</div>
              <div className="text-sub-heading-label2">
                Integrate your Turbonomoic Sustainablity data into Envizi ESG
                Suite
              </div>
              <div className="upload-section">
                <table>
                  <tbody>
                    <tr>
                      <td className="my-textbox-row">
                        <TextInput
                          className="my-textbox"
                          labelText="Start Date"
                          value={this.getStartDateForDisplay()}
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
                          className="my-textbox"
                          labelText="End Date"
                          value={this.getEndDateForDisplay()}
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
                    <tr>
                      <td className="my-textbox-row"></td>
                    </tr>
                    <tr>
                      <td className="my-textbox-row">
                        <Button
                          className="fin-button-1"
                          onClick={(e) => this.handleView(e)}
                          disabled={this.state.loading}
                        >
                          Preview
                        </Button>{' '}
                        &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;
                        <Button
                          className="fin-button-1"
                          onClick={(e) => this.handleIngest(e)}
                          disabled={this.state.loading}
                        >
                          Ingest to Envizi
                        </Button>
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
                  </tbody>
                </table>
              </div>
            </section>
            <section className="top-section">
              <div className="text-sub-heading">Turbonomic Data</div>
              <div className="text-sub-heading-label2">
                Turbonomic Data retrived for Integrations
              </div>
              <div className="upload-section">
                <DataTable
                  jsonData={this.state.locationData}
                  headingText={'Groups & Locations'}
                />
                {this.state.myAccountsData !== null ? (
                  <div>
                    <DataTable
                      jsonData={this.state.myAccountsData.energy_consumption}
                      headingText={'Accounts and Data - Energy Consumption'}
                    />
                    <DataTable
                      jsonData={this.state.myAccountsData.active_hosts}
                      headingText={'Accounts and Data - Active Hosts'}
                    />
                    <DataTable
                      jsonData={this.state.myAccountsData.active_vms}
                      headingText={'Accounts and Data - Active VMs'}
                    />
                    <DataTable
                      jsonData={this.state.myAccountsData.energy_host_intensity}
                      headingText={'Accounts and Data - Energy Host Intensity'}
                    />
                    <DataTable
                      jsonData={this.state.myAccountsData.vm_host_density}
                      headingText={'Accounts and Data - VM Host Density'}
                    />
                  </div>
                ) : (
                  <p></p>
                )}
              </div>
            </section>
          </div>
        </Column>
      </Grid>
    );
  }
}
export default TurboPage;
