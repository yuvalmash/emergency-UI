function img_create(src, alt, title) {
    var img = document.createElement('img');
    img.src = src;
    if ( alt != null ) img.alt = alt;
    if ( title != null ) img.title = title;
    return img;
}


fetch(`/forces/get_event_data?token=${"Yt-03UGyIbGAOeeOVRhYw-KS0AQZmi6ZVIVvN_G3aMR"}`)
    .then((r) => {
        return r.json();
    })
    .then(function (response) {
    var lat = response['lat']
    var lon = response['lon']
    var address1 = response['address1']
    var address2 = response['address2']
    var free_text = response['free_text']
    var wind_speed = response['wind_speed']
    for (index = 0; index < Object.keys(response).length; index++){
        if (Object.keys(response)[index] != 'medias' && Object.keys(response)[index] != 'token'){
            document.body.innerHTML += '<font size="5"><b>' + Object.keys(response)[index] + ': </b>' + Object.values(response)[index] + '</font><br>'
        }
    }
    var my_div = document.createElement('div')
        for (index = 0; index < response['medias'].length; index++) {
            my_div.append(img_create(response['medias'][index]))
        }
        document.body.append(my_div)
    })


