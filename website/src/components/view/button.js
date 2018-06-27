import React from 'react'

export class ViewButton extends React.Component{
	constructor(){
		super()
		this.handleClick = this.handleClick.bind(this)
	}

	handleClick(){
		this.props.callBack('view', true)
	}

	render(){
		return(
			<section>
                <div className="content" onClick={this.handleClick}>
                    <a className="icon fa-vcard-o"><span className="label">Icon</span></a>
                    <h3>View All Faces</h3>
                </div>
             </section>
			);
	}
}