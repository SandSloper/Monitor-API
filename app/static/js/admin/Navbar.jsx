class Navbar extends React.Component{
    constructor(props) {
        super(props);
        this.state = {value:"ogc"};
        this.handleClick = this.handleClick.bind(this);
  }
  handleClick(ev) {
    this.setState({
      value: ev.currentTarget.getAttribute('data-key')
    });
  }
  render(){
    return(
        <nav className="navbar navbar-expand-lg navbar-light bg-light">
            <div className="navbar">
                <div className="btn-group btn-group-toggle" data-toggle="buttons">
                    <label className={('btn btn-secondary ')+(this.state.value==="ogc" ? 'active' : '')} data-key="ogc" onClick={this.handleClick}>
                        <input type="radio" name="options"/>OGC-Dienste
                    </label>
                    <label className={('btn btn-secondary ')+(this.state.value==="monitor" ? 'active' : '')} data-key="monitor" onClick={this.handleClick}>
                        <input type="radio"/> IÖR-Monitor
                    </label>
                </div>
                <div className="logout my-2 my-lg-0">
                    <a href="https://monitor.ioer.de/monitor_api/logout">
                        <button type="submit" className="btn btn-warning">Logout</button>
                    </a>
                </div>
            </div>
        </nav>
    );
  }
}
 ReactDOM.render(
    < Navbar />,
    document.getElementById('navbar')
  );