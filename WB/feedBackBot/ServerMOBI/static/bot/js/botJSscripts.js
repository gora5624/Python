function sendReqToServer() {
    var e = document.getElementById("selectIP");
    var value = e.value;
    var text = e.options[e.selectedIndex].text;
    location.href='http://192.168.0.229:5000/ServerMOBI/bot?IP='+value.replaceAll('”','');
}