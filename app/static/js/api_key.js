const txt_copy = "Kopieren";
var key_input = $('#api_key'),
    key_btn = $('#api_key_btn'),
    url_base = window.location.origin+'/monitor_api';
$(function(){
    key_btn.click(function () {
          var id = $(this).text(),
           username=$(this).data('user_name'),
           user_id=$(this).data('user_id');

       if(id===txt_copy){
            var $temp = $("<input>");
            $("body").append($temp);
            $temp.val(key_input.val()).select();
            document.execCommand("copy");
            $temp.remove();
       }else{
            var key = makekey();
            //key_input.val(key);
            //check if the key allredy exists
           $.ajax({
               url:url_base+'/check_key',
               type:"GET",
               data:{"key":key},
               success:function(data){
                   console.log(data);
                   if(!data){
                        insert(key,username,user_id);
                   }
               }
           })
       }
    });
});
function insert(key,username,user_id){
 $.ajax({
        url:url_base+'/insert_key',
        type:"GET",
        data:{
            key:key,
            name:username,
            id:user_id
        },
         success:function(data){
            console.log(this.url);
                  if(data){
                      key_input.val(key);
                      key_btn.text(txt_copy);
                  }
         }
   });
}
function makekey() {
  var text = "";
  var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

  for (var i = 0; i < 32; i++)
    text += possible.charAt(Math.floor(Math.random() * possible.length));

  return text;
}