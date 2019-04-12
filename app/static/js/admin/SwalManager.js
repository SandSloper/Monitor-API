class SwalManager{
    static setError(){
        swal({
            title:"Fehler",
            text:`<div class="text-danger font-weight-bold">Es ist ein Fehler aufgetreten. <i class="far fa-frown"></i></div>`,
            type:"error",
            html:true
        });
    }
    static setLoading(type){
        let _type = "info";
        if(type){
           _type = type;
        }
       swal({
            title:"Loading...",
            text:`
              <div class="progress bg-${_type}" id="progressbar">
                  <div class="progress-bar progress-bar-striped" role="progressbar" style="width: 0%;" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>
                </div>
            `,
            type:"info",
            html:true,
            showConfirmButton: false
        });
        var elem = document.getElementById("progressbar");
        var width = 1;
        var time = 500;
        var id = setInterval(frame, time);
        function frame() {
            if (width >= 100) {
              clearInterval(id);
              width=1;
              id = setInterval(frame, time);
            } else {
              width++;
              elem.style.width = width + '%';
            }
        }
    }
    static removeDialog(){
        swal.close();
    }
}