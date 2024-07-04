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
import { Add, TrashCan } from '@carbon/react/icons';

import CarbonTableSimple from '../../components/CarbonTableSimple/CarbonTableSimple';
import CarbonTable from '../../components/CarbonTable/CarbonTable';

import ApiUtility from '../../components/ApiUtility/ApiUtility'; // Import the utility class
import EnvUtility from '../../components/EnvUtility/EnvUtility';

import '../../components/css/common.css'; // Import the CSS file for styling

class ExcelDetailPage extends Component {
  constructor() {
    super();
    this.apiUtility = new ApiUtility();
    this.state = {
      loading: true,

      main_data: null,
      uploaded_columns: [''],

      selectedFilePOC: null,
      resultUpload: null,
      resultIngest: null,
      msg_process: null,
      msg_save: null,
    };
    this.envUtility = new EnvUtility();
  }

  componentDidMount() {
    this.handlePageOnLoad();
  }

  handlePageOnLoad() {
    // Read the Query param
    const queryParams = new URLSearchParams(window.location.search);
    const action = queryParams.get('action');
    const id = queryParams.get('id');

    if (action === 'new') {
      this.handleNew();
    } else if (action === 'load') {
      this.handleLoad(id);
    } else if (action === 'clone') {
      this.handleClone(id);
    }
  }

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
      // newData.selectedFilePOC = null;
      newData.resultUpload = null;
      newData.resultIngest = null;
      this.handleTemplateChange();
      return newData;
    });
  };

  handleFileChangePOC = (event) => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.selectedFilePOC = event.target.files[0];
      newData.resultUpload = null;
      newData.resultIngest = null;
      newData.msg_process = null;
      newData.msg_save = null;
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

  handleBack = (event) => {
    window.location.href = '/excelpro';
  };

  handleNew() {
    const myPayload = {};
    this.postRequest(
      '/api/excelpro/loadnew',
      null,
      null,
      this.sucessCallBackLoadNew,
      myPayload
    );
  }

  handleLoad(id) {
    const myPayload = { id: id };
    this.postRequest(
      '/api/excelpro/load',
      null,
      null,
      this.sucessCallBackLoad,
      myPayload
    );
  }

  handleTemplateChange() {
    const myPayload = this.state.main_data;
    this.postRequest(
      '/api/excelpro/templatechange',
      this.startLoading,
      this.stopLoading,
      this.sucessCallBackTemplateChange,
      myPayload
    );
  }

  handleClone(id) {
    const myPayload = { id: id };
    this.postRequest(
      '/api/excelpro/load',
      null,
      null,
      this.sucessCallBackClone,
      myPayload
    );
  }

  handleSavePOC = (event) => {
    this.postRequest(
      '/api/excelpro/save',
      this.startLoading,
      this.stopLoading,
      this.sucessCallBackSave,
      this.state.main_data
    );
  };

  handleViewInScreen = () => {
    const myPayload = {
      template_columns: this.state.resultUpload.template_columns,
      uploadedFile: this.state.resultUpload.uploadedFile,
      main_data: this.state.main_data,
    };
    this.postRequest(
      '/api/excelpro/viewInScreen',
      this.startLoading,
      this.stopLoading,
      this.sucessCallBackViewInScreen,
      myPayload
    );
  };

  handleIngestToEnvizi = () => {
    const myPayload = {
      template_columns: this.state.resultUpload.template_columns,
      uploadedFile: this.state.resultUpload.uploadedFile,
      main_data: this.state.main_data,
    };
    this.postRequest(
      '/api/excelpro/ingestToEnvizi',
      this.startLoading,
      this.stopLoading,
      this.sucessCallBackIngestToEnvizi,
      myPayload
    );
  };

  handleUploadData = async () => {
    this.startLoading();

    const headers = {
      'Access-Control-Allow-Origin': '*',
      'Content-Type': 'multipart/form-data',
    };
    try {
      var my_URL = this.envUtility.getAPIUrl() + '/api/excelpro/uploadData';

      const formData = new FormData();
      formData.append('file', this.state.selectedFilePOC);
      formData.append('envizi_template', this.state.main_data.envizi_template);

      const response = await axios.post(my_URL, formData, { headers });

      this.sucessCallBackUpload(response);
    } catch (error) {
      console.error('Error uploading file', error);
      this.stopLoading();
    }
  };

  sucessCallBackUpload = async (resp) => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.resultUpload = resp.data;
      newData.uploaded_columns = resp.data.uploaded_columns;
      newData.msg_process = resp.data.msg;
      newData.loading = false;
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

  sucessCallBackViewInScreen = (resp) => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.resultIngest = resp;
      newData.msg_process = resp.msg;
      newData.loading = false;
      return newData;
    });
  };

  sucessCallBackLoadNew = (resp) => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.main_data = resp.data;
      newData.loading = false;
      return newData;
    });
  };

  sucessCallBackLoad = (resp) => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.main_data = resp.data;
      newData.loading = false;
      return newData;
    });
  };

  sucessCallBackClone = (resp) => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.main_data = resp.data;
      newData.main_data.id = '';
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

  sucessCallBackSave = (resp) => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.main_data = resp.data;
      newData.msg_save = resp.msg;
      newData.loading = false;
      return newData;
    });
  };

  startLoading = () => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.msg = null;
      newData.msg_process = null;
      newData.msg_save = null;
      newData.loading = true;
      return newData;
    });
  };

  stopLoading = (error) => {
    console.log(error);
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.loading = false;
      return newData;
    });
  };

  postRequest = (
    url,
    startCallBack,
    errorCallBack,
    sucesssCallBack,
    myPayload
  ) => {
    this.apiUtility.postRequest(
      url,
      startCallBack,
      errorCallBack,
      sucesssCallBack,
      myPayload
    );
  };

  getJsonDataType4 = () => {
    return {
      id: 1,
      text_value: '',
      uploaded_column: '',
      operation_value: '',
      operation_elements: ['Append', '+', '-', '*', '/'],
    };
  };

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
      const element = this.getJsonDataType4();

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

  handleTextValueChange = (event, name) => {
    const fieldIndex = this.findItemIndexByName(name);
    if (fieldIndex !== -1) {
      this.setState((prevData) => {
        const { value } = event.target;
        const newData = { ...prevData };
        newData.main_data.fields[fieldIndex].text_value = value;
        return newData;
      });
    }
  };

  handleListValueChange = (event, name) => {
    const fieldIndex = this.findItemIndexByName(name);
    if (fieldIndex !== -1) {
      this.setState((prevData) => {
        const value = event.selectedItem;
        const newData = { ...prevData };
        newData.main_data.fields[fieldIndex].list_value = value;
        return newData;
      });
    }
  };

  handleUploadedColumnValueChange = (event, name) => {
    const fieldIndex = this.findItemIndexByName(name);
    if (fieldIndex !== -1) {
      this.setState((prevData) => {
        const value = event.selectedItem;
        const newData = { ...prevData };
        newData.main_data.fields[fieldIndex].uploaded_column = value;
        return newData;
      });
    }
  };
  handleSubTextValueChange = (event, name, index) => {
    const fieldIndex = this.findItemIndexByName(name);
    if (fieldIndex !== -1) {
      this.setState((prevData) => {
        const { value } = event.target;
        const newData = { ...prevData };
        newData.main_data.fields[fieldIndex].list[index].text_value = value;
        return newData;
      });
    }
  };

  handleSubListValueChange = (event, name, index) => {
    const fieldIndex = this.findItemIndexByName(name);
    if (fieldIndex !== -1) {
      this.setState((prevData) => {
        const value = event.selectedItem;
        const newData = { ...prevData };
        newData.main_data.fields[fieldIndex].list[index].uploaded_column =
          value;
        return newData;
      });
    }
  };

  handleOperationListValueChange = (event, name, index) => {
    const fieldIndex = this.findItemIndexByName(name);
    if (fieldIndex !== -1) {
      this.setState((prevData) => {
        const value = event.selectedItem;
        const newData = { ...prevData };
        newData.main_data.fields[fieldIndex].list[index].operation_value =
          value;
        return newData;
      });
    }
  };

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
          <Grid className="my-tabs-group-content">
            <Column md={4} lg={16} sm={4} className="landing-page__tab-content">
              <table className="fin-table">
                <tbody>
                  <tr>
                    <td>
                      {this.state.main_data && (
                        <div className="my-component">
                          <div className="fin-header-section">
                            <div className="fin-text-heading">Meta info</div>
                            <div className="fin-text-heading-label">
                              Enter the excel template information{' '}
                            </div>
                          </div>
                          <div className="fin-container">
                            <table>
                              <tbody>
                                <tr>
                                  <td className="instruction-label">
                                    <TextInput
                                      class="my-textbox"
                                      labelText="Id"
                                      value={this.state.main_data.id}
                                      disabled={true}
                                      onChange={(e) =>
                                        this.handleInputChange(e, 'id')
                                      }
                                    />
                                  </td>
                                </tr>
                                <tr>
                                  <td className="instruction-label">
                                    <TextInput
                                      class="my-textbox"
                                      labelText="Name"
                                      value={this.state.main_data.name}
                                      onChange={(e) =>
                                        this.handleInputChange(e, 'name')
                                      }
                                    />
                                  </td>
                                </tr>
                                <tr>
                                  <td className="instruction-label">
                                    <TextInput
                                      class="my-textbox"
                                      labelText="Desc"
                                      value={this.state.main_data.desc}
                                      onChange={(e) =>
                                        this.handleInputChange(e, 'desc')
                                      }
                                    />
                                  </td>
                                </tr>
                                <tr>
                                  <td className="instruction-label">
                                    <Dropdown
                                      className="gan-dropdown-operation"
                                      titleText="Envizi Template"
                                      items={
                                        this.state.main_data
                                          .envizi_template_list
                                      }
                                      selectedItem={
                                        this.state.main_data.envizi_template
                                      }
                                      onChange={(e) =>
                                        this.handleDropDownChange(
                                          e,
                                          'envizi_template'
                                        )
                                      }
                                    />
                                  </td>
                                </tr>
                              </tbody>
                            </table>
                          </div>
                        </div>
                      )}
                    </td>
                  </tr>
                  <tr>
                    <td>
                      <div className="my-component">
                        <div className="fin-header-section">
                          <div className="fin-text-heading">
                            Data Ingestion to Envizi
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
                                    // size="sm"
                                    className="fin-button-1"
                                    onClick={() => {
                                      this.handleUploadData();
                                    }}
                                    disabled={!this.state.selectedFilePOC}
                                  >
                                    Load source data
                                  </Button>
                                </td>
                                <td className="instruction-label">
                                  <Button
                                    // size="sm"
                                    className="fin-button-1"
                                    onClick={() => {
                                      this.handleViewInScreen();
                                    }}
                                    disabled={!this.state.resultUpload}
                                  >
                                    Preview
                                  </Button>
                                </td>
                                <td className="instruction-label">
                                  <Button
                                    // size="sm"
                                    className="fin-button-1"
                                    onClick={() => {
                                      this.handleIngestToEnvizi();
                                    }}
                                    disabled={!this.state.resultUpload}
                                  >
                                    Ingest to Envizi
                                  </Button>
                                </td>
                                <td className="instruction-label">
                                  <Button
                                    className="fin-button-1"
                                    onClick={() => {
                                      this.handleBack();
                                    }}
                                  >
                                    Back
                                  </Button>
                                </td>
                              </tr>
                              <tr>
                                <td>
                                  <span className="instruction-msg">
                                    {!this.state.loading &&
                                    this.state.msg_process ? (
                                      <span>{this.state.msg_process}</span>
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
                      {this.state.resultIngest &&
                        this.state.resultIngest.processed_data && (
                          <span>
                            <CarbonTable
                              columns={this.state.resultIngest.template_columns}
                              jsonData={this.state.resultIngest.processed_data}
                              headingText1={'Data Generated'}
                              headingText2={
                                'The below data have been pushed to Envizi'
                              }
                            />
                            {this.state.resultIngest.validation_errors &&
                              Object.keys(
                                this.state.resultIngest.validation_errors
                              ).length > 0 && (
                                <CarbonTableSimple
                                  columns={['Error', 'Rows']}
                                  jsonData={
                                    this.state.resultIngest.validation_errors
                                  }
                                  headingText1={'Validation Errors'}
                                  headingText2={
                                    'The below validation errors occured in the data'
                                  }
                                />
                              )}
                          </span>
                        )}
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
                    {!this.state.loading && this.state.main_data && (
                      <td>
                        <div className="my-component">
                          <div className="fin-header-section">
                            <div className="fin-text-heading">Data Mapping</div>
                            <div className="fin-text-heading-label">
                              Map the data from your uploaded excel file to the
                              template columns
                            </div>
                          </div>
                          {/* <div className="gan-text-sub-heading">
                                                      Envizi Template Columns
                                                  </div>
                                                  <div className="gan-text-sub-heading-label">
                                                      The the list of Envizi Template columns
                                                  </div> */}
                          <div className="fin-container">
                            {this.state.main_data.fields.map((item, index) => (
                              <div className="fin-mapping-container">
                                <div className="fin-mapping-container2">
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
                                            item.name
                                          )
                                        }
                                      />
                                    </div>
                                    <div className="fin-column">
                                      <Dropdown
                                        className="gan-dropdown-uploaded-columns"
                                        items={this.state.uploaded_columns}
                                        // titleText="Uploaded Columns"
                                        selectedItem={item.uploaded_column}
                                        size="md"
                                        type="default" // Set type to "default" for single-select behavior
                                        // defaultSelectedItems={[item.uploaded_column]}
                                        onChange={(e) =>
                                          this.handleUploadedColumnValueChange(
                                            e,
                                            item.name
                                          )
                                        }
                                      />
                                    </div>
                                    <div className="fin-column">
                                      {item.type == 3 && (
                                        <Dropdown
                                          className="gan-dropdown-existing-values"
                                          // titleText="Existing Values"
                                          items={item.list_elements}
                                          size="md"
                                          type="default" // Set type to "default" for single-select behavior
                                          selectedItem={item.list_value}
                                          onChange={(e) =>
                                            this.handleListValueChange(
                                              e,
                                              item.name
                                            )
                                          }
                                        />
                                      )}
                                    </div>
                                  </div>
                                </div>
                                <div className="fin-mapping-container2">
                                  {(item.type == 2 || item.type == 3) &&
                                    item.list.map((subitem, index) => (
                                      <div className="fin-row">
                                        <div className="fin-column">
                                          <div className="fin-field-label"></div>
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
                                                index
                                              )
                                            }
                                          />
                                        </div>
                                        <div className="fin-column">
                                          <Dropdown
                                            className="gan-dropdown-uploaded-columns"
                                            items={this.state.uploaded_columns}
                                            // titleText="Uploaded Columns"
                                            selectedItem={
                                              subitem.uploaded_column
                                            }
                                            // size="md"
                                            // defaultSelectedItems={[subitem.uploaded_column]}
                                            type="default" // Set type to "default" for single-select behavior
                                            onChange={(e) =>
                                              this.handleSubListValueChange(
                                                e,
                                                item.name,
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
                                            selectedItem={
                                              subitem.operation_value
                                            }
                                            type="default" // Set type to "default" for single-select behavior
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
                                              this.addField(
                                                item.name,
                                                index + 1
                                              )
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
                                    className="fin-button-1"
                                    onClick={this.handleSavePOC}
                                  >
                                    Save
                                  </Button>
                                </div>
                                <div className="fin-column">
                                  <Button
                                    className="fin-button-1"
                                    onClick={this.handleBack}
                                  >
                                    Back
                                  </Button>
                                </div>
                                <div className="fin-row">
                                  <div>
                                    <span className="instruction-msg">
                                      {this.state.msg_save &&
                                        this.state.msg_save}
                                    </span>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </td>
                    )}
                  </tr>
                </tbody>
              </table>
            </Column>
          </Grid>
        </Column>
      </Grid>
    );
  }
}
export default ExcelDetailPage;
