import React from 'react';
import './CarbonTable.css'; // Import the CSS file for styling
import {
  Table,
  TableHead,
  TableRow,
  TableHeader,
  TableBody,
  TableContainer,
  TableCell,
} from '@carbon/react';
const CarbonTable = ({ columns, jsonData, headingText1, headingText2 }) => {
  if (!jsonData || jsonData.length === 0) {
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

        <Table aria-label="sample table">
          <TableHead>
            <TableRow>
              {columns.map((column) => (
                <TableHeader>{column}</TableHeader>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {jsonData.map((item, index) => (
              <TableRow key={index}>
                {columns.map((column) => (
                  <TableCell key={index} >{item[column]}</TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
        </TableContainer>

      </div>
    </div>
  );
};

export default CarbonTable;
