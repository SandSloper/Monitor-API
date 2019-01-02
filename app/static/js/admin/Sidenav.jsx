class Sidenav extends React.Component{
    render(){
        return(
            <div>
                <ul className="list-group">
                    <li className="list-group-item">
                        <p className="font-weight-bold">Dashboard</p>
                    </li>
                     <li className="list-group-item">
                        <p className="font-weight-bold">WFS</p>
                    </li>
                    <li className="list-group-item">
                        <p className="font-weight-bold">WCS</p>
                    </li>
                    <li className="list-group-item">
                        <p className="font-weight-bold">WMS</p>
                    </li>
                </ul>
            </div>
        );
    }
}
 ReactDOM.render(
    < Sidenav />,
    document.getElementById('side_nav')
  );