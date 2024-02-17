const video = document.getElementById("vid");
const canvas = document.getElementById("canvas");
const captureButton = getElementById("cap_button");
const image = getElementById("im");

navigator.mediaDevices.getUserMedia({ video: true})
.then((stream) => {
	video.srcObject = stream
})
.catch()
