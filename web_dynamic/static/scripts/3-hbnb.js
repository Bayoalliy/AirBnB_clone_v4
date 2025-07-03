document.addEventListener("DOMContentLoaded", function (){
  const amenitiesId = [];
  const amenitiesName = [];
  $(".amenities input").bind("change", function() {
      if (this.checked) {
        amenitiesId.push(this.dataset.id);
        amenitiesName.push(this.dataset.name);
      } else {
        const nameIdx = amenitiesName.indexOf(this.dataset.name);
        const idIdx = amenitiesId.indexOf(this.dataset.id);
        amenitiesName.splice(nameIdx, 1);
        amenitiesId.splice(idIdx, 1);
      }
      const displayText = amenitiesName.join(", ");
      $(".amenities > h4").text(displayText || "\u00A0");
    })

  fetch("http://3.82.128.8:5001/api/v1/status/").
    then(res => {
        if (!res.ok){
            throw new Error(res.status);
        }
        return(res.json())
    }).then(data => {
        if (data.status === "OK") {
            $("#api_status").attr("class", "available");
        }
    }).catch(err => {
        console.log("There is an error: ", err)
    })

  fetch("http://3.82.128.8:5001/api/v1/places_search/",
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({})
    }
  )
  .then(res => {
    if (!res.ok){
      throw new Error(res.status);
    }
       return(res.json())
   })
  .then(data => {
       for (place of data) {
         const guest = place.max_guest > 1 ? "Guests" : "Guest";
         const room = place.number_rooms > 1 ? "Bedrooms" : "Bedroom";
         const bath = place.number_bathrooms > 1 ? "Bathrooms" : "Bathroom";
          $("section.places").append(`
          <article>
          <div class="title_box">
            <h2>${ place.name }</h2>
            <div class="price_by_night">${place.price_by_night}</div>
          </div>
          <div class="information">
            <div class="max_guest">${place.max_guest} ${guest}</div>
            <div class="number_rooms">${place.number_rooms} ${room}</div>
            <div class="number_bathrooms">${place.number_bathrooms} ${bath}</div>
          </div>
          <div class="user">
            <b>Owner:</b> john doe
          </div>
          <div class="description">
            ${place.description}
          </div>
        </article>`
          )
      }
    }).catch(err => {
         console.log("There is an error: ", err)
    })
});

