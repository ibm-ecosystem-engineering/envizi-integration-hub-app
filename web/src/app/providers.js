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

import { Dashboard32, List32, Settings32 } from '@carbon/icons-react';
import AppHeader from '@/components/AppHeader/AppHeader';

export function Providers({ children }) {
  return (
    <div>
      <Theme theme="white">
        <AppHeader />
        <Content>{children} </Content>
      </Theme>
    </div>
  );
}
