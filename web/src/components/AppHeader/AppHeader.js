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
      <Header aria-label="My App" className="HeaderClass">
        <HeaderName
          href="#"
          prefix={<img className="HeaderImage" src="../images/envizi.svg" />}
        >
          &nbsp; <span className="HeaderTitle">Integration Hub</span>
        </HeaderName>
        <HeaderNavigation>
          <Button className="HeaderMenu" href="/">
            Home
          </Button>
          <Button className="HeaderMenu" href="/turbo">
            Turbonomic
          </Button>
          {/* <Button className="HeaderMenu" href="/excel">
            Excel P
          </Button> */}
          <Button className="HeaderMenu" href="/excelpro">
            Excel 
          </Button> 
          <Button className="HeaderMenu" href="/webhooks">
            Webhook
          </Button>
          <Button className="HeaderMenu" href="/invoice">
            Invoice
          </Button>
          <Button className="HeaderMenu" href="/config">
            Config
          </Button>
        </HeaderNavigation>
        <HeaderGlobalBar>
          <HeaderGlobalAction aria-label="Notifications">
            {/* <Notification20 /> */}
          </HeaderGlobalAction>
          <HeaderGlobalAction aria-label="User Avatar">
            {/* <UserAvatar20  size={20} /> */}
          </HeaderGlobalAction>
          <HeaderGlobalAction aria-label="App Switcher">
            {/* <AppSwitcher20  size={20} /> */}
          </HeaderGlobalAction>
        </HeaderGlobalBar>
      </Header>
    );
  }
}

export default AppHeader;
