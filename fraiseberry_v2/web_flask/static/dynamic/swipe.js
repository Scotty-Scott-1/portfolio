
document.addEventListener("DOMContentLoaded", function() {
	const candidates = document.querySelectorAll(".card");
	let index = 0;

	function show(index) {
		candidates.forEach((candidate, idx) => {
			if(idx === index) {
				candidate.classList.add('active')
				let yes = candidate.querySelector("#yes");
				let no = candidate.querySelector("#no");

				yes.addEventListener("click", () => {
					index++;
					if (index >= candidates.length) {
						index = 0;
						alert("Your search results are delepeted. Swipe again or widen your search")
						window.location.href = '/dashboard/';
					}
					show(index);
					console.log(index);

					user_name_element = candidate.querySelector("#card_info_2");
					user_name = user_name_element.textContent;
					const form_data = {
						canidate_user_name: user_name,
					};
					fetch('/swipe/', {
						method: "POST",
						body: JSON.stringify(form_data),
						headers: {"Content-Type": "application/json"}

					})

					.then(response => response.json());
				});


				no.addEventListener("click", () => {
					index++;
					if (index >= candidates.length) {
						index = 0;
						alert("Your search results are delepeted. Swipe again or widen your search")
						window.location.href = '/dashboard/';
					}
					show(index);
					console.log(index);
				});
			} else {
				candidate.classList.remove('active')
			}
		});
	}

	show(index);
});

function like() {

}

