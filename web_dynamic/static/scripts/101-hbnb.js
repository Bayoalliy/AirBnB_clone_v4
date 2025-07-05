document.addEventListener("DOMContentLoaded", function (){
  async function getData(url) {                                                                                                                  try {                                                                                                                                          const res = await fetch(url);
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

  function formatDate(dateString) {
      const date = new Date(dateString);
      const options = { day: '2-digit', month: 'long', year: 'numeric' };
      return date.toLocaleDateString('en-US', options);
  }

  function getReviews(place_id) {
    getData(`http://3.82.128.8:5001/api/v1/places/${place_id}/reviews`)
        .then(data => {
          if (data) {
            for (const review of data) {
              const date = formatDate(review.created_at)
              getData(`http://3.82.128.8:5001/api/v1/users/${review.user_id}`)
              .then(user => {
                if (user) {
                  $(`article#${place_id} ul`).append(`
                    <li>
                      <h3>From ${user.first_name} ${user.last_name} on the ${date}</h3>
                      <p>${review.text}</p>
                    </li>`
                  )
                }
              })
            }
          }
        })
  }

  function addPlace(place, userName) {
    $("section.places").append(`
          <article id=${place.id}>
            <div class="title_box">
              <h2>${ place.name }</h2>
              <div class="price_by_night">${place.price_by_night}</div>
            </div>
            <div class="information">                                                                                                                      <div class="max_guest">${place.max_guest} Guest${place.max_guest > 1 ? "s" : ""}</div>
              <div class="number_rooms">${place.number_rooms} Room${place.number_rooms > 1 ? "s" : ""}</div>
              <div class="number_bathrooms">${place.number_bathrooms} Bathroom${place.number_bathrooms > 1 ? "s" : ""}</div>
            </div>
            <div class="user">
              <b>Owner:</b> ${userName}
            </div>
            <div class="description">
              ${place.description}
            </div>
            <div class="reviews">
              <h2>Reviews</h2><span class="off">Show</span>
              <ul></ul>
          </article>`)

          $(`article#${place.id} span`).bind("click", function() {
            if ($(this).attr("class") === "off") {
              getReviews(place.id)
              $(this).attr("class", "on")
              $(this).text("Hide");
            } else {
              $(`article#${place.id} ul`).empty()
              $(this).attr("class", "off")
              $(this).text("Show");
            }
          })
  }

  const amenitiesId = [];
  const amenitiesName = [];
  const statesId = [];
  const statesName = [];
  const citiesId = [];
  const citiesName = [];

  $(".filters input").bind("change", function() {
      if (this.checked) {
        if ($(this).parent().parent().parent().html() === $(".amenities .popover").html()) {
          amenitiesId.push(this.dataset.id);
          amenitiesName.push(this.dataset.name);
        } else if ($(this).parent().parent().parent().html() === $(".popover #state").html()) {
          console.log(true);
          statesId.push(this.dataset.id);
          statesName.push(this.dataset.name);
          console.log("stateName: ", this.dataset.name)
        } else {
          console.log(false)
          citiesId.push(this.dataset.id);
          citiesName.push(this.dataset.name);
        }
      } else {
        let nameIdx = amenitiesName.indexOf(this.dataset.name);
        let idIdx = amenitiesId.indexOf(this.dataset.id);

        if ($(this).parent().parent().parent().html() === $(".amenities .popover").html()) {
          amenitiesName.splice(nameIdx, 1);
          amenitiesId.splice(idIdx, 1);
        } else if ($(this).parent().parent().parent().html() === $(".popover #state").html()) {
          nameIdx = statesName.indexOf(this.dataset.name);
          idIdx = statesId.indexOf(this.dataset.id);
          statesName.splice(nameIdx, 1);
          statesId.splice(idIdx, 1);
        } else {
          nameIdx = citiesName.indexOf(this.dataset.name);
          idIdx = citiesId.indexOf(this.dataset.id);
          citiesName.splice(nameIdx, 1);
          citiesId.splice(idIdx, 1);
        }

      }
      console.log("states: ", statesName);
      console.log("cities: ", citiesName);
      const amenitiesDisplayText = amenitiesName.join(", ");
      const locationsDisplayText = statesName.concat(citiesName).join(", ");
      $(".amenities > h4").text(amenitiesDisplayText || "\u00A0");
      $(".locations > h4").text(locationsDisplayText || "\u00A0");
    })

  fetch("http://3.82.128.8:5001/api/v1/status/").
    then(res => {
        if (!res.ok){
            throw new Error(res.status);
        }
        return(res.json())
    }).then(data => {
        if (data.status === "OK") {                                                                                                                      $("#api_status").attr("class", "available");
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
         const url = `http://3.82.128.8:5001/api/v1/users/${place.user_id}`;
         getData(url)
         .then(user => {
            let userName = null;
            if (user) {                                                                                                                                    userName = user.first_name + ' ' + user.last_name;                                                                                         }
            addPlace(place, userName);
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
      body: JSON.stringify({
              'amenities': amenitiesId,
              'states': statesId,
              'cities': citiesId
      })
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
            addPlace(place, userName);
          })
      }
    }).catch(err => {
         console.log("There is an error: ", err)
    })
  })
});
