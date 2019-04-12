class ModalDialog extends React.Component{
    //probs title,body
    constructor(props){
        super(props);
    }
    static remove(){
        $('.modal').modal('hide');
    }
    componentDidMount(){
        $('.modal').modal('show');
     }
     render(){
        return(
            <div className="modal" tabindex="-1" role="dialog">
                <div className="modal-dialog" role="document" style={{width:"auto",maxWidth:"90%"}}>
                    <div className="modal-content">
                        <div className="modal-header">
                            <h5 className={("modal-title ")+("text-"+this.props.style)}>{this.props.title}</h5>
                        </div>
                        <div className="modal-body">
                            {this.props.body}
                        </div>
                        <div className="modal-footer">
                        <button type="button" className="btn btn-secondary" data-dismiss="modal">Close</button>
                    </div>
                    </div>
                </div>
            </div>
        )
    }
}