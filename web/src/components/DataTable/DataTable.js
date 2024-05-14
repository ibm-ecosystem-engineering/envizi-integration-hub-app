import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css'; // Import Bootstrap CSS
import Table from 'react-bootstrap/Table';
import './DataTable.css'; // Import the CSS file for styling
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

const DataTable = ({ jsonData, headingText }) => {
  if (!jsonData || jsonData.length === 0) {
    return <p></p>;
  }

  const keys = jsonData.length > 0 ? Object.keys(jsonData[0]) : [];
  return (
    <Row>
      <Col className="section">
        <Container>
          <Row>
            <Col>
              <div className="section-sub">
                <Container>
                  <div className="myHeading">{headingText} </div>
                  <Table striped bordered hover className="myTable">
                    <thead>
                      <tr>
                        {keys.map((key) => (
                          <th key={key} className="myHeaderRow">
                            {key}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {jsonData.map((item, index) => (
                        <tr key={index}>
                          {keys.map((key) => (
                            <td key={key}>{item[key]}</td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </Table>
                </Container>
              </div>
            </Col>
          </Row>
        </Container>
      </Col>
    </Row>
  );
};

export default DataTable;
