import React from 'react'
import './display.css'

export class ViewDisplay extends React.Component{
	constructor(){
		super()
		this.state = {
			loading: false
		}
		this.facelist=[];
		this.faceimage=[];
		this.facedetails=[];
		this.table_header = (<thead>
													<tr>
														<th>Name</th>
														<th>Facetoken</th>
													</tr>
												</thead>
												);

		this.handleClick = this.handleClick.bind(this)
	}

	componentWillMount(){
		this.setState({loading: true})
		fetch('/viewall', 
		{
  		method: 'POST',
  		headers: {
    	'Accept': 'application/json',
    	'Content-Type': 'application/json',
  		},
  		body: JSON.stringify({})
		}).then((response) => {
			return response.json();
		}).then((data) => {
			var jsonString = JSON.stringify(data);
			var jsonObject = JSON.parse(jsonString);
			for(var i=0;i<jsonObject.length; i++){
				this.facelist.push(
					<tr className='face-row' key={i} onClick={this.handleClick} face-token={jsonObject[i].facetoken} face-name={jsonObject[i].name}>
						<td>{jsonObject[i].name}</td>
						<td>{jsonObject[i].facetoken}</td>
					</tr>
					);
			}
			this.setState({loading: false})
			return;
		})
	}

	handleClick(e){
		this.setState({loadingImage: true})
		var token = e.currentTarget.getAttribute('face-token')
		var name = e.currentTarget.getAttribute('face-name')
		this.faceimage.splice(0,this.faceimage.length)
		this.facedetails.splice(0,this.facedetails.length)

		this.faceimage.push(
			<img src={require('../../faces/' + token + '.png')} key={token + '1'} />
			);
		this.facedetails.push(
			<section>
				<p>Name: {name}</p>
				<p>Token: {token}</p>
			</section>
			);
		this.setState({loadingImage: false})
	}

	render(){
		var Rows = (<tbody>{this.state.loading?<tr><td>loading data...</td></tr>:this.facelist}</tbody>);
		var Image = (<section>{this.faceimage}</section>)
		var ImageDetails = (<section>{this.facedetails}</section>)
		return(
			<div className="row">
				<div className="col-6 col-12-medium">
					<div className="table-wrapper">
						<table className="alt">
							{this.table_header}
							{Rows}
						</table>
					</div>
				</div>

				<div className="col-6 col-12-medium">
					{Image}
					{ImageDetails}
				</div>
			</div>
			);
	}
}