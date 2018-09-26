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
        let setting = ["gebiete","wfs"];
        if(_option){
            setting=_option;
        }
        let values = [];
        $.when(table.getData(setting[0])).done(function(data) {
            $.each(data, function (key, row) {
                $.each(data[key]['indicators'], function (key, value) {
                    values.push({
                        "name": value.ind_name_short,
                        "url": '<a target="_blank" href="' + window.location.origin + '/ogc?id=' + key + '&service=' + setting[1] + '&key=' + user_key + '&VERSION=1.1.0&REQUEST=GetCapabilities">' + window.location.origin + '/ogc?id=' + key + '&service=' + setting[1] + '&key=' + user_key + '</a>'
                    });
                });
            });
            console.log(values);
                table.getTableObject().DataTable({
                    data: values,
                    columns: [
                        {data: 'name'},
                        {data: 'url'},
                    ]
                });
        });
    },
    getData:function(setting){
         return  $.ajax({
            type: "GET",
            url: 'https://monitor.ioer.de/monitor_test/backend/query.php',
            data: {
                values:'{"format":{"id":"'+setting+'"},"query":"getAllIndicators"}'
            }
        });

    },
    destroy:function(){
        this.getTableObject().dataTable().fnDestroy();
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