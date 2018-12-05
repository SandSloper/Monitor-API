const url_base =window.location.origin + '/monitor_api/';
//TODO noch auf react umstellen !
$(document).ready(function(){
    table.init(false);
    checkbox.init();
});
const table={
    getTableObject:function(){
        $elem = $('#service_table');
        return $elem;
    },
    init:function(_option){
        const table = this,
            user_key=this.getTableObject().data('key');
        let setting = ["gebiete","wfs"],
            values = [];
        if(_option){
            setting=_option;
        }

        $.when(table.getData(setting[0])).done(function(data) {
            console.log(data);
            $.each(data, function (key, row) {
                $.each(data[key]['indicators'], function (key, value) {
                    let capability_url = url_base + '/ogc?id=' + key + '&service=' + setting[1] + '&key=' + user_key + '&VERSION=1.1.0&REQUEST=GetCapabilities',
                        url=url_base + '/ogc?id=' + key + '&service=' + setting[1] + '&key=' + user_key,
                        button_group = '<div class="btn-group" role="group" aria-label="Basic example">'+
                                          '<a target="_blank" href="'+capability_url+'"><button type="button" class="btn btn-warning">GetCapabilities</button></a>'+
                                          '<button type="button" class="btn btn-primary copy" data-url="'+url+'">URL-Kopieren</button>'+
                                          '<button type="button" class="btn btn-secondary info_btn" data-title="'+value.ind_name+'" data-info="'+value.interpretation+'" data-methodik="'+value.methodik+'">Indikator-Info</button>'+
                                        '</div>';
                    values.push({
                        "name": value.ind_name_short,
                        "url": button_group
                    });
                });
            });
            table.getTableObject().DataTable({
                data: values,
                columns: [
                    {data: 'name'},
                    {data: 'url'},
                ]
            });
            table.button.init();
        });
    },
    getData:function(setting){
        console.log(setting);
         return  $.ajax({
            type: "POST",
            url: 'https://monitor.ioer.de/backend/query.php',
            data: {
                values:'{"format":{"id":"'+setting+'"},"query":"getAllIndicators"}'
            },
            success:function(){
                console.log(this.url);
            }
        });

    },
    destroy:function(){
        this.getTableObject().dataTable().fnDestroy();
    },
    button:{
        init:function(){
            const object = this;
            $('#info_modal').modal({ show: false});
            $(document).on('click','.info_btn',function(){
                object.showInfo($(this).data('title'),$(this).data('info'),$(this).data('methodik'));
            });
            $(document).on('click','.copy',function(){
                object.copyUrl($(this).data('url'));
            });
        },
        showInfo:function(title,info,methodik,times){
            const info_dialog = $('#info_modal');
            info_dialog.find('#modal_title').text(title);
            info_dialog.find('#modal_interpretation').text(info);
            info_dialog.find('#modal_methodik').text(methodik);
            info_dialog.modal('show');
        },
        copyUrl:function(url){
            console.log(url);
            var $temp = $("<input>");
            $("body").append($temp);
            $temp.val(url).select();
            document.execCommand("copy");
            $temp.remove();
        }
    }
};
const checkbox={
    getContainerObject:function(){
        $elem = $('.services').find('form');
        return $elem;
    },
    init:function(){
        const check = this;
        check.getContainerObject()
            .find('input:radio')
            .change(function(){
                let val = $(this).val();
                table.destroy();
                if(val === "wcs"){
                    table.init(["raster","wcs"])
                }else{
                    table.init(false);
                }
            });
    }
};