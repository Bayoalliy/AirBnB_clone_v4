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
});
