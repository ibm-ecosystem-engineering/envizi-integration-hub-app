import React, { Component, Container } from 'react';
// import { DndProvider, useDrag, useDrop } from 'react-dnd';
// import { HTML5Backend } from 'react-dnd-html5-backend';
import './DraggableList.css';

const ItemTypes = {
  CARD: 'card',
};

class DraggableList extends Component {
  constructor(props) {
    super(props);
    this.state = {
      items: this.props.data,
      itemsCompare: this.props.dataCompare,
    };
  }
  setLoading = (value) => {
    this.setState((prevData) => {
      const newData = { ...prevData };
      newData.loading = value;
      return newData;
    });
  };

  moveItem = (dragIndex, hoverIndex) => {
    const items = this.state.items;
    const itemsCompare = this.state.itemsCompare;
    const draggedItem = items[dragIndex];

    items.splice(dragIndex, 1);
    items.splice(hoverIndex, 0, draggedItem);

    {
      items.map((item, index) =>
        item.text === itemsCompare[index].text
          ? (item.difference = false)
          : (item.difference = true)
      );
    }

    this.setState({ items: items });
  };

  render() {
    const { items } = this.state;

    const Card = ({ id, text, index, difference }) => {
      const [, ref] = useDrag({
        type: ItemTypes.CARD,
        item: { id, index },
      });

      const [, drop] = useDrop({
        accept: ItemTypes.CARD,
        hover: (draggedItem) => {
          if (draggedItem.index !== index) {
            this.moveItem(draggedItem.index, index);
            draggedItem.index = index;
          }
        },
      });

      return (
        <span>
          {difference ? (
            <div
              ref={(node) => ref(drop(node))}
              style={{
                padding: '4px',
                width: '300px',
                border: '1px solid #D21404',
                marginBottom: '4px',
              }}
            >
              {text} &nbsp;
            </div>
          ) : (
            <div
              ref={(node) => ref(drop(node))}
              style={{
                padding: '4px',
                width: '300px',
                border: '1px solid #ccc',
                marginBottom: '4px',
              }}
            >
              {text} &nbsp;
            </div>
          )}
        </span>
      );
    };

    return (
      <div>
        {items.map((item, index) => (
          <Card
            key={item.id}
            id={item.id}
            text={item.text}
            index={index}
            difference={item.difference}
          />
        ))}
      </div>
    );
  }
}

class DraggableListDisplay extends Component {
  constructor(props) {
    super(props);
    // Access props passed to the component
    console.log('Parameter passed 1:', this.props.data1);
    console.log('Parameter passed 2:', this.props.data2);
  }

  render() {
    const data1 = [
      { id: 1, text: 'Item 1' },
      { id: 2, text: 'Item 2' },
      { id: 3, text: 'Item 3' },
    ];

    return (
      // <DndProvider backend={HTML5Backend}>
      <div className="outer-container">
        <div className="left-side">
          <div className="left-side-label"> Template file Columns </div>
          <DraggableList data={this.props.data1} />
        </div>
        {/* <div className="middle-side">a
          </div> */}
        <div className="right-side">
          <div className="left-side-label"> Uploaded file Columns </div>
          <DraggableList
            data={this.props.data2}
            dataCompare={this.props.data1}
          />
        </div>
      </div>
      // </DndProvider>
    );
  }
}

export default DraggableListDisplay;
