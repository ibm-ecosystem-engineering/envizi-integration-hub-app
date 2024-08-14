'use client';
import React, { Component } from 'react';

import {
  HeaderContainer,
  HeaderMenuButton,
  SkipToContent,
  SideNav,
  SideNavItems,
  Button,
  HeaderSideNavItems,
} from '@carbon/react';
import { Switcher, Notification, UserAvatar } from '@carbon/icons-react';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import Image from 'react-bootstrap/Image';
import {
  Notification20,
  UserAvatar20,
  AppSwitcher20,
} from '@carbon/icons-react';

import {
  Header,
  HeaderName,
  HeaderNavigation,
  HeaderMenuItem,
  HeaderGlobalBar,
  HeaderGlobalAction,
} from 'carbon-components-react';

import '../css/common.css'; // Import the CSS file for styling

class AppHeader extends Component {
  render() {
    return (
      <div aria-label="My App" className="HeaderClass">
      <div className="containerHeading">
      <div className="boxHeading">
        <span className="HeaderTitle">Integration Hub &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
      </div>
      <div className="boxHeading">
        <Button className="HeaderMenu" href="/">
            Home
          </Button>
      </div>
      <div className="boxHeading">
      <Button className="HeaderMenu" href="/turbo">
            Turbonomic
          </Button>
      </div>
      <div className="boxHeading">
      <Button className="HeaderMenu" href="/excelpro">
            Excel 
          </Button> 
      </div>
      <div className="boxHeading">
      <Button className="HeaderMenu" href="/webhooks">
            Webhook
          </Button>
      </div>
      <div className="boxHeading">
      <Button className="HeaderMenu" href="/invoice">
            Invoice
          </Button>
      </div>
      <div className="boxHeading">
      <Button className="HeaderMenu" href="/config">
            Config
          </Button>
      </div>
    </div>

        <div>
        
        </div>
   
      </div>
    );
  }
}

export default AppHeader;
