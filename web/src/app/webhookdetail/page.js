'use client';
import React, { Component } from 'react';
import MyUtility from './utility'; // Import the utility class

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
  Dropdown,
} from 'carbon-components-react';
import {
  Table,
  TableHead,
  TableRow,
  TableHeader,
  TableBody,
  TableCell,
  Link,
} from '@carbon/react';
import axios from 'axios';

import {
  Advocate,
  Globe,
  AcceleratingTransformation,
} from '@carbon/pictograms-react';
import { API_URL } from '../../components/common-constants.js';
import CarbonTable from '@/components/CarbonTable/CarbonTable';
import CarbonTableSimple from '@/components/CarbonTableSimple/CarbonTableSimple';

import { Add, TrashCan } from '@carbon/react/icons';

import '../../components/css/common.css'; // Import the CSS file for styling
import ApiUtility from '@/components/ApiUtility/ApiUtility'; // Import the utility class

class WebhookDetailPage extends Component {
  constructor() {
    super();
    this.apiUtility = new ApiUtility();
    this.myUtility = new MyUtility();
    this.state = {
      loading: false,
      main_data: null,

      resultIngest: null,
      msg_process : null,
      msg_save : null,

      // locations: [],
      // accounts: [],
    };
  }

  componentDidMount() {
    this.handlePageOnLoad();
  }

  handlePageOnLoad() {
    // Read the Query param
    const queryParams = new URLSearchParams(window.location.search);
    const action = queryParams.get('action');
    const id = queryParams.get('id');

    console.log('handlePageOnLoad action : ---> ' + action);
    console.log('handlePageOnLoad id : ---> ' + id);

    if (action === "new") {
      this.handleNew();
    } else if (action === "load") {
      this.handleLoad(id);
    } else if (action === "clone") {
      this.handleClone(id);
    }
  }

  // Function to add a new element after a specific index
  addItemAfterIndex = (newItem, index) => {
    setItems((prevItems) => [
      ...prevItems.slice(0, index + 1),
      newItem,
      ...prevItems.slice(index + 1),
    ]);
  };

  // Function to find index based on ID and add a new element after that index
  addNewElementAfterId = (id, newItem) => {
    const index = items.findIndex((item) => item.id === id);
    if (index !== -1) {
      addItemAfterIndex(newItem, index);
    }
  };

  findItemIndexByName = (name) => {
    const myData = this.state.main_data.fields;

    for (let i = 0; i < myData.length; i++) {
      const item = myData[i];
      if (item.name === name) {
        return i;
      }
    }
    return -1;
  };

  // Function to handle adding a new field to a section
  addField = (name, index) => {
    const fieldIndex = this.findItemIndexByName(name);
    if (fieldIndex !== -1) {
      const element = this.myUtility.getJsonDataType2();
      const item = this.state.main_data.fields[fieldIndex];
      item.list.splice(index, 0, element);

      this.setState((prevData) => {
        const newData = { ...prevData };
        newData.main_data.fields[fieldIndex].list = item.list;
        return newData;
      });
    }
  };

  // Function to handle adding a new field to a section
  removeField = (name, index) => {
    const fieldIndex = this.findItemIndexByName(name);
    if (fieldIndex !== -1) {
      const item = this.state.main_data.fields[fieldIndex];
      // Remove 1 element at the specified index
      item.list.splice(index, 1);

      this.setState((prevData) => {
        const newData = { ...prevData };
        newData.main_data.fields[fieldIndex].list = item.list;
        return newData;
      });
    }
  };

  handleInputChange = (event, name) => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.main_data[name] = event.target.value;
      return newData;
    });
  };
  handleDropDownChange = (event, name) => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.main_data[name] = event.selectedItem;
      return newData;
    });
  };

  handleEnviziTemplateDropDownChange = (event, name) => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.main_data[name] = event.selectedItem;
      newData.resultIngest = null;
      this.handleTemplateChange();
      return newData;
    });

  };


  handleTextValueChange = (event, name1, name2) => {
    const fieldIndex = this.findItemIndexByName(name1);
    if (fieldIndex !== -1) {
      this.setState((prevData) => {
        const newData = { ...prevData };
        newData.main_data.fields[fieldIndex][name2] = event.target.value;
        return newData;
      });
    }
  };

  handleListValueChange = (event, name1, name2) => {
    const fieldIndex = this.findItemIndexByName(name1);
    if (fieldIndex !== -1) {
      this.setState((prevData) => {
        const newData = { ...prevData };
        newData.main_data.fields[fieldIndex][name2] = event.selectedItem;
        return newData;
      });
    }
  };


  handleSubTextValueChange = (event, name1, name2, index) => {
    const fieldIndex = this.findItemIndexByName(name1);
    console.log("field Index : " + fieldIndex)
    if (fieldIndex !== -1) {
      this.setState((prevData) => {
        const newData = { ...prevData };
        newData.main_data.fields[fieldIndex].list[index][name2] = event.target.value;
        return newData;
      });
    }
  };

  handleOperationListValueChange = (event, name, index) => {
    const fieldIndex = this.findItemIndexByName(name);
    if (fieldIndex !== -1) {
      this.setState((prevData) => {
        const newData = { ...prevData };
          newData.main_data.fields[fieldIndex].list[index].operation_value = event.selectedItem;
        return newData;
      });
    }
  };

  handleBack = () => {
    console.log("handle back...")
    window.location.href = '/webhooks';
  };

  handleNew() {
    const myPayload = {};
    this.postRequest('/api/webhook/loadnew', null, null, this.sucessCallBackLoadNew, myPayload);
  }

  handleLoad(id) {
    const myPayload = { id: id,};
    this.postRequest('/api/webhook/load', null, null, this.sucessCallBackLoad, myPayload);
  }


  handleTemplateChange() {
    const myPayload = this.state.main_data;
    this.postRequest('/api/webhook/templatechange', this.startLoading, this.stopLoading, this.sucessCallBackTemplateChange, myPayload);
  }

  handleClone(id) {
    const myPayload = { id: id,};
    this.postRequest('/api/webhook/load', null, null, this.sucessCallBackClone, myPayload);
  }

  handleSave = (event) => {
    this.postRequest('/api/webhook/save', this.startLoading, this.stopLoading, this.sucessCallBackSave, this.state.main_data);
  };

  handleViewInScreen = () => {
    this.postRequest('/api/webhook/viewInScreen', this.startLoading, this.stopLoading, this.sucessCallBackViewInScreen, this.state.main_data);
  };

  handleIngestToEnvizi =  () => {
    this.postRequest('/api/webhook/ingestToEnvizi',  this.startLoading, this.stopLoading, this.sucessCallBackIngestToEnvizi, this.state.main_data);
  }

  handleWebhookRefresh = () => {
    this.postRequest('/api/webhook/load_webhook_response', this.startLoading, this.stopLoading, this.sucessCallBackWebhookRefresh, this.state.main_data);
  };

  sucessCallBackLoadNew = (resp) => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.main_data = resp.data;
      newData.webhook_response = null;
      newData.loading = false;
      return newData;
    });
  };

  sucessCallBackTemplateChange = (resp) => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.main_data = resp.data;
      newData.loading = false;
      return newData;
    });
  };

  sucessCallBackLoadNew = (resp) => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.main_data = resp.data;
      newData.excel_response = resp.excel_response;
      newData.loading = false;
      return newData;
    });
  };


  
  sucessCallBackViewInScreen = (resp) => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.resultIngest = resp;
      newData.loading = false;
      newData.msg_process = resp.msg;
      return newData;
    });
  };

  sucessCallBackIngestToEnvizi = (resp) => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.resultIngest = resp;
      newData.msg_process = resp.msg;
      newData.loading = false;
      return newData;
    });
  };

  sucessCallBackLoad = (resp) => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.main_data = resp.data;
      newData.webhook_response = resp.webhook_response;
      newData.loading = false;
      return newData;
    });
  };

  sucessCallBackClone = (resp) => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.main_data = resp.data;
      newData.main_data_response = resp.webhook_response;
      newData.main_data.id = "";
      newData.loading = false;
      return newData;
    });
  };

  sucessCallBackSave = (resp) => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.main_data = resp.data;
      newData.webhook_response = resp.webhook_response;
      newData.msg_save = resp.msg;
      newData.loading = false;
      return newData;
    });
  };


  sucessCallBackWebhookRefresh = (resp) => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.webhook_response = resp.data;
      newData.msg_refresh = resp.msg;
      newData.loading = false;
      return newData;
    });
  };

  startLoading = () => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.msg = null;
      newData.msg_save = null;
      newData.msg_process = null;
      newData.msg_refresh = null;
      newData.loading = true;
      return newData;
    });
  }

  stopLoading  = (error)=> {
    console.log(error);
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.loading = false;
      return newData;
    });
  }

  postRequest = (url, startCallBack, errorCallBack, sucesssCallBack, myPayload) => {
    this.apiUtility.postRequest(url,startCallBack, errorCallBack, sucesssCallBack, myPayload)
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
          <span className="SubHeaderTitle">Webhook Details</span>
        </Column>

        {this.state.main_data && (
          <Column lg={16} md={8} sm={4} className="landing-page__r2">
            <div className="my-component">
              <section className="top-section">
                <div className="text-sub-heading">Meta info</div>
                {/* <div className="text-sub-heading-label2">
                        Envizi AWS S3 access details
                      </div> */}
                <div className="upload-section">
                  <table>
                    <tbody>
                      <tr>
                        <td className="my-textbox-row">
                          <TextInput
                            class="my-textbox"
                            labelText="Id"
                            value={this.state.main_data.id}
                            disabled={true}
                            onChange={(e) => this.handleInputChange(e, 'id')}
                          />
                        </td>
                      </tr>
                      <tr>
                        <td className="my-textbox-row">
                          <TextInput
                            class="my-textbox"
                            labelText="Name"
                            value={this.state.main_data.name}
                            onChange={(e) => this.handleInputChange(e, 'name')}
                          />
                        </td>
                      </tr>
                      <tr>
                        <td className="my-textbox-row">
                          <TextInput
                            class="my-textbox"
                            labelText="Desc"
                            value={this.state.main_data.desc}
                            onChange={(e) => this.handleInputChange(e, 'desc')}
                          />
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </section>
            </div>
            <div className="my-component">
              <section className="top-section">
                <div className="text-sub-heading">Webhook Access</div>
                {/* <div className="text-sub-heading-label2">
                        Envizi AWS S3 access details
                      </div> */}
                <div className="upload-section">
                  <table>
                    <tbody>
                      <tr>
                        <td className="my-textbox-row">
                          <Dropdown
                              className="gan-dropdown-operation"
                              titleText="Http Method"
                              items={this.state.main_data.http_method_list}
                              selectedItem={this.state.main_data.http_method}
                              onChange={(e) =>
                                this.handleDropDownChange(e, 'http_method')
                              }
                            ></Dropdown>
                        </td>
                      </tr>
                      <tr>
                        <td className="my-textbox-row">
                          <TextInput
                            class="my-textbox"
                            labelText="URL"
                            value={this.state.main_data.url}
                            onChange={(e) => this.handleInputChange(e, 'url')}
                          />
                        </td>
                      </tr>
                      <tr>
                        <td className="my-textbox-row">
                          <TextInput
                            class="my-textbox"
                            labelText="Bearer Token"
                            type="password"
                            value={this.state.main_data.token}
                            onChange={(e) => this.handleInputChange(e, 'token')}
                          />
                        </td>
                      </tr>
                      <tr>
                        <td className="my-textbox-row">
                          <TextInput
                            class="my-textbox"
                            labelText="User"
                            value={this.state.main_data.user}
                            onChange={(e) => this.handleInputChange(e, 'user')}
                          />
                        </td>
                      </tr>
                      <tr>
                        <td className="my-textbox-row">
                          <TextInput
                            class="my-textbox"
                            labelText="Password"
                            type="password"
                            value={this.state.main_data.password}
                            onChange={(e) =>
                              this.handleInputChange(e, 'password')
                            }
                          />
                        </td>
                      </tr>
                      <tr>
                        <td className="my-textbox-row">
                          <TextInput
                            class="my-textbox"
                            labelText="API Key Name"
                            value={this.state.main_data.api_key_name}
                            onChange={(e) =>
                              this.handleInputChange(e, 'api_key_name')
                            }
                          />
                        </td>
                        
                      </tr>
                      <tr>
                        <td className="my-textbox-row">
                          <TextInput
                            class="my-textbox"
                            labelText="API Key Value"
                            type="password"
                            value={this.state.main_data.api_key_value}
                            onChange={(e) =>
                              this.handleInputChange(e, 'api_key_value')
                            }
                          />
                        </td>
                        
                      </tr>   

                        <tr>
                        <td className="my-textbox-row">
                          <TextInput
                            class="my-textbox"
                            labelText="Firewall URL"
                            value={this.state.main_data.firewall_url}
                            onChange={(e) => this.handleInputChange(e, 'firewall_url')}
                          />
                        </td>
                      </tr>
                      <tr>
                        <td className="my-textbox-row">
                          <TextInput
                            class="my-textbox"
                            labelText="Firewall User"
                            value={this.state.main_data.firewall_user}
                            onChange={(e) => this.handleInputChange(e, 'firewall_user')}
                          />
                        </td>
                      </tr>
                      <tr>
                        <td className="my-textbox-row">
                          <TextInput
                            class="my-textbox"
                            labelText="Firewall Password"
                            type="password"
                            value={this.state.main_data.firewall_password}
                            onChange={(e) =>
                              this.handleInputChange(e, 'firewall_password')
                            }
                          />
                        </td>
                      </tr>                                         
                    </tbody>
                  </table>
                </div>
              </section>
            </div>
            <div className="my-component">
              <section className="top-section">
                <div className="text-sub-heading">Template Type</div>
                {/* <div className="text-sub-heading-label2">
                        Envizi AWS S3 access details
                      </div> */}
                <div className="upload-section">
                  <table>
                    <tbody>
                      <tr>
                        <td className="my-textbox-row">
                          <Dropdown
                            className="gan-dropdown-operation"
                            titleText="Envizi Template"
                            items={this.state.main_data.envizi_template_list}
                            selectedItem={this.state.main_data.envizi_template}
                            onChange={(e) =>
                              this.handleEnviziTemplateDropDownChange(e, 'envizi_template')
                            }
                          />
                        </td>
                      </tr>
                      <tr>
                        <td className="my-textbox-row">
                          <Dropdown
                            className="gan-dropdown-operation"
                            titleText="Webhook Data Template Type"
                            items={this.state.main_data.data_template_type_list}
                            selectedItem={this.state.main_data.data_template_type}
                            onChange={(e) =>
                              this.handleDropDownChange(e, 'data_template_type')
                            }
                          ></Dropdown>
                        </td>
                      </tr>
                      <tr>
                        <td className="my-textbox-row">
                          <TextInput
                            class="my-textbox"
                            labelText="Multiple Records Field"
                            value={this.state.main_data.multiple_records_field}
                            onChange={(e) =>
                              this.handleInputChange(
                                e,
                                'multiple_records_field'
                              )
                            }
                          />
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </section>
            </div>

            <div className="my-component">
              <section className="top-section">
                <div className="text-sub-heading">Webhook Response</div>
                {
                  <div className="text-sub-heading-label2">
                    The response data from Webhook for reference and for data
                    mapping.
                  </div>
                }
                <div className="upload-section">
                  <table className="full-width-table">
                    <tbody>
                      <tr>
                        <td className="my-textbox-row">
                          <textarea
                            rows="9"
                            className="full-width-textarea"
                            name="webhook-response"
                            value={JSON.stringify(
                              this.state.webhook_response,
                              null,
                              2
                            )}
                            placeholder="Result"
                          />
                        </td>
                      </tr>
                      <tr>
                        <td className="my-textbox-row">
                          <Button
                            className="fin-button-1"
                            onClick={this.handleWebhookRefresh}
                          >
                            Refresh
                          </Button>
                        </td>
                      </tr>
                      <tr>
                        <td className="my-textbox-row">
                          <div>
                            <span className="instruction-msg">
                              {this.state.msg_refresh}
                            </span>
                          </div>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </section>
            </div>





            <div className="my-component">
              <section className="top-section">
                <div className="text-sub-heading">Data Ingestion to Envizi</div>
                {
                  <div className="text-sub-heading-label2"> 
                    Preview the Envizi data generated based on the Webhook mapping and Ingest into Envizi
                  </div>
                }


                <div className="upload-section">
                  <table className="full-width-table">
                    <tbody>
                      <tr>
                        <td className="my-textbox-row">
                        <div className="fin-mapping-container">

                        <div className="fin-row">
                            <div className="fin-column">
                              <Button className="fin-button-1"  onClick={this.handleViewInScreen}
                              >Preview </Button>
                            </div>              
                            <div className="fin-column">
                            <Button className="fin-button-1" 
                              onClick={this.handleIngestToEnvizi}
                              >
                                Ingest to Envizi
                              </Button>
                            </div>              
                            <div className="fin-column">
                              <Button className="fin-button-1" onClick={ this.handleBack } >
                                  Back
                              </Button>
                            </div>      
                            <div className="fin-row">
                              <div className="instruction-msg"> 
                                  {this.state.msg_process &&
                                    this.state.msg_process.msg}
                              </div>
                            </div>
                          </div>
                        </div>

                        </td>
                      </tr>
                      <tr>
                        <td className="my-textbox-row">
                          <div>
                            <span className="instruction-msg">
                              {this.state.msg_process}
                            </span>
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
                        <td className="my-textbox-row">
                        {this.state.resultIngest &&
                            this.state.resultIngest.processed_data && (
                              <span>
                              <CarbonTable
                                columns={ this.state.resultIngest.template_columns }
                                jsonData={ this.state.resultIngest.processed_data}
                                headingText1={'Data Preview'}
                                headingText2={'The below data would be generated and pushed to Envizi'}
                              />
                              {this.state.resultIngest.validation_errors && Object.keys(this.state.resultIngest.validation_errors).length > 0 && (
                                  <CarbonTableSimple
                                    columns={ ["Error", "Rows"] }
                                    jsonData={ this.state.resultIngest.validation_errors}
                                    headingText1={'Validation Errors'}
                                    headingText2={'The below validation errors occured in the data'}
                                  />
                              )}
                              </span>
                            )}
                        </td>
                      </tr>


                    </tbody>
                  </table>
                  </div>
              </section>
            </div>


            <div className="my-component">
              <section className="top-section">
                <div className="text-sub-heading">Data Mapping</div>
                <div className="text-sub-heading-label2">
                  Map the data from webhook returned json file to the template
                  columns
                </div>
                <div className="upload-section">
                  <div className="fin-container">
                    {!this.state.loading &&
                      this.state.main_data &&
                      this.state.main_data.fields &&
                      this.state.main_data.fields.map((item, index) => (
                        <div className="fin-mapping-container">
                          <div className="fin-row">
                            <div className="fin-column">
                              <div className="fin-field-label">
                                {item.label}
                              </div>
                            </div>
                            <div className="fin-column">
                              <TextInput
                                className="fin-text-box"
                                // labelText="Free Text"
                                value={item.text_value}
                                size="md"
                                onChange={(e) =>
                                  this.handleTextValueChange(
                                    e,
                                    item.name,
                                    'text_value'
                                  )
                                }
                              />
                            </div>
                            <div className="fin-column">
                              <TextInput
                                className="fin-text-box"
                                // labelText="Mapping field"
                                value={item.map_value}
                                size="md"
                                onChange={(e) =>
                                  this.handleTextValueChange(
                                    e,
                                    item.name,
                                    'map_value'
                                  )
                                }
                              />
                            </div>
                            { <div className="fin-column">
                              {item.type == 3 && (
                                <Dropdown
                                  className="gan-dropdown-existing-values"
                                  // titleText="Existing Values"
                                  items={item.list_elements}
                                  size="md"
                                  type="default" // Set type to "default" for single-select behavior
                                  selectedItem={item.list_value}
                                  onChange={(e) => this.handleListValueChange(e, item.name, 'list_value')}
                                />
                              )}
                            </div> }
                          </div>
                          <div className="fin-mapping-container2">
                            {item.list.map((subitem, index) => (
                              <div className="fin-row">
                              <div className="fin-field-label">
                              </div>                                
                                <div className="fin-column">
                                  <TextInput
                                    className="fin-text-box1"
                                    // labelText="Free Text"
                                    value={subitem.text_value}
                                    // size="md"
                                    onChange={(e) =>
                                      this.handleSubTextValueChange(
                                        e,
                                        item.name,
                                        'text_value',
                                        index
                                      )
                                    }
                                  />
                                </div>
                                <div className="fin-column">
                                  <TextInput
                                    className="fin-text-box1"
                                    // labelText="Free Text"
                                    value={subitem.map_value}
                                    // size="md"
                                    onChange={(e) =>
                                      this.handleSubTextValueChange(
                                        e,
                                        item.name,
                                        'map_value',
                                        index
                                      )
                                    }
                                  />
                                </div>
                                <div className="fin-column">
                                  <Dropdown
                                    className="gan-dropdown-operation"
                                    // titleText="Operation"
                                    items={subitem.operation_elements}
                                    selectedItem={subitem.operation_value}
                                    // defaultSelectedItems={[subitem.operation_value]}
                                    // size="md"
                                    onChange={(e) =>
                                      this.handleOperationListValueChange(
                                        e,
                                        item.name,
                                        index
                                      )
                                    }
                                  />
                                </div>
                                <div className="fin-column">
                                  <Button
                                    // kind="secondary"
                                    className="fin-button-icon"
                                    hasIconOnly
                                    renderIcon={Add}
                                    iconDescription="Add"
                                    size="sm"
                                    onClick={() =>
                                      this.addField(item.name, index + 1)
                                    }
                                  />
                                  <Button
                                    // kind="secondary"
                                    className="fin-button-icon"
                                    hasIconOnly
                                    renderIcon={TrashCan}
                                    iconDescription="Delete"
                                    size="sm"
                                    onClick={() =>
                                      this.removeField(item.name, index)
                                    }
                                  />
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      ))}
                    <div className="fin-mapping-container">
                      <div className="fin-row">
                        <div className="fin-column">
                          <Button
                            className="fin-button-1"
                            onClick={this.handleSave}
                          >
                            Save
                          </Button>
                        </div>
                        <div className="fin-column">
                          <Button
                            className="fin-button-1"x
                            onClick={this.handleBack}
                          >
                            Back
                          </Button>
                        </div>
                      </div>
                      <div className="fin-row">
                        <div>
                          <span className="instruction-msg">
                            {this.state.msg_save}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </section>
            </div>


          </Column>
        )}
      </Grid>
    );
  }
}
export default WebhookDetailPage;
