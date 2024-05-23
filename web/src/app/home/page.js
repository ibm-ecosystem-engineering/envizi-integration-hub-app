'use client';

import {
  Breadcrumb,
  BreadcrumbItem,
  Button,
  Tabs,
  Tab,
  TabList,
  TabPanels,
  TabPanel,
  Grid,
  Column,
  TableRow,
  Table,
  TableBody,
  TableHead,
  TableHeader,
  TableCell

} from '@carbon/react';


import {
  Advocate,
  Globe,
  AcceleratingTransformation,
} from '@carbon/pictograms-react';
import Image from 'next/image';
import archImage from '../../components/images/arch.png'; // Import the CSS file for styling
import '../../components/css/common.css'; // Import the CSS file for styling

export default function LandingPage() {
  return (
    <Grid className="landing-page" fullWidth>

      <Column lg={16} md={8} sm={4} className="landing-page__r2">
        <div className="my-component">
          <Grid>
            <Column lg={16}>
              <div className="mySectionTitle">
                Welcome to Envizi Integration Hub !
              </div>
            </Column>
            <Column lg={16}>
              <div className="mySectionTitle2">
              </div>
            </Column>
            <Column lg={10}>
              <div>
                <Image src={archImage} height="400" alt="Logo" />
              </div>
            </Column>
            <Column lg={6}>
              <div className="mySectionText">
                Envizi Integration Hub facilitates the integration of data from
                various external systems into the IBM Envizi ESG Suite.
              </div>

              <div className="mySectionText">
                It connects to external systems, such as Turbonomic, retrieves
                emissions data, converts this data into the Universal Account
                Setup and Data Loading format (UDC), and then dispatches it to
                an S3 bucket configured within the IBM Envizi ESG Suite.
              </div>

              <div className="mySectionText">
                At present the following integrations are available.
                <ol>
                    <li>1. Excel Integrations</li>
                    <li>2. WebHook Integrations</li>
                    <li>3. Invoice Processing</li>
                    <li>4. Utility Bill Processing</li>
                    <li>5. Turbonomic Integration</li>
                </ol>
              </div>

              <div className="mySectionText">
                Configuration settings are accessible through the Config menu.
              </div>

              <div className="mySectionText">
                This Integration Hub can be expanded to include integration with
                numerous other external systems that need to interface with the
                IBM Envizi ESG Suite.
              </div>

            </Column>
          </Grid>
        </div>
      </Column>
    </Grid>
  );
}
