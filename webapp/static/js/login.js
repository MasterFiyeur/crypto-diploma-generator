async function login(){
	let email = document.getElementById("email").value;
	let password = document.getElementById("password").value;
	console.log(email, password);
	fetch("/api/login", {
		method: "POST",
		headers: {
			"Content-Type": "application/json"
		},
		body: JSON.stringify({
			email: email,
			password: password
		})
	}).then(response => {
		if (response.status === 200){
			window.location.href = "/home";
		} else {
			alert("Login failed");
		}
	});
}