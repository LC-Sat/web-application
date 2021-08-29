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


/* Update form */

const connectToCansatCheckbox = document.getElementById("connectToCansat");
const encryptDataSwitch = document.getElementById("encryptionSwitch");
const startRecord = document.getElementById("startRecord");

const checkboxs = [encryptDataSwitch, startRecord];

checkboxs.forEach(checkbox => {
	checkbox.addEventListener("change", () => {
		document.getElementById("form").submit();
	});
});

connectToCansatCheckbox.addEventListener("change", () => {

	document.getElementById("connectToCansat").disabled = true;
	document.getElementById("mainContainer").style.opacity = 0.3;
	document.getElementById("header").style.opacity = 0.3;
	document.getElementById("batteryBackground").style.opacity = 0.3;
	document.getElementById("memoryBackground").style.opacity = 0.3;
	document.getElementById("waitCansatModal").classList.add('visible');
	document.getElementById("form").submit();

});


const stopRecord = document.getElementById("stopRecord");
stopRecord.addEventListener("change", () => {
	document.getElementById("recordingForm").submit();
});
