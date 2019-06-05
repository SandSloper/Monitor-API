class ApiKey extends React.Component{
    constructor(props) {
        super(props);
        this.state = {value: key,button_text:button_text};
        this.textArea = React.createRef();
        this.copyToClipboard = this.copyToClipboard.bind(this);
    }
    copyToClipboard(){
        const el = document.createElement('textarea'),
            manager = this;
        console.log(this.state.value, this.state.value.length);
        if(this.state.value && this.state.value.length >1){
            el.value = this.state.value;
            document.body.appendChild(el);
            el.select();
            document.execCommand('copy');
            document.body.removeChild(el);
        }else{
             var key =ApiKey.makekey();
            //check if the key allredy exists
            console.log(url_base+'/check_key');
           $.ajax({
               url:url_base+'/check_key',
               type:"GET",
               data:{"key":key},
               success:function(data){
                   console.log(data);
                   if(!data){
                        manager.insert(key,username,user_id);
                   }
               }
            });
        }
    }
    static makekey() {
        var text = "";
        var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

        for (var i = 0; i < 32; i++)
        text += possible.charAt(Math.floor(Math.random() * possible.length));

        return text;
    }
    insert(key,username,user_id){
        const manager = this;
        console.log(url_base+'/check_key');
         $.ajax({
                url:url_base+'/insert_key',
                type:"GET",
                data:{
                    key:key,
                    name:username,
                    id:user_id
                },
                 success:function(data){
                          if(data){
                              manager.setState({value: key});
                              manager.setState({button_text: "Kopieren"});
                          }
                 }
           });
        }
    render(){
        return(
            <div className="container api_key_generate">
                <h5>API-Key</h5>
                <hr className="hr"/>
                    <textarea ref={(textarea) => this.textArea = textarea} className="form-control" id="api_key" value={this.state.value} rows={1} disabled/>
                    <button type="button" className="btn btn-warning" id="api_key_btn" data-user_name={username}  data-user_id={user_id} onClick={this.copyToClipboard}>{this.state.button_text}</button>
            </div>
        );
    }
}
 ReactDOM.render(
    <ApiKey />,
    document.getElementById('root')
  );
