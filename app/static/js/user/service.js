const url_base =window.location.origin + '/monitor_api/';

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
            user_key=key;
        let setting = ["gebiete","wfs"],
            values = [];
        if(_option){
            setting=_option;
        }

        $.when(table.getData(setting[0])).done(function(data) {
            let get_service = function(){
                switch (setting[0]) {
                    case "gebiete":
                        return "wfs";
                    //raster and wcs are identically
                    case "raster":
                        return "wcs";
                }
            };
            $.each(data, function (key, row) {
                $.each(data[key]['indicators'], function (key, value) {
                    if(value.ogc[get_service()]==="1") {
                        console.log(value);
                        let capability_url = url_base + 'user?id=' + key + '&service=' + setting[1] + '&key=' + user_key + '&VERSION=2.0.0&REQUEST=GetCapabilities',
                            url = url_base + 'user?id=' + key + '&service=' + setting[1] + '&key=' + user_key,
                            // set the url for the map viewer link
                            url_monitor = function () {
                                if (setting[0] === "raster") {
                                    return `https://monitor.ioer.de/?raeumliche_gliederung=raster&ind=${key}`;
                                } else {
                                    return `https://monitor.ioer.de/?raeumliche_gliederung=gebiete&opacity=0.8&ind=${key}&raumgl=bld`;
                                }
                            },
                            indicator_group = `<div><b>${value.ind_name_short}</b></div><div>${value.interpretation}</div>`,
                            button_group = `<div class="btn-group" role="group" aria-label="Basic example">
                                          <a target="_blank" href="${capability_url}"><button type="button" class="btn btn-warning">GetCapabilities</button></a>
                                          <button type="button" class="btn btn-primary copy" data-url="${url}">URL-Kopieren</button>
                                          <a href="${url_monitor()}" target="_blank"><button type="button" class="btn btn-secondary info_btn">Karte</button></a>
                                        </div>`;
                        values.push({
                            "name": indicator_group,
                            "url": button_group
                        });
                    }
                });
            });
            table.getTableObject().DataTable({
                data: values,
                columns: [
                    {data: 'name'},
                    {data: 'url'},
                ],
                 "language": {
                    "url": "static/lib/datatables/german.json"
                }
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
        copyUrl:function(url){
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