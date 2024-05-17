import React from 'react';
import './CarbonTableSimple.css'; // Import the CSS file for styling
import {
  Table,
  TableHead,
  TableRow,
  TableHeader,
  TableBody,
  TableContainer,
  TableCell,
} from '@carbon/react';
const CarbonTableSimple = ({ column, arrayData, headingText1, headingText2 }) => {
  if (!arrayData || arrayData.length === 0) {
    return <p></p>;
  }

  return (
    <div className="my-component">
      <div className="fin-header-section">
        <div className="fin-text-heading">{headingText1}</div>
        <div className="fin-text-heading-label">{headingText2}</div>
      </div>
      <div className="fin-container">
      <TableContainer>

        <Table aria-label="Simple table">
          <TableHead>
            <TableRow>
                <TableHeader>{column}</TableHeader>
            </TableRow>
          </TableHead>
          <TableBody>
            {arrayData.map((item, index) => (
              <TableRow key={index}>
                  <TableCell key={index} >{item}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        </TableContainer>

      </div>
    </div>
  );
};

export default CarbonTableSimple;
