class Navbar extends React.Component{
  render(){
    return(
        <nav className="navbar navbar-expand-lg navbar-light bg-light">
            <div className="navbar">
                <ul className="navbar-nav">
                    <li className="nav-item">
                        <button className="btn btn-secondary">OGC-Dienste</button>
                    </li>
                    <li className="nav-item ">
                        <button className="btn btn-secondary">IÖR-Monitor</button>
                    </li>
                </ul>
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