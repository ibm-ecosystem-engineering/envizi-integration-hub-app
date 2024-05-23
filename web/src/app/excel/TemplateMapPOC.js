'use client';

import React, { Component } from 'react';

import {
  TextInput,
  Button,
} from 'carbon-components-react';

import {  Dropdown } from 'carbon-components-react';

import '../../components/css/common.css'; // Import the CSS file for styling

import { Add, TrashCan } from '@carbon/react/icons';

/* Option 2: Use the flexgrid module */

class TemplateMapPOC extends Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: false,
      pageData: [],
      uploaded_columns: this.props.uploaded_columns,
      locations: this.props.locations,
      accounts: this.props.accounts,
    };
  }

  findSuitableUploadedColumn(columnToFind) {
    var mycolumns = this.state.uploaded_columns;
    for (const mycolumn of mycolumns) {
      if (mycolumn === columnToFind) {
        return mycolumn;
      }
    }
    for (const mycolumn of mycolumns) {
      if (mycolumn.includes(columnToFind)) {
        return mycolumn;
      }
    }
    for (const mycolumn of mycolumns) {
      if (columnToFind.includes(mycolumn)) {
        return mycolumn;
      }
    }
    return columnToFind;
    // return ""
  }

  getJsonDataType4 = () => {
    return {
      id: 1,
      text_value: '',
      uploaded_column: '',
      operation_value: '',
      operation_elements: ['Append', '+', '-', '*', '/'],
    };
  };

  // Method to return JSON data
  getJsonDataType1 = (name, label) => {
    return {
      id: 0,
      name: name,
      label: label,
      type: '2',
      text_value: '',
      uploaded_column: this.findSuitableUploadedColumn(label),
      list: [],
    };
  };

  getJsonDataType2 = (name, label) => {
    return {
      id: 0,
      name: name,
      label: label,
      type: '2',
      text_value: '',
      uploaded_column: this.findSuitableUploadedColumn(label),
      // uploaded_column: label,
      list: [this.getJsonDataType4()],
    };
  };

  getJsonDataType2_with_default = (name, label, defaultValue) => {
    return {
      id: 0,
      name: name,
      label: label,
      type: '2',
      text_value: defaultValue,
      uploaded_column: this.findSuitableUploadedColumn(label),
      list: [this.getJsonDataType4()],
    };
  };

  getJsonDataType3 = (name, label, list_elements) => {
    return {
      id: 0,
      name: name,
      label: label,
      type: '3',
      text_value: '',
      list_value: '',
      uploaded_column: this.findSuitableUploadedColumn(label),
      list_elements: list_elements,
      list: [this.getJsonDataType4()],
    };
  };

  handleLoad() {
    //Uploaded columns
    let arr1 = [''];
    let arr2 = this.state.uploaded_columns;
    let combinedArray = [...arr1, ...arr2];
    this.setUploadedColumns(combinedArray);

    var list = [];
    list.push(this.getJsonDataType1('organization', 'Organization'));
    list.push(
      this.getJsonDataType3('location', 'Location', this.state.locations)
    );
    list.push(this.getJsonDataType2('account_style', 'Account Style Caption'));
    list.push(
      this.getJsonDataType3(
        'account_name',
        'Account Number',
        this.state.accounts
      )
    );
    list.push(this.getJsonDataType2('account_ref', 'Account Reference'));
    list.push(this.getJsonDataType2('account_supplier', 'Account Supplier'));
    list.push(
      this.getJsonDataType2_with_default(
        'record_start',
        'Record Start YYYY-MM-DD',
        '2024-01-01'
      )
    );
    list.push(
      this.getJsonDataType2_with_default(
        'record_end',
        'Record End YYYY-MM-DD',
        '2024-01-01'
      )
    );
    list.push(this.getJsonDataType2('quantity', 'Quantity'));
    list.push(
      this.getJsonDataType2(
        'total_cost',
        'Total cost (incl. Tax) in local currency'
      )
    );
    list.push(this.getJsonDataType2('record_reference', 'Record Reference'));
    list.push(
      this.getJsonDataType2('record_invoice_number', 'Record Invoice Number')
    );
    list.push(
      this.getJsonDataType2('record_data_quality', 'Record Data Quality')
    );

    console.log('PocTemplateMapPage handleLoad  1---> ');
    this.setPageData(list);
    console.log('PocTemplateMapPage handleLoad  2---> ');
    console.info(JSON.stringify(list, null, 2));
  }

  componentDidMount() {
    this.handleLoad();
  }

  setLoading = (value) => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.loading = value;
      return newData;
    });
  };

  setUploadedColumns = (value) => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.uploaded_columns = value;
      return newData;
    });
  };

  setPageData = (value) => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.pageData = value;
      return newData;
    });
    this.props.onChildDataChange(this.state);
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
    // console.info('findItemIndexByName Test 1 : ' + name);

    const myData = this.state.pageData;

    for (let i = 0; i < myData.length; i++) {
      // console.info('findItemIndexByName Test 2 Index - ' + i);
      const item = myData[i];
      // console.info('findItemIndexByName Test 3 item[name] - ' + item.name + ':');
      if (item.name === name) {
        // console.info('findItemIndexByName Test 4 match found ');
        return i;
      }
    }
    // console.info('findItemIndexByName Test 5 match not found ');
    return -1;
  };

  // Function to handle adding a new field to a section
  addField = (name, index) => {
    // console.info('addField Test ----------------------- Start');
    // console.info('addField Test 1 name : ' + name);
    // console.info('addField Test 2 index : ' + index);

    const fieldIndex = this.findItemIndexByName(name);
    // console.info('addField Test 3 fieldIndex : ' + fieldIndex);
    if (fieldIndex !== -1) {
      const element = this.getJsonDataType4();
      // console.info('addField Test 4 element : ' + element);

      const item = this.state.pageData[fieldIndex];
      // console.info('addField Test 5 item[list] - ' + JSON.stringify(item.list));
      item.list.splice(index, 0, element);
      // console.info('addField Test 6 item[list] - ' + JSON.stringify(item.list));

      this.setState((prevData) => {
        const newData = { ...prevData };
        newData.pageData[fieldIndex].list = item.list;
        return newData;
      });
    }
  };

  // Function to handle adding a new field to a section
  removeField = (name, index) => {
    // console.info('removeField Test ----------------------- Start');
    // console.info('removeField Test 1 name : ' + name);
    // console.info('removeField Test 2 index : ' + index);

    const fieldIndex = this.findItemIndexByName(name);
    // console.info('removeField Test 3 fieldIndex : ' + fieldIndex);
    if (fieldIndex !== -1) {
      const item = this.state.pageData[fieldIndex];
      // console.info('removeField Test 4 item[list] - ' + JSON.stringify(item.list));

      // Remove 1 element at the specified index
      item.list.splice(index, 1);

      // console.info('removeField Test 5 item[list] - ' + JSON.stringify(item.list));

      this.setState((prevData) => {
        const newData = { ...prevData };
        newData.pageData[fieldIndex].list = item.list;
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
        newData.pageData[fieldIndex].text_value = value;
        this.props.onChildDataChange(newData);
        return newData;
      });
    }
  };

  handleListValueChange = (event, name) => {
    const fieldIndex = this.findItemIndexByName(name);
    console.info('handleListValueChange --11111>fieldIndex : ' + fieldIndex);
    if (fieldIndex !== -1) {
      this.setState((prevData) => {
        const value = event.selectedItem;
        const newData = { ...prevData };
        console.info('handleListValueChange -->value : ' + value);

        newData.pageData[fieldIndex].list_value = value;
        this.props.onChildDataChange(newData);
        return newData;
      });
    }
  };

  handleUploadedColumnValueChange = (event, name) => {
    const fieldIndex = this.findItemIndexByName(name);
    console.info(
      'handleUploadedColumnValueChange -222->fieldIndex : ' + fieldIndex
    );

    if (fieldIndex !== -1) {
      this.setState((prevData) => {
        const value = event.selectedItem;
        const newData = { ...prevData };
        newData.pageData[fieldIndex].uploaded_column = value;
        console.info('handleUploadedColumnValueChange -->value : ' + value);

        this.props.onChildDataChange(newData);
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
        newData.pageData[fieldIndex].list[index].text_value = value;
        this.props.onChildDataChange(newData);
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
        newData.pageData[fieldIndex].list[index].uploaded_column = value;
        this.props.onChildDataChange(newData);
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
        newData.pageData[fieldIndex].list[index].operation_value = value;
        this.props.onChildDataChange(newData);
        return newData;
      });
    }
  };

  onClickIngestPOC = async () => {
    await this.props.onChildDataChange(this.state);
    this.props.ingestButtonClickParentMethod();
  };

  render() {
    if (this.state.loading) {
      return <div>Loading...</div>;
    }

    return (
      <div className="my-component">
        <div className="fin-header-section">
          <div className="fin-text-heading">Data Mapping</div>
          <div className="fin-text-heading-label">
            Map the data from your uploaded excel file to the template columns
          </div>
        </div>
        {/* <div className="gan-text-sub-heading">
                            Envizi Template Columns
                        </div>
                        <div className="gan-text-sub-heading-label">
                            The the list of Envizi Template columns
                        </div> */}
        <div className="fin-container">
          {this.state.pageData.map((item, index) => (
            <div className="fin-mapping-container">
              <div className="fin-mapping-container2">
              <div className="fin-row">
                <div className="fin-column">
                  <div className="fin-field-label">{item.label}</div>
                </div>
                <div className="fin-column">
                  <TextInput
                    className="fin-text-box"
                    // labelText="Free Text"
                    value={item.text_value}
                    size="md"
                    onChange={(e) => this.handleTextValueChange(e, item.name)}
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
                      this.handleUploadedColumnValueChange(e, item.name)
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
                      onChange={(e) => this.handleListValueChange(e, item.name)}
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
                            this.handleSubTextValueChange(e, item.name, index)
                          }
                        />
                      </div>
                      <div className="fin-column">
                        <Dropdown
                          className="gan-dropdown-uploaded-columns"
                          items={this.state.uploaded_columns}
                          // titleText="Uploaded Columns"
                          selectedItem={subitem.uploaded_column}
                          // size="md"
                          // defaultSelectedItems={[subitem.uploaded_column]}
                          type="default" // Set type to "default" for single-select behavior

                          onChange={(e) =>
                            this.handleSubListValueChange(e, item.name, index)
                          }
                        />
                      </div>
                      <div className="fin-column">
                        <Dropdown
                          className="gan-dropdown-operation"
                          // titleText="Operation"
                          items={subitem.operation_elements}
                          selectedItem={subitem.operation_value}
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
                          onClick={() => this.addField(item.name, index + 1)}
                        />
                        <Button
                          kind="secondary"
                          className="fin-button-icon"
                          hasIconOnly
                          renderIcon={TrashCan}
                          iconDescription="Delete"
                          size="sm"
                          onClick={() => this.removeField(item.name, index)}
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
                  onClick={this.onClickIngestPOC}
                >
                  Ingest
                </Button>
              </div>
              <div className="fin-row">
                <div>
                  <span className="instruction-msg">
                    {this.props.resultIngestPOC &&
                      this.props.resultIngestPOC.msg}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}
export default TemplateMapPOC;
