document.getElementById("login-form").addEventListener("submit", async function (event) {
    event.preventDefault();
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;

    let response = await fetch("/api/login/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
    });

    let data = await response.json();
    if (response.ok) {
        window.location.href = "/";  // Redireciona para a home após login
    } else {
        alert(data.error || "Erro no login");
    }
});
