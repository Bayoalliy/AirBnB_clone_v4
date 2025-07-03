document.addEventListener("DOMContentLoaded", function (){
  async function getData(url) {
    try {
      const res = await fetch(url);
      if (!res.ok) {
        console.error("Server error: ", res.status);
        return null;
      }
      const data = await res.json();
      return data;
    } catch (err) {
      console.error("Network error: ", err);
      return null;
    }
  }



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
       for (const place of data) {
         const guest = place.max_guest > 1 ? "Guests" : "Guest";
         const room = place.number_rooms > 1 ? "Bedrooms" : "Bedroom";
         const bath = place.number_bathrooms > 1 ? "Bathrooms" : "Bathroom";
         const url = `http://3.82.128.8:5001/api/v1/users/${place.user_id}`;
         getData(url)
         .then(user => {
            let userName = null;
            if (user) {
              userName = user.first_name + ' ' + user.last_name;
            }
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
              <b>Owner:</b> ${userName}
            </div>
            <div class="description">
              ${place.description}
            </div>
          </article>`)
         })
      }
    }).catch(err => {
         console.log("There is an error: ", err)
    })

  $(".filters button").bind("click", function() {
    $("section.places").empty();
    fetch("http://3.82.128.8:5001/api/v1/places_search/",
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({'amenities': amenitiesId})
    }
  )
  .then(res => {
    if (!res.ok){
      throw new Error(res.status);
    }
       return(res.json())
   })
  .then(data => {
       for (const place of data) {
         const guest = place.max_guest > 1 ? "Guests" : "Guest";
         const room = place.number_rooms > 1 ? "Bedrooms" : "Bedroom";
         const bath = place.number_bathrooms > 1 ? "Bathrooms" : "Bathroom";
         const url = `http://3.82.128.8:5001/api/v1/users/${place.user_id}`
          getData(url).then(user => {
            let userName = null;
            if (user) {
              userName = user.first_name + ' ' + user.last_name;
            }

            $("section.places").append(
            `<article>
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
              <b>Owner:</b> ${userName}
            </div>
            <div class="description">
              ${place.description}
            </div>
          </article>`)
          })
      }
    }).catch(err => {
         console.log("There is an error: ", err)
    })
  })
});

