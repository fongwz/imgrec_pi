import React from 'react'
import Pusher from 'pusher-js';

export class CompareDisplay extends React.Component{

	constructor(){
		super()
		this.state = {confidence: null}
		this.piImage = []
		this.dbImage = []
	}

	componentDidMount() {
    const pusher = new Pusher('ac944354925fa2b30b7e', {
      cluster: 'ap1',
      encrypted: true
    });
    const channel = pusher.subscribe('imgrec');
    channel.bind('comparison', data => {
      console.log(data)
      this.piImage.splice(0, this.piImage.length)
      this.dbImage.splice(0, this.dbImage.length)

      this.piImage.push(<img src={'/comparisons/' + data.comparison_token + '.png'} key={data.comparison_token + '1'} alt="blank" />);
      this.dbImage.push(<img src={'/faces/' + data.face_token + '.png'} key={data.face_token + '1'} alt="blank" />);
      this.setState({	     
        confidence: data.confidence,
        user_id: data.user_id
      })
    });
  }

	render(){
		var imgTaken = (<section>{this.piImage}</section>);
		var imgResult = (<section>{this.dbImage}</section>);
		return(
			<div className="row">
				<div className="col-6 col-12-medium">
					<h1>Image taken</h1>
					{imgTaken}
				</div>

				<div className="col-6 col-12-medium">
					<h1>Best match</h1>
					{imgResult}
				</div>

				{
					this.state.confidence && 
					<div className="highlights">
						<h3>Confidence level: {this.state.confidence}</h3>
						<h3>Matched with: {this.state.user_id}</h3>
					</div>
				}
			</div>
			);
	}
}