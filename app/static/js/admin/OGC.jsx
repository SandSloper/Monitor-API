class OGC extends React.Component{
   constructor(props) {
        super(props);
        this.state={
            result:false,
            resultJSX:false
        };
        this.handleClick = this.handleClick.bind(this);
   }
   handleClick(ev){
        let service=ev.currentTarget.getAttribute('data-service');
        if(service==="updateAll"){
            SwalManager.setLoading("info");
            RequestManager.updateOGCService(this.props.service)
                .then(result => {
                    console.log(result);
                   SwalManager.removeDialog();
                   let data = result.data;
                   let resultJSX = (
                           <div className="card-columns">
                               {data.map((value,index)=>{
                                   let elements = data[index][Object.keys(value)];
                                   let sp_extend = Object.keys(elements.spatial_extends);
                                   if(elements.state==="create") {
                                       return (
                                           <div className="card text-white bg-success">
                                               <div className="card-body">
                                                   <h5 className="card-title">{elements.name}</h5>
                                                   <div className="card-text font-weight-bold">Zeitschnitte:</div>
                                                   <ul className="list-group">
                                                   {elements.times.split(",").map((value, index) => {
                                                            return(
                                                                <li className="list-group-item text-dark">{value}</li>
                                                            )
                                                        })
                                                   }
                                                   </ul>
                                                    <div className="card-text font-weight-bold">Räumliche-Gebiete:</div>
                                                   <ul className="list-group">
                                                   {this.props.service!=="geosn" ?
                                                       sp_extend.map((value,i)=>{
                                                       if(parseInt(elements.spatial_extends[value])===1){
                                                           return(
                                                                <li className="list-group-item text-dark">{value}</li>
                                                            )
                                                       }
                                                   }):elements.spatial_extends}
                                                   </ul>
                                               </div>
                                           </div>)
                                   }else{
                                       return(
                                           <div className="card text-white bg-danger">
                                               <div className="card-body">
                                                   <h5 className="card-title">{elements.name}</h5>
                                                   <p className="card-text font-weight-bold">{elements.state}</p>
                                               </div>
                                           </div>)
                                   }
                               })
                               }
                        </div>
                    );
                    this.setState({
                       result: true,
                       resultJSX: resultJSX
                    });
                }).catch(error=>{
                    console.error(error);
               SwalManager.setError();
            });
            this.setState({result:false});
        }else if(service==="create"){

        }
   }
  render(){
    return(
        <div className="jumbotron">
            <div className="row w-100">
                <div className="col-md-3">
                    <div className="card mx-sm-1 p-3">
                        <div className="card-img-top text-center text-info"><i className="fa fa-sync fa-4x" aria-hidden="true"></i></div>
                        <div className="card-body text-center">
                            <a href="#" className="btn btn-info" data-service="updateAll" onClick={this.handleClick}>Alle Dienste aktualisieren</a>
                        </div>
                    </div>
                </div>
                <div className="col-md-3">
                   <div className="card mx-sm-1 p-3 el-disabled">
                        <div className="card-img-top text-center text-primary"><i className="fa fa-edit fa-4x" aria-hidden="true"></i></div>
                        <div className="card-body text-center">
                            <a href="#" className="btn btn-primary el-disabled" data-service="create">Einzelnen Dienste erstellen</a>
                        </div>
                    </div>
                </div>
                <div className="col-md-3">
                    <div className="card mx-sm-1 p-3 el-disabled">
                        <div className="card-img-top text-center text-danger"><i className="fa fa-trash-alt fa-4x" aria-hidden="true"></i></div>
                        <div className="card-body text-center">
                            <a href="#" className="btn btn-danger el-disabled">Dienst löschen</a>
                        </div>
                    </div>
                </div>
                <div className="col-md-3">
                    <div className="card mx-sm-1 p-3 el-disabled">
                        <div className="card-img-top text-center text-success"><i className="fa fa-table fa-4x" aria-hidden="true"></i></div>
                        <div className="card-body text-center">
                            <a href="#" className="btn btn-success el-disabled">Übersicht</a>
                        </div>
                    </div>
                </div>
            </div>
            {this.state.result? <ModalDialog title={"Erstellte Layer:"} body={this.state.resultJSX} style={"success"}/>:null}
        </div>
    );
  }
}
ReactDOM.render(
    < OGC service={"wfs"}/>,
    document.getElementById('page_content')
);