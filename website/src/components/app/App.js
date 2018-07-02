import React, { Component } from 'react';
import {View} from './../view/view.js'
import {Compare} from './../compare/compare.js'
import './../../css/assets/css/main.css'

class App extends Component {
  constructor(){
    super()
    this.state = {
      view: false,  
      compare: false
    }
    this.componentCallBack = this.componentCallBack.bind(this)
  }

  componentCallBack(name, state) {
    this.setState({[name]: state});
  }

  shouldComponentUpdate(){
    if(!this.state.view || !this.state.compare){
      return true
    } else {
      return false
    }
  }

  render() {
    let view;
    if(!this.state.view && !this.state.compare){
      view = (
        <div className="highlights">
          <View open={false} callBack={this.componentCallBack}/>
          <Compare open={false} callBack={this.componentCallBack}/>
        </div>
        );
    } else if(this.state.view){ view=(<View open={true} callBack={this.componentCallBack} />); 
    } else if(this.state.compare){ view=(<Compare open={true} callBack={this.componentCallBack} />); }

    console.log(this.state.view, this.state.compare)

    return (
        <section className="wrapper">
          <header id="header">
            <a className="logo" href="index.html">Home</a>
          </header>
          <div className="inner">
            {view}
          </div>
        </section>
    );
  }
}

export default App;
