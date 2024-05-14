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

import {
  Advocate,
  Globe,
  AcceleratingTransformation,
} from '@carbon/pictograms-react';

class MyUtility {
  createEmptyWebhook() {
    var myWebhook = {
      id: '',
      name: '',
      desc: '',
      http_method_list: this.getHttpMethod_List(),
      http_method : '',
      url: '',
      user: '',
      password: '',
      token: '',
      api_key_name: '',
      api_key_value: '',
      envizi_template_list: this.getEnvizi_Template_List(),
      envizi_template: '',
      data_template_type_list: this.getWebhook_Data_Template_Type_List(),
      data_template_type: '',
      multiple_records_field: '',
      fields: this.createEmptyFields(),
    };
    return myWebhook;
  }

  createEmptyFields() {
    console.info('createEmptyFields start ----->:');

    var list = [];
    list.push(this.getJsonDataType1('organization', 'Organization'));
    list.push(this.getJsonDataType1('location', 'Location'));
    list.push(this.getJsonDataType1('account_style', 'Account Style Caption'));
    list.push(this.getJsonDataType1('account_name', 'Account Number'));
    list.push(this.getJsonDataType1('account_ref', 'Account Reference'));
    list.push(this.getJsonDataType1('account_supplier', 'Account Supplier'));
    list.push(this.getJsonDataType1('record_start', 'Record Start YYYY-MM-DD'));
    list.push(this.getJsonDataType1('record_end', 'Record End YYYY-MM-DD'));
    list.push(this.getJsonDataType1('quantity', 'Quantity'));
    list.push(
      this.getJsonDataType1(
        'total_cost',
        'Total cost (incl. Tax) in local currency'
      )
    );
    list.push(this.getJsonDataType1('record_reference', 'Record Reference'));
    list.push(
      this.getJsonDataType1('record_invoice_number', 'Record Invoice Number')
    );
    list.push(
      this.getJsonDataType1('record_data_quality', 'Record Data Quality')
    );
    console.info('createEmptyFields end ----->:');
    return list;
  }

  getJsonDataType1 = (name, label) => {
    return {
      id: 0,
      name: name,
      label: label,
      type: '1',
      text_value: '',
      map_value: '',
      list: [this.getJsonDataType2()],
    };
  };

  getJsonDataType2 = () => {
    return {
      id: 1,
      text_value: '',
      map_value: '',
      operation_elements: ['Append', '+', '-', '*', '/'],
    };
  };

  getHttpMethod_List = () => {
    return ['GET', 'POST'];
  };

  getEnvizi_Template_List = () => {
    return ['POC', 'ASDL-PMC'];
  };


  getWebhook_Data_Template_Type_List = () => {
    return ['1-single', '2-multiple', '3-multiple-and-common'];
  };
}
export default MyUtility;
