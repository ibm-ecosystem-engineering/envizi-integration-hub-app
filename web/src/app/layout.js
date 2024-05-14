import './globals.scss';

import { Providers } from './providers';

export const metadata = {
  title: 'Envizi Integration Hub',
  description: 'Envizi Integration Hub - Solution Accelerator',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
