
document.addEventListener("DOMContentLoaded", function() {
	const popbutton = document.getElementById("pp");
	const logout = document.getElementById("logout");

	popbutton.addEventListener("click", () => {
		showPopover();
	});
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
