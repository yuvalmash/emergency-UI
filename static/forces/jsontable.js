
fetch(`/forces/get_event_data?token=${"Yt-03UGyIbGAOeeOVRhYw-KS0AQZmi6ZVIVvN_G3aMR"}`)
    .then((r) => {
        return r.json();
    })
    .then(function (response) {
        // console.log(Object.keys(response[0])[0])
        timestm.append(Object.keys(response[0])[0] + Object.values(response[0])[0])
        middlepane.append(Object.keys(response[0])[1] + Object.values(response[0])[1] + Object.keys(response[0])[2] + Object.values(response[0])[2])
    })


