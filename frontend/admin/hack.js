icon = document.getElementById("new emergency")
time = document.getElementById("time")

var today = new Date();
var h = String(today.getHours()).padStart(2, '0')
var m = String(today.getMinutes()).padStart(2, '0')
var s = String(today.getSeconds()).padStart(2, '0')
var dd = String(today.getDate()).padStart(2, '0');
var mm = String(today.getMonth() + 1).padStart(2, '0');
var yyyy = today.getFullYear();

function startEmergency() {
    time.innerHTML = dd + '/' + mm + '/' + yyyy + "   " + h + ":" + m + ":" + s
    document.getElementById("formId").classList.remove("form")
    icon.style.display = "none"
}