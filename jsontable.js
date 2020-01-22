
// DATA = [{
//     "time": "kaki time",
//     "lat": " ", "lan": " ", "img": " ", "video": "kaki video ", "msg": "kaki msg ", "category": "category"
// }]


fetch('http://127.0.0.1:5000')
    .then((r) => {
        return r.json();
    })
    .then(function (response) {


        arr = Object.keys(response[0])

        let result = '<table>';
        for (let i = 0; i < Object.values(arr).length; i++) {
            result += '<tr>';
            result += '<td>' + Object.keys(response[0])[i] + '</td>';
            result += '<td>' + Object.values(response[0])[i] + '</td>';
            result += "</tr>";
        }
        result += "</table>";

        time.innerHTML = result
    })




