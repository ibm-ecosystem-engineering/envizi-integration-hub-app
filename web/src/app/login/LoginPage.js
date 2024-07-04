// src/LoginForm.js
import React, { Component } from 'react';

import {
  Button,
  TextInput,
  Loading,
  Grid,
  Column,
} from 'carbon-components-react';
import axios from 'axios';
import EnvUtility from '../../components/EnvUtility/EnvUtility';

class LoginPage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: false,
      main_data: {
        username: '',
        password: '',
        login_status: 'FALSE',
        msg: '',
      },
    };
    this.envUtility = new EnvUtility();
  }

  handleInputChange = (event, fieldName) => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.main_data[fieldName] = event.target.value;
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
      'Access-Control-Allow-Origin': '*',
    };

    var my_URL = this.envUtility.getAPIUrl() + myAPI;
    axios
      .post(my_URL, this.state.main_data, { headers })
      .then((response) => {
        this.setState((prevData) => {
          const newData = { ...prevData };
          newData.main_data = response.data;

          if (newData.main_data['login_status'] == 'TRUE') {
            this.props.onLogin(true);
          }

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

  handleLogin = (event) => {
    return this.handleCommon(event, '/api/login/validate');
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
          <span className="SubHeaderTitle">Login</span>
        </Column>
        <Column lg={16} md={8} sm={4} className="landing-page__r2">
          <div className="my-component">
            <section className="top-section">
              <div className="text-sub-heading">Login</div>
              <div className="text-sub-heading-label2">
                Enter your credentials to login into the application.
              </div>
              <div className="upload-section">
                <table>
                  <tbody>
                    <tr>
                      <td className="my-textbox-row">
                        <TextInput
                          className="my-textbox"
                          id="username"
                          labelText="Username"
                          value={this.state.main_data.username}
                          onChange={(e) =>
                            this.handleInputChange(e, 'username')
                          }
                          required
                        />
                      </td>
                    </tr>
                    <tr>
                      <td className="my-textbox-row">
                        <TextInput
                          className="my-textbox"
                          id="password"
                          labelText="Password"
                          type="password"
                          value={this.state.main_data.password}
                          onChange={(e) =>
                            this.handleInputChange(e, 'password')
                          }
                          required
                        />
                      </td>
                    </tr>
                    <tr>
                      <td className="my-textbox-row"></td>
                    </tr>
                    <tr>
                      <td>
                        <span className="instruction-msg">
                          {!this.state.loading && this.state.main_data.msg ? (
                            <span>
                              <p>{this.state.main_data.msg}</p>
                              <p></p>
                            </span>
                          ) : (
                            <span></span>
                          )}
                        </span>
                      </td>
                    </tr>
                    <tr>
                      <td className="my-textbox-row">
                        <Button
                          className="fin-button-1"
                          onClick={(e) => this.handleLogin(e)}
                          disabled={this.state.loading}
                        >
                          Login
                        </Button>{' '}
                        &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;
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
          </div>
        </Column>
      </Grid>
    );
  }
}
export default LoginPage;
