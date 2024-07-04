'use client';
import React, { Component } from 'react';

import axios from 'axios';
import EnvUtility from '../../components/EnvUtility/EnvUtility';

class ApiUtility {
  postRequest = (
    url,
    startCallBack,
    errorCallBack,
    sucesssCallBack,
    myPayload
  ) => {
    const headers = { 'Access-Control-Allow-Origin': '*' };

    const envUtility = new EnvUtility();
    var my_URL = envUtility.getAPIUrl() + url;

    if (startCallBack) startCallBack();
    axios
      .post(my_URL, myPayload, { headers })
      .then((response) => {
        sucesssCallBack(response.data);
      })
      .catch((error) => {
        if (errorCallBack) errorCallBack(error);
      });
  };
}

export default ApiUtility;
