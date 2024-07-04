'use client';

import { Content, Theme } from '@carbon/react';
import {
  SideNav,
  SideNavItems,
  SideNavLink,
  SideNavMenu,
  SideNavMenuItem,
} from 'carbon-components-react';
import { Menu32 } from '@carbon/icons-react';
import React, { useState } from 'react';

import { Dashboard32, List32, Settings32 } from '@carbon/icons-react';
import AppHeader from '@/components/AppHeader/AppHeader';
import LoginPage from './login/LoginPage';

export function Providers({ children }) {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLogin = (status) => {
    setIsLoggedIn(status);
  };

  return (
    <div>
      <Theme theme="white">
        <AppHeader />
        <Content>
          {/* {!isLoggedIn ? (
            <LoginPage onLogin={handleLogin} />
          ) : ( */}
          {children}
          {/* )} */}
        </Content>
      </Theme>
    </div>
  );
}
