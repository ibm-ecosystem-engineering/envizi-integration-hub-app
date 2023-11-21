import React, { Component } from 'react';
import { useEffect } from 'react';

import axios from 'axios';
import Spinner from 'react-bootstrap/Spinner';

import Form from "react-bootstrap/Form";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Button from "react-bootstrap/Button";
import Image from "react-bootstrap/Image";
import Collapse from "react-bootstrap/Collapse";
import Container from "react-bootstrap/Container";


import Main from "../main/main";

import configJsonData from "../../data/envizi-config.json";
import { useState } from 'react'
import Card from 'react-bootstrap/Card';


class SevOneMain extends React.Component {

  handleDownload = () => {
    fetch('/http://localhost:3001/download-file', { method: 'GET' })
      .then((response) => {
        if (response.ok) {
          return response.blob();
        } else {
          throw new Error('Failed to download file');
        }
      })
      // .then((blob) => {
      //   const url = window.URL.createObjectURL(blob);
      //   const a = document.createElement('a');
      //   a.href = url;
      //   a.download = 'example.pdf'; // Specify the desired filename
      //   a.click();
      //   window.URL.revokeObjectURL(url);
      // })
      .catch((error) => {
        console.error('Error downloading file:', error);
      });
  };


  render() {
    return (
      <div>
        <h1>Download Content</h1>
        <button onClick={this.handleDownload}>Download1</button>
      </div>
    );
  }
}

export default SevOneMain;
