class Menu extends React.Component{
  render(){
    let url = window.location.href,
        path = url.includes("services");
    return(
        <nav className="navbar navbar-expand-lg navbar-light bg-light" id="navbarNav">
            <div className="navbar">
                <ul className="navbar-nav">
                    <li className={"nav-item "+(path ? '':'active')}>
                        <a className="nav-link" href="https://monitor.ioer.de/monitor_api/api_key">API-Key</a>
                    </li>
                    <li className={"nav-item "+(path ? 'active':'')}>
                        <a className="nav-link" href="https://monitor.ioer.de/monitor_api/services">OGC-Dienste</a>
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
    < Menu />,
    document.getElementById('navbar')
  );