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
import { Add, TrashCan, Replicate, Edit, Run } from '@carbon/react/icons';

import {
  Advocate,
  Globe,
  AcceleratingTransformation,
} from '@carbon/pictograms-react';
import { API_URL } from '../../components/common-constants.js';
import CarbonTable from '../../components/CarbonTable/CarbonTable';
import ApiUtility from '../../components/ApiUtility/ApiUtility'; // Import the utility class

import '../../components/css/common.css'; // Import the CSS file for styling

class ExcelListPage extends Component {
  constructor() {
    super();
    this.state = {
      loading: false,
      msg: null,
      excelList: null,
    };
    this.apiUtility = new ApiUtility();
  }

  componentDidMount() {
    this.handleLoad();
  }

  getExcelProDetailLink(id) {
    return '/excelprodetail?action=load&id=' + id;
  }

  handleNew = () => {
    window.location.href = '/excelprodetail?action=new';
  };

  handleClone = (id) => {
    window.location.href = '/excelprodetail?action=clone&id=' + id;
  };

  handleOpen = (id) => {
    window.location.href = '/excelprodetail?action=load&id=' + id;
  };

  handleLoad = () => {
    this.postRequest(
      '/api/excelpro/loadall',
      null,
      null,
      this.sucessCallBackLoad,
      null
    );
  };

  handleDelete = (id) => {
    this.postRequest(
      '/api/excelpro/delete',
      this.startLoading,
      this.stopLoading,
      this.sucessCallBackDelete,
      id
    );
  };

  sucessCallBackLoad = (resp) => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.excelList = resp.data;
      newData.msg = resp.msg;
      newData.loading = false;
      return newData;
    });
  };

  sucessCallBackDelete = (resp) => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.excelList = resp.data;
      newData.msg = resp.msg;
      newData.loading = false;
      return newData;
    });
  };

  startLoading = () => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.msg = null;
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

  postRequest = (url, startCallBack, errorCallBack, sucesssCallBack, id) => {
    var myPayload = { id: id };
    this.apiUtility.postRequest(
      url,
      startCallBack,
      errorCallBack,
      sucesssCallBack,
      myPayload
    );
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
          <span className="SubHeaderTitle">Excel Integration</span>
        </Column>
        <Column lg={16} md={8} sm={4} className="landing-page__r2">
          <div className="my-component">
            <section className="top-section">
              <div className="text-sub-heading">Excel Mapping list </div>
              <div className="text-sub-heading-label2">
                Manage your excel mapping list here
              </div>

              <div className="upload-section">
                <div className="fin-row">
                  <div className="fin-column">
                    <Button className="fin-button-1" onClick={this.handleNew}>
                      New
                    </Button>
                  </div>
                </div>
              </div>
              <div>
                {this.state.loading && (
                  <div>
                    <p>&nbsp;</p>
                    <Loading description="Loading content..." />
                  </div>
                )}
              </div>
              <div className="upload-section">
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableHeader>Id</TableHeader>
                      <TableHeader>Name</TableHeader>
                      <TableHeader>Desc</TableHeader>
                      <TableHeader>Envizi Template Type</TableHeader>
                      <TableHeader>Actions</TableHeader>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {this.state.excelList &&
                      this.state.excelList.map((item) => (
                        <TableRow key={item.id}>
                          <TableCell key={item.id}>
                            <Link
                              href={this.getExcelProDetailLink(item.id)}
                              target="_self"
                            >
                              {item.id}
                            </Link>
                          </TableCell>
                          <TableCell>{item.name}</TableCell>
                          <TableCell>{item.desc}</TableCell>
                          <TableCell>{item.type}</TableCell>
                          <TableCell>
                            <Button
                              className="fin-button-icon2"
                              hasIconOnly
                              renderIcon={Edit}
                              iconDescription="Open"
                              size="sm"
                              onClick={() => this.handleOpen(item.id)}
                            />
                            <Button
                              kind="secondary"
                              className="fin-button-icon2"
                              hasIconOnly
                              renderIcon={Replicate}
                              iconDescription="Clone/Copy"
                              size="sm"
                              onClick={() => this.handleClone(item.id)}
                            />
                            <Button
                              kind="secondary"
                              className="fin-button-icon2"
                              hasIconOnly
                              renderIcon={TrashCan}
                              iconDescription="Delete"
                              size="sm"
                              onClick={() => this.handleDelete(item.id)}
                            />
                          </TableCell>
                        </TableRow>
                      ))}
                  </TableBody>
                </Table>
              </div>
            </section>
          </div>
        </Column>
      </Grid>
    );
  }
}
export default ExcelListPage;
