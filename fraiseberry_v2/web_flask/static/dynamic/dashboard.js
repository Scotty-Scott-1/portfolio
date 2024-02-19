
document.addEventListener("DOMContentLoaded", function() {
	const popbutton = document.getElementById("pp");
	const pref_icon = document.getElementById("prefs");
	const camera = document.getElementById("camera");
	let profile_pic = document.getElementById("pp");

	popbutton.addEventListener("click", () => {
		showPopover();
	});

	pref_icon.addEventListener("click", () => {
		window.location.href="/preferences/"
	});

	camera.addEventListener("click", () => {
		window.location.href="/camera/"
	});

	profile_pic.src = ""

});





	function showPopover () {
		const pop = document.getElementById("popover")
		if (pop.style.display === "none") {
			pop.style.display= "block";
			pop.classList.remove("hidden");
		}
		else {
			pop.classList.add("hidden");
			pop.style.display = "none";
		}
	}
