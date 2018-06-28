import React from 'react'

export class CompareButton extends React.Component{
	constructor(){
		super()
		this.handleClick = this.handleClick.bind(this)
	}

	handleClick(){
		this.props.callBack('compare', true)
	}

	render(){
		return(
			<section>
                <div className="content" onClick={this.handleClick}>     
                    <a className="icon fa-files-o"><span className="label">Icon</span></a>
                    <h3>Check Comparison</h3> 
                </div>
            </section>
			);
	}
}

