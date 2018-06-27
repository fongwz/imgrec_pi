import React from 'react'
import {ViewButton} from './button.js'
import {ViewDisplay} from './display.js'

export class View extends React.Component{
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
			view = (<ViewDisplay />)
		} else {
			view = (<ViewButton callBack={this.buttonCallBack}/>)
		}

		return(
			<section>
				{view}
			</section>
			);
	}
}