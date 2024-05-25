var slider1 = document.getElementById("slider1");
const minValue = 0;
const maxValue = 1000;

noUiSlider.create(slider1, {
    start: [minValue, minValue],
    step: 1,
    connect: true,
    range: {
        min: [minValue],
        max: [maxValue]
    },
});

var slider1Value = document.getElementById("slider1-span");

slider1.noUiSlider.on("update", function(values, handle) {
    slider1Value.innerHTML = `${values[0]} - ${values[1]}`;
});
