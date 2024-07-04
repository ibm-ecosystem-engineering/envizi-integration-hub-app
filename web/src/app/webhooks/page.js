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
import { Add, TrashCan, Replicate, Edit, Run } from '@carbon/react/icons';

import CarbonTable from '../../components/CarbonTable/CarbonTable';
import ApiUtility from '../../components/ApiUtility/ApiUtility'; // Import the utility class

import '../../components/css/common.css'; // Import the CSS file for styling

class WebhookPage extends Component {
  constructor() {
    super();
    this.state = {
      loading: false,
      msg: null,
      webhooks: null,
      execution_result: null,
    };
    this.apiUtility = new ApiUtility();
  }

  componentDidMount() {
    this.handleLoad();
  }

  getWebhookDetailLink(id) {
    return '/webhookdetail?action=load&id=' + id;
  }

  handleNew = () => {
    window.location.href = '/webhookdetail?action=new';
  };

  handleOpen = (id) => {
    window.location.href = '/webhookdetail?action=load&id=' + id;
  };

  handleClone = (id) => {
    window.location.href = '/webhookdetail?action=clone&id=' + id;
  };

  handleLoad = () => {
    this.postRequest(
      '/api/webhook/loadall',
      null,
      null,
      this.sucessCallBackLoad,
      null
    );
  };

  handleExecute = (id) => {
    this.postRequest(
      '/api/webhook/execute',
      this.startLoading,
      this.stopLoading,
      this.sucessCallBackExecute,
      id
    );
  };

  handleDelete = (id) => {
    this.postRequest(
      '/api/webhook/delete',
      this.startLoading,
      this.stopLoading,
      this.sucessCallBackDelete,
      id
    );
  };

  sucessCallBackLoad = (resp) => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.webhooks = resp.data;
      newData.msg = resp.msg;
      newData.loading = false;
      return newData;
    });
  };

  sucessCallBackExecute = (resp) => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.execution_result = resp.data;
      newData.template_columns = resp.template_columns;
      newData.msg = resp.msg;
      newData.loading = false;
      return newData;
    });
  };

  sucessCallBackDelete = (resp) => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.webhooks = resp.data;
      newData.msg = resp.msg;
      newData.loading = false;
      return newData;
    });
  };

  startLoading = () => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.msg = null;
      newData.execution_result = null;
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
          <span className="SubHeaderTitle">Webhook Integration</span>
        </Column>
        <Column lg={16} md={8} sm={4} className="landing-page__r2">
          <div className="my-component">
            <section className="top-section">
              <div className="text-sub-heading">Webhooks</div>
              <div className="text-sub-heading-label2">
                Manage your webhooks here
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
                    {this.state.webhooks &&
                      this.state.webhooks.map((item) => (
                        <TableRow key={item.id}>
                          <TableCell key={item.id}>
                            <Link
                              href={this.getWebhookDetailLink(item.id)}
                              target="_self"
                            >
                              {item.id}
                            </Link>
                          </TableCell>
                          <TableCell>{item.name}</TableCell>
                          <TableCell>{item.desc}</TableCell>
                          <TableCell>{item.type}</TableCell>
                          <TableCell>
                            {/* <Button
                                    kind="secondary"
                                    type="button"
                                    className="fin-button-icon"
                                    hasIconOnly
                                    renderIcon={Run}
                                    iconDescription="Run/Execute"
                                    size="sm"
                                    onClick={() =>
                                      this.handleExecute(item.id)
                                    }
                                  />                                   */}
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

        <Column lg={16} md={8} sm={4} className="landing-page__r2">
          <div className="my-component">
            {this.state.execution_result && (
              <section className="top-section">
                <div className="text-sub-heading">Webhook Execution Result</div>
                <div className="text-sub-heading-label2">
                  Webhook Execution results
                </div>

                {/* <div className="upload-section">
                  <div className="fin-row">
                    <div className="fin-column">
                      {JSON.stringify(this.state.execution_result)}
                    </div>
                  </div>
                </div> */}
                <div className="upload-section">
                  {this.state.execution_result && (
                    <CarbonTable
                      columns={this.state.template_columns}
                      jsonData={this.state.execution_result}
                      headingText1={'Data Ingested'}
                      headingText2={'The below data have been pushed to Envizi'}
                    />
                  )}
                </div>
              </section>
            )}
          </div>
        </Column>
      </Grid>
    );
  }
}
export default WebhookPage;
