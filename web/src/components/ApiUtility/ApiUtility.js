'use client';
import React, { Component } from 'react';

import axios from 'axios';
import { API_URL } from '../common-constants.js';

class ApiUtility {

  postRequest = (url, startCallBack, errorCallBack, sucesssCallBack, myPayload) => {

    if (startCallBack)
      startCallBack();
    const headers = { 'Access-Control-Allow-Origin': '*', };
    axios
      .post(API_URL + url, myPayload, { headers })
      .then((response) => {
        console.log('Output of the execute API Call ---> ' + JSON.stringify(response.data));
        sucesssCallBack (response.data)
      })
      .catch((error) => {
        if (errorCallBack)
          errorCallBack(error);
      });
  };
  
}
export default ApiUtility;
