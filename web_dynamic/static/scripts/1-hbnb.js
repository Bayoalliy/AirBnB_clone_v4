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
});

