document.getElementById('contact').addEventListener("click", function() {
	document.querySelector('.bg-modal').style.display = "flex";
	document.body.classList.add("stop-scrolling");
});

document.querySelector('.close').addEventListener("click", function() {
	document.querySelector('.bg-modal').style.display = "none";
	document.body.classList.remove("stop-scrolling");
});