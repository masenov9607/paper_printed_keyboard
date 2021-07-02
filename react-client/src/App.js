import './App.css';
import React, { Component } from 'react'
import eventService from './service/event-service';

export default class App extends Component {
  state = {
    current_num: -1,
    classes:["non_active","non_active","non_active","non_active","non_active","non_active",
    "non_active","non_active","non_active","non_active",],
    errors: []
  }

  constructor(props) {
    super(props);
    this.moveForward = this.moveForward.bind(this);
  }
  zero_style = {
    justifyContent: "center"
  };
  render() {
    return (
      <div className="App">
            <header className="App-header">
            <h3>Events:</h3>
            <button className={this.state.classes[1]}>1</button>
            <button className={this.state.classes[2]}>2</button>
            <button className={this.state.classes[3]}>3</button>
            <br/>
            <button className={this.state.classes[4]}>4</button>
            <button className={this.state.classes[5]}>5</button>
            <button className={this.state.classes[6]}>6</button>
            <br/>
            <button className={this.state.classes[7]}>7</button>
            <button className={this.state.classes[8]}>8</button>
            <button className={this.state.classes[9]}>9</button>
            <br/>
            <button style={this.zero_style} className={this.state.classes[0]}>0</button>
            </header>
      </div>
    );
  }

  componentDidMount() {
    eventService.wsSubject.subscribe(
      message => {
        this.showMessage(message);
      },
      error => {
        this.showError(error);
      },
      () => {
        this.showMessage("Event stream completed.");
      });
  }

  showMessage(message) {
    let num = message["key"];
    let new_classes = this.state.classes;
    new_classes[this.state.current_num] = "non_active";
    new_classes[num] = "active";
    this.setState(state => ({classes: new_classes}));
    this.setState(state => ({current_num: num }));
    //this.setState(state => ({messages: state.messages.concat(message)}));
  }
  showError(error) {
    //this.setState(state => ({errors: state.errors.concat(error)}));
  }

  moveForward(){
    //eventService.sendEvent("moveForward");
  }
  moveStop = () => {
    //eventService.sendEvent("moveStop");
  }
}
