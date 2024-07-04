import React, { Component } from 'react';

class EnvUtility {
  // This is a server side method. Should not use "use client"
  getAPIUrl = () => {
    return process.env.NEXT_PUBLIC_API_URL;
  };
}

export default EnvUtility;
