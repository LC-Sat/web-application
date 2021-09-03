const ydata = document.querySelectorAll(".data");
const xdata = document.getElementById("xData");

const pressionCheckbox = document.getElementById("pression")
pressionCheckbox.disabled = true;

xdata.addEventListener("change", () => {

	ydata.forEach(d => {
		d.disabled = false;
	});

	if (xdata.value != "time") {

		ydata.forEach(d => {

			if (d.id == xdata.value) {
				d.disabled = true;
			}

		});

	}

});