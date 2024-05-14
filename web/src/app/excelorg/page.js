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
import DraggableList from '@/components/DraggableList/DraggableList';
import DataTable from '@/components/DataTable/DataTable';

import Image from 'next/image.js';
import '../../components/css/common.css'; // Import the CSS file for styling
import './excel.css'; // Import the CSS file for styling

import invoiceImage from './images/invoice.png'; // Import the image file
import integrationImage from './images/integration.png'; // Import the image file

class ExcelPage extends Component {
  constructor() {
    super();
    this.state = {
      loading: false,
      selectedFileCONFIG: null,
      selectedFilePOC: null,
      selectedFileASDL: null,
      resultContentCONFIG: null,
      resultContentPOC: [],
      resultContentASDL: [],
      resultContentPOCIngest: '',
      resultContentASDLIngest: '',
      resultContentInvoice: '',
    };
  }

  handleFileChangeCONFIG = (event) => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.selectedFileCONFIG = event.target.files[0];
      newData.resultContentCONFIG = null;
      return newData;
    });
  };

  handleFileChangePOC = (event) => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.selectedFilePOC = event.target.files[0];
      newData.resultContentPOC = null;
      return newData;
    });
  };

  handleFileChangeASDL = (event) => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.selectedFileASDL = event.target.files[0];
      newData.resultContentASDL = null;
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

  handleIngestCONFIG = async () => {
    this.setLoading(true);

    try {
      var urlFinal = API_URL + '/api/excel/uploadConfigConnector';
      const formData = new FormData();
      formData.append('file', this.state.selectedFileCONFIG);

      const response = await axios.post(urlFinal, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log('File uploaded successfully:', response.data);

      this.setState((prevData) => {
        const newData = { ...prevData };
        newData.resultContentCONFIG = response.data;
        newData.loading = false;
        return newData;
      });
    } catch (error) {
      console.error('Error uploading file', error);
      this.setLoading(false);
    }
  };

  handleUploadPOC = async () => {
    this.setLoading(true);
    try {
      var urlFinal = API_URL + '/api/excel/loadTemplatePOC';

      const formData = new FormData();
      formData.append('file', this.state.selectedFilePOC);

      const response = await axios.post(urlFinal, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log('File uploaded successfully:', response.data);

      this.setState((prevData) => {
        const newData = { ...prevData };
        newData.resultContentPOC = response.data;
        newData.loading = false;
        return newData;
      });
    } catch (error) {
      console.error('Error uploading file', error);
      this.setLoading(false);
    }
  };

  handleInvoice = async () => {
    this.setLoading(true);
    try {
      var urlFinal = API_URL + '/api/invoice/export';

      const formData = new FormData();
      const response = await axios.post(urlFinal, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log('File uploaded successfully:', response.data);

      this.setState((prevData) => {
        const newData = { ...prevData };
        newData.resultContentInvoice = response.data;
        newData.loading = false;
        return newData;
      });
    } catch (error) {
      console.error('Error uploading file', error);
      this.setLoading(false);
    }
  };

  handleUploadASDL = async () => {
    this.setLoading(true);
    try {
      var urlFinal = API_URL + '/api/excel/loadTemplateASDL';

      const formData = new FormData();
      formData.append('file', this.state.selectedFileASDL);

      const response = await axios.post(urlFinal, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log('File uploaded successfully:', response.data);

      this.setState((prevData) => {
        const newData = { ...prevData };
        newData.resultContentASDL = response.data;
        newData.loading = false;
        return newData;
      });
    } catch (error) {
      console.error('Error uploading file', error);
      this.setLoading(false);
    }
  };

  handleIngestPOC = async () => {
    this.setLoading(true);

    const headers = {
      Authorization: 'Bearer xxxxx',
      'Access-Control-Allow-Origin': '*',
    };

    const myData = {
      template_columns: this.state.resultContentPOC.template_array,
      uploaded_columns: this.state.resultContentPOC.uploaded_array,
      uploadedFile: this.state.resultContentPOC.uploadedFile,
    };

    axios
      .post(API_URL + '/api/excel/ingestTemplatePOC', myData, { headers })
      .then((response) => {
        console.log('Output of the API Call ---> ' + response.data);
        const returnData = response.data;
        this.setState((prevData) => {
          const newData = { ...prevData };
          newData.resultContentPOC = response.data;
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

  handleIngestASDL = async () => {
    this.setLoading(true);

    const headers = {
      Authorization: 'Bearer xxxxx',
      'Access-Control-Allow-Origin': '*',
    };

    const myData = {
      template_columns: this.state.resultContentASDL.template_array,
      uploaded_columns: this.state.resultContentASDL.uploaded_array,
      uploadedFile: this.state.resultContentASDL.uploadedFile,
    };

    axios
      .post(API_URL + '/api/excel/ingestTemplateASDL', myData, { headers })
      .then((response) => {
        console.log('Output of the API Call ---> ' + response.data);
        const returnData = response.data;
        this.setState((prevData) => {
          const newData = { ...prevData };
          newData.resultContentASDL = response.data;
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
    if (this.state.loading) {
      return <div>Loading...</div>;
    }

    return (
      <Grid className="landing-page" fullWidth>
        <Column
          lg={16}
          md={8}
          sm={4}
          className="landing-page__banner my-title-image"
        >
          <span className="SubHeaderTitle">Excel Data Processing</span>
        </Column>
        <Column lg={16} md={8} sm={4} className="landing-page__r2">
          <Tabs defaultSelectedIndex={0}>
            <TabList className="tabs-group" aria-label="Page navigation">
              <Tab>Config Connector & UDC</Tab>
              <Tab>POC Account Setup and Data Load</Tab>
              <Tab>Account Setup and Data Load PM&C</Tab>
            </TabList>
            <TabPanels>
              <TabPanel>
                <Grid className="tabs-group-content">
                  <Column
                    md={4}
                    lg={7}
                    sm={4}
                    className="landing-page__tab-content"
                  >
                    <table>
                      <tr>
                        <td>
                          <h2 className="landing-page__subheading">
                            Config Connector & UDC Template
                          </h2>
                        </td>
                      </tr>
                      <tr>
                        <td>
                          <p className="landing-page__p">
                            If you have the Config Connector & UDC Template
                            files in the expected format, you can directly
                            upload those file in this section and upon Ingest
                            button click it will be pushed to S3 bucket
                            configured in the Data Services to integrate the
                            data into the Envizi.
                          </p>
                        </td>
                      </tr>
                      <tr>
                        <td className="instruction-label">
                          <input
                            type="file"
                            className="file-class"
                            onClick={this.handleFileChangeCONFIG}
                            onChange={this.handleFileChangeCONFIG}
                          />
                        </td>
                      </tr>
                      <tr>
                        <td className="instruction-label">
                          <Button
                            size="sm"
                            className="input-control-lable"
                            onClick={() => {
                              this.handleIngestCONFIG();
                            }}
                            disabled={this.state.loading}
                          >
                            Upload & Ingest
                          </Button>
                        </td>
                      </tr>
                      <tr>
                        <td>&nbsp;</td>
                      </tr>
                      <tr>
                        <td>
                          <span className="instruction-msg">
                            {!this.state.loading &&
                            this.state.resultContentCONFIG ? (
                              <span>{this.state.resultContentCONFIG.msg}</span>
                            ) : (
                              <span></span>
                            )}
                          </span>
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
                    </table>
                  </Column>
                  <Column md={4} lg={{ span: 8, offset: 7 }} sm={4}>
                    <Image
                      className="landing-page__illo"
                      src={integrationImage}
                      alt="Invoice"
                      width={786}
                      height={647}
                    />
                  </Column>
                </Grid>
              </TabPanel>

              <TabPanel>
                <Grid className="tabs-group-content">
                  <Column
                    md={4}
                    lg={7}
                    sm={4}
                    className="landing-page__tab-content"
                  >
                    <table>
                      <tr>
                        <td>
                          <h2 className="landing-page__subheading">
                            POC Account Setup and Data Load
                          </h2>
                        </td>
                      </tr>
                      <tr>
                        <td>
                          <p className="landing-page__p11">
                            If you have something similar to POC Account Setup
                            and Data Load format you can upload the file in this
                            section. It shows the template file columns on the
                            left and the uploaded files column on the right. You
                            can drag and drop the columns appropriately and
                            click ingest to push the files to S3 bucket for
                            further processing.
                          </p>
                        </td>
                      </tr>
                      <tr>
                        <td className="instruction-label">
                          <input
                            type="file"
                            className="file-class"
                            onClick={this.handleFileChangePOC}
                            onChange={this.handleFileChangePOC}
                          />
                        </td>
                      </tr>
                      <tr>
                        <td className="instruction-label">
                          <Button
                            size="sm"
                            className="input-control-lable"
                            onClick={() => {
                              this.handleUploadPOC();
                            }}
                            disabled={this.state.loading}
                          >
                            Upload & Ingest
                          </Button>
                        </td>
                      </tr>
                      <tr>
                        <td>&nbsp;</td>
                      </tr>
                      <tr>
                        <td>
                          <span className="instruction-msg">
                            {!this.state.loading &&
                            this.state.resultContentPOC ? (
                              <span>{this.state.resultContentPOC.msg}</span>
                            ) : (
                              <span></span>
                            )}
                          </span>
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
                        <td>&nbsp;</td>
                      </tr>
                      <tr>
                        <td>
                          {this.state.resultContentPOC &&
                          this.state.resultContentPOC.template_array ? (
                            <table>
                              <tr>
                                <td>
                                  Map the columns between the uploaded Excel
                                  file and the template
                                </td>
                              </tr>
                              <tr>
                                <td>
                                  <DataTable
                                    jsonData={
                                      this.state.resultContentPOC.template_array
                                    }
                                    headingText={'Template'}
                                  />
                                  <DataTable
                                    jsonData={
                                      this.state.resultContentPOC.uploaded_array
                                    }
                                    headingText={'Uploaded'}
                                  />
                                </td>
                              </tr>
                              <tr>
                                <td>
                                  <Button
                                    className="btn-success button-excel"
                                    onClick={this.handleIngestPOC}
                                  >
                                    Ingest
                                  </Button>
                                </td>
                              </tr>
                            </table>
                          ) : (
                            <span></span>
                          )}
                        </td>
                      </tr>
                      <tr>
                        <td className="instruction-msg">
                          {this.state.resultContentPOCIngest}
                        </td>
                      </tr>
                    </table>
                  </Column>
                  <Column md={4} lg={{ span: 8, offset: 7 }} sm={4}>
                    <Image
                      className="landing-page__illo"
                      src={integrationImage}
                      alt="Invoice"
                      width={786}
                      height={647}
                    />
                  </Column>
                </Grid>
              </TabPanel>

              <TabPanel>
                <Grid className="tabs-group-content">
                  <Column
                    md={4}
                    lg={7}
                    sm={4}
                    className="landing-page__tab-content"
                  >
                    <table>
                      <tr>
                        <td>
                          <h2 className="landing-page__subheading">
                            Account Setup and Data Load PM&C
                          </h2>
                        </td>
                      </tr>
                      <tr>
                        <td>
                          <p className="landing-page__p">
                            If you have something similar to Account Setup and
                            Data Load PM&C format you can upload the file in
                            this section. It shows the template file columns on
                            the left and the uploaded files column on the right.
                            You can drag and drop the columns appropriately and
                            click ingest to push the files to S3 bucket for
                            further processing.
                          </p>
                        </td>
                      </tr>
                      <tr>
                        <td className="instruction-label">
                          <input
                            type="file"
                            className="file-class"
                            onClick={this.handleFileChangeASDL}
                            onChange={this.handleFileChangeASDL}
                          />
                        </td>
                      </tr>
                      <tr>
                        <td className="instruction-label">
                          <Button
                            size="sm"
                            className="input-control-lable"
                            onClick={() => {
                              this.handleUploadASDL();
                            }}
                            disabled={this.state.loading}
                          >
                            Upload & Ingest
                          </Button>
                        </td>
                      </tr>
                      <tr>
                        <td>&nbsp;</td>
                      </tr>
                      <tr>
                        <td>
                          <span className="instruction-msg">
                            {!this.state.loading &&
                            this.state.resultContentASDL ? (
                              <span>{this.state.resultContentASDL.msg}</span>
                            ) : (
                              <span></span>
                            )}
                          </span>
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
                        <td>&nbsp;</td>
                      </tr>
                      <tr>
                        <td>
                          {this.state.resultContentASDL &&
                          this.state.resultContentASDL.template_array ? (
                            <table>
                              <tr>
                                <td>
                                  Map the columns between the uploaded Excel
                                  file and the template
                                </td>
                              </tr>
                              <tr>
                                <td>
                                  <DataTable
                                    jsonData={
                                      this.state.resultContentASDL
                                        .template_array
                                    }
                                    headingText={'Template'}
                                  />
                                  <DataTable
                                    jsonData={
                                      this.state.resultContentASDL
                                        .uploaded_array
                                    }
                                    headingText={'Uploaded'}
                                  />
                                </td>
                              </tr>
                              <tr>
                                <td>
                                  <Button
                                    className="btn-success button-excel"
                                    onClick={this.handleIngestASDL}
                                  >
                                    Ingest
                                  </Button>
                                </td>
                              </tr>
                            </table>
                          ) : (
                            <span></span>
                          )}
                        </td>
                      </tr>
                      <tr>
                        <td className="instruction-msg">
                          {this.state.resultContentASDLIngest}
                        </td>
                      </tr>
                    </table>
                  </Column>
                  <Column md={4} lg={{ span: 8, offset: 7 }} sm={4}>
                    <Image
                      className="landing-page__illo"
                      src={integrationImage}
                      alt="Invoice"
                      width={786}
                      height={647}
                    />
                  </Column>
                </Grid>
              </TabPanel>
            </TabPanels>
          </Tabs>
        </Column>
      </Grid>
    );
  }
}
export default ExcelPage;
