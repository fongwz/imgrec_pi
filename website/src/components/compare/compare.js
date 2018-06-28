import React from 'react'
import {CompareButton} from './button.js'
import {CompareDisplay} from './display.js'

export class Compare extends React.Component{
	constructor(){
		super()
		this.buttonCallBack = this.buttonCallBack.bind(this)
	}

	buttonCallBack(name, state){
		this.props.callBack(name, state)
	}

	render(){
		let view;
		if(this.props.open){
			view = (<CompareDisplay />);
		} else {
			view = (<CompareButton callBack={this.buttonCallBack}/>);
		}

		return(
			<section>
				{view}
			</section>
			);
	}
}