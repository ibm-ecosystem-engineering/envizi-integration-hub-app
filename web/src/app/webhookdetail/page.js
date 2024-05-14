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
import { Add, TrashCan } from '@carbon/react/icons';

import '../../components/css/common.css'; // Import the CSS file for styling
import '../../components/css/new-common.css'; // Import the CSS file for styling
import ApiUtility from '@/components/ApiUtility/ApiUtility'; // Import the utility class

class WebhookDetailPage extends Component {
  constructor() {
    super();
    this.apiUtility = new ApiUtility();
    this.myUtility = new MyUtility();
    this.state = {
      loading: false,
      webhook: null,
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
    const myData = this.state.webhook.fields;

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
      const item = this.state.webhook.fields[fieldIndex];
      item.list.splice(index, 0, element);

      this.setState((prevData) => {
        const newData = { ...prevData };
        newData.webhook.fields[fieldIndex].list = item.list;
        return newData;
      });
    }
  };

  // Function to handle adding a new field to a section
  removeField = (name, index) => {
    const fieldIndex = this.findItemIndexByName(name);
    if (fieldIndex !== -1) {
      const item = this.state.webhook.fields[fieldIndex];
      // Remove 1 element at the specified index
      item.list.splice(index, 1);

      this.setState((prevData) => {
        const newData = { ...prevData };
        newData.webhook.fields[fieldIndex].list = item.list;
        return newData;
      });
    }
  };

  handleInputChange = (event, name) => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.webhook[name] = event.target.value;
      return newData;
    });
  };
  handleDropDownChange = (event, name) => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.webhook[name] = event.selectedItem;
      return newData;
    });
  };

  handleTextValueChange = (event, name1, name2) => {
    const fieldIndex = this.findItemIndexByName(name1);
    if (fieldIndex !== -1) {
      this.setState((prevData) => {
        const newData = { ...prevData };
        newData.webhook.fields[fieldIndex][name2] = event.target.value;
        return newData;
      });
    }
  };

  handleSubTextValueChange = (event, name1, name2, index) => {
    const fieldIndex = this.findItemIndexByName(name1);
    if (fieldIndex !== -1) {
      this.setState((prevData) => {
        const newData = { ...prevData };
        newData.webhook.fields[fieldIndex].list[index][name2] =
          event.target.value;
        return newData;
      });
    }
  };

  handleOperationListValueChange = (event, name, index) => {
    const fieldIndex = this.findItemIndexByName(name);
    if (fieldIndex !== -1) {
      this.setState((prevData) => {
        const newData = { ...prevData };
          newData.webhook.fields[fieldIndex].list[index].operation_value =
          event.selectedItem;
        return newData;
      });
    }
  };

  handleBack = (event) => {
    window.location.href = '/webhooks';
  };


  handleNew() {
      const myWebhook = this.myUtility.createEmptyWebhook();
      this.setState((prevData) => {
        const newData = { ...prevData };
        newData.webhook = myWebhook;
        newData.loading = false;
        return newData;
      });
  }

  handleLoad(id) {
    const myPayload = { id: id,};
    this.postRequest('/api/webhook/load', null, null, this.sucessCallBackLoad, myPayload);
  }

  handleClone(id) {
    const myPayload = { id: id,};
    this.postRequest('/api/webhook/load', null, null, this.sucessCallBackClone, myPayload);
  }

  handleSave = (event) => {
    this.postRequest('/api/webhook/save', this.startLoading, this.stopLoading, this.sucessCallBackSave, this.state.webhook);
  };

  handleConvert = (event) => {
    this.postRequest('/api/webhook/convert', this.startLoading, this.stopLoading, this.sucessCallBackConvert, this.state.webhook);
  };

  handleWebhookRefresh = (event) => {
    this.postRequest('/api/webhook/load_webhook_response', this.startLoading, this.stopLoading, this.sucessCallBackWebhookRefresh, this.state.webhook);
  };

  sucessCallBackLoad = (resp) => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.webhook = resp.data;
      newData.webhook_response = resp.webhook_response;
      newData.loading = false;
      return newData;
    });
  };

  sucessCallBackClone = (resp) => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.webhook = resp.data;
      newData.webhook_response = resp.webhook_response;
      newData.webhook.id = "";
      newData.loading = false;
      return newData;
    });
  };

  sucessCallBackSave = (resp) => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.save_msg = resp.msg;
      newData.webhook = resp.data;
      newData.webhook_response = resp.webhook_response;
      newData.loading = false;
      return newData;
    });
  };

  sucessCallBackConvert = (resp) => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.convert_msg = resp.msg;
      newData.convert_processed_data = resp.data;
      newData.template_columns = resp.template_columns;
      newData.loading = false;
      return newData;
    });
  };

  sucessCallBackWebhookRefresh = (resp) => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.refresh_msg = resp.msg;
      newData.webhook_response = resp.data;
      newData.loading = false;
      return newData;
    });
  };

  startLoading = () => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.msg = null;
      newData.save_msg = null;
      newData.convert_msg = null;
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
        {/* <Column lg={16} md={8} sm={4} className="landing-page__r2">
          <div className="my-component">
            {JSON.stringify(this.state.webhook, null, 2)}
          </div>
        </Column> */}

        {this.state.webhook && (
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
                            value={this.state.webhook.id}
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
                            value={this.state.webhook.name}
                            onChange={(e) => this.handleInputChange(e, 'name')}
                          />
                        </td>
                      </tr>
                      <tr>
                        <td className="my-textbox-row">
                          <TextInput
                            class="my-textbox"
                            labelText="Desc"
                            value={this.state.webhook.desc}
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
                              items={this.state.webhook.http_method_list}
                              selectedItem={this.state.webhook.http_method}
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
                            value={this.state.webhook.url}
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
                            value={this.state.webhook.token}
                            onChange={(e) => this.handleInputChange(e, 'token')}
                          />
                        </td>
                      </tr>
                      <tr>
                        <td className="my-textbox-row">
                          <TextInput
                            class="my-textbox"
                            labelText="User"
                            value={this.state.webhook.user}
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
                            value={this.state.webhook.password}
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
                            value={this.state.webhook.api_key_name}
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
                            value={this.state.webhook.api_key_value}
                            onChange={(e) =>
                              this.handleInputChange(e, 'api_key_value')
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
                            items={this.state.webhook.envizi_template_list}
                            selectedItem={this.state.webhook.envizi_template}
                            onChange={(e) =>
                              this.handleDropDownChange(e, 'envizi_template')
                            }
                          />
                        </td>
                      </tr>
                      <tr>
                        <td className="my-textbox-row">
                          <Dropdown
                            className="gan-dropdown-operation"
                            titleText="Webhook Data Template Type"
                            items={this.state.webhook.data_template_type_list}
                            selectedItem={this.state.webhook.data_template_type}
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
                            value={this.state.webhook.multiple_records_field}
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
                            className="btn-success button-excel"
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
                              {this.state.refresh_msg}
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
                <div className="text-sub-heading">Data Mapping</div>
                <div className="text-sub-heading-label2">
                  Map the data from webhook returned json file to the template
                  columns
                </div>
                <div className="upload-section">
                  <div className="fin-container">
                    {!this.state.loading &&
                      this.state.webhook &&
                      this.state.webhook.fields &&
                      this.state.webhook.fields.map((item, index) => (
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
                                    kind="secondary"
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
                                    kind="secondary"
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
                            className="btn-success button-excel"
                            onClick={this.handleSave}
                          >
                            Save
                          </Button>
                        </div>
                        <div className="fin-column">
                          <Button
                            className="btn-success button-excel"
                            onClick={this.handleBack}
                          >
                            Back
                          </Button>
                        </div>
                      </div>
                      <div className="fin-row">
                        <div>
                          <span className="instruction-msg">
                            {this.state.save_msg}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </section>
            </div>

            <div className="my-component">
              <section className="top-section">
                <div className="text-sub-heading">Envizi Data Preview</div>
                {
                  <div className="text-sub-heading-label2">
                    Preview of the Envizi data generated based on the Webhook mapping.
                  </div>
                }
                <div className="upload-section">
                  <table className="full-width-table">
                    <tbody>
                      <tr>
                        <td className="my-textbox-row">
                          <Button
                            className="btn-success button-excel"
                            onClick={this.handleConvert}
                          >
                            Preview 
                          </Button>
                        </td>
                      </tr>
                      <tr>
                        <td className="my-textbox-row">
                          {this.state.convert_processed_data && (
                            <CarbonTable
                              columns={this.state.template_columns}
                              jsonData={this.state.convert_processed_data}
                              headingText1={'Data Preview'}
                              headingText2={
                                'The below data would be generated and pushed to Envizi'
                              }
                            />
                          )}
                        </td>
                      </tr>

                      <tr>
                        <td className="my-textbox-row">
                          <div>
                            <span className="instruction-msg">
                              {this.state.convert_msg}
                            </span>
                          </div>
                        </td>
                      </tr>
                    </tbody>
                  </table>
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
