class Sidenav extends React.Component{
       constructor(props) {
           super(props);
           this.state={
               active:"wfs"
           };
           this.handleClick = this.handleClick.bind(this);
       }
       handleClick(ev) {
           const service = ev.currentTarget.getAttribute('data-service');
            this.setState({
              active: service
            });
            const ogc =  < OGC service={service}/>;
            ReactDOM.render(
            ogc,
            document.getElementById('page_content'));
          }
        render(){
            return(
                <div>
                    <ul className="list-group">
                        {/*<li className="list-group-item">
                            <p className="font-weight-bold">Dashboard</p>
                        </li>*/}
                         <li className={('list-group-item cursor ')+(this.state.active==="wfs" ? 'active':null)} data-service="wfs" onClick={this.handleClick}>
                            <p className="font-weight-bold" data-service="wfs">WFS</p>
                        </li>
                        <li className={('list-group-item cursor ')+(this.state.active==="wcs" ? 'active':null)} data-service="wcs" onClick={this.handleClick}>
                            <p className="font-weight-bold" data-service="wcs">WCS</p>
                        </li>
                        <li className={('list-group-item cursor ')+(this.state.active==="wms" ? 'active':null)} data-service="wms" onClick={this.handleClick}>
                            <p className="font-weight-bold">WMS</p>
                        </li>
                        <li className={('list-group-item cursor ')+(this.state.active==="geosn" ? 'active':null)} data-service="geosn" onClick={this.handleClick}>
                            <p className="font-weight-bold">GeoMIS</p>
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