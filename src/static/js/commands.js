/* Header */

const headerLogo = document.getElementById("header");
const batteryElement = document.getElementById("batteryBackground");
const memoryElement = document.getElementById("memoryBackground");

window.addEventListener("scroll", () => {
	if (window.scrollY == 0) {
		headerLogo.style.opacity = 1;
		batteryElement.style.opacity = 1;
		memoryElement.style.opacity = 1;
	} else {
		headerLogo.style.opacity = 0.3;
		batteryElement.style.opacity = 0.3;
		memoryElement.style.opacity = 0.3;
	}
});

/* Battery */

const batteryCharge = document.getElementById("batteryCharge");
const batteryIndicator = document.getElementById("batteryIndicator");
const maxBattery = 100;
const maxWidthBattery = 5.4;

function updateBattery(chargeValue) {
	
	/* Check if value returned is valid */
	if (chargeValue > 100 || chargeValue < 0 || typeof chargeValue === 'string' || typeof chargeValue === 'boolean') {
		return;
	}

	/* update width and values of the battery */
	var batteryChargeWidth = (chargeValue * maxWidthBattery) / maxBattery;
	batteryCharge.style.width = String(batteryChargeWidth) + "em";
	batteryIndicator.innerHTML  = String(chargeValue) + "%";

}

updateBattery(100); /* update on loading */


/* Memory */

const memoryCapacity = document.getElementById("memoryCapacity");
const memoryIndicator = document.getElementById("memoryIndicator");
const maxMemory = 100;
const maxHeightMemory = 6;

function updateMemory(memoryCapacityValue) {
	
	/* Check if value returned is valid */
	if (memoryCapacityValue > 100 || memoryCapacityValue < 0 || typeof memoryCapacityValue === 'string' || typeof memoryCapacityValue === 'boolean') {
		return;
	}

	/* update width and values of the battery */
	var memoryCapacityHeight = (memoryCapacityValue * maxWidthBattery) / maxBattery;
	memoryCapacity.style.height = String(memoryCapacityHeight) + "em";
	memoryIndicator.innerHTML  = String(memoryCapacityValue) + "%";

}

updateMemory(100); /* update on loading */

/* Console */

const consoleElement = document.getElementById("consoleContent");

function writeTextToConsole(text, type) {
	var element = document.createElement("p");
	element.innerHTML = text;
	element.classList.add("consoleText");
	element.classList.add(type);
	consoleElement.appendChild(element);
}


/* Update buttons */

const connectToCansat = document.getElementById("connectToCansat");
const encryptionSwitch = document.getElementById("encryptionSwitch");
const startRecord = document.getElementById("startRecord");

var cansatConnected = false;

connectToCansat.addEventListener("click", () => {
	console.log("start");

	while (cansatConnected == false) {
		setTimeout(() => {
			console.log("Waiting ...");
		}, 2000);
	}

	console.log("connected");

});