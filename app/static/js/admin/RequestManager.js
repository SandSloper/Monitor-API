class RequestManager{
    static updateOGCService(_service){
        console.info("create services for: ",_service);
        return axios.post('https://monitor.ioer.de/monitor_api/admin/'+_service);
    }
}