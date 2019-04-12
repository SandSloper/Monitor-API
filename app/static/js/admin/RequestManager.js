class RequestManager{
    static updateOGCService(_service){
        return axios.post('https://monitor.ioer.de/monitor_api/admin/'+_service);
    }
}