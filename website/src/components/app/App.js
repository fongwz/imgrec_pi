import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import axios from 'axios';
import Pusher from 'pusher-js';

class App extends Component {
  constructor(){
    super()
    this.state = {text: "hello"}
  }

  componentDidMount(){

    const pusher = new Pusher('ac944354925fa2b30b7e', {
      cluster: 'ap1',
      encrypted: true
    });
    const channel = pusher.subscribe('imgrec');
    channel.bind('message', data => {
      console.log(data)
    });

    const payload = {
      username: "hi",
      message: "be"
    }
    axios.post('http://localhost:5000/message', payload);
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Welcome to React</h1>
        </header>
        <p className="App-intro">
          {this.state.text}
        </p>
        <p><img src={require("../../faces/1.jpg")} alt="Stickman"/></p>
      </div>
    );
  }
}

export default App;
