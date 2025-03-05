document.getElementById("login-form").addEventListener("submit", async function (event) {
            event.preventDefault();
            let email = document.getElementById("email").value;
            let password = document.getElementById("password").value;

            let response = await fetch("/api/login/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken")
                },
                credentials: "include",
                body: JSON.stringify({ email, password }),
            });

            let data = await response.json();

            // Redirecionar para a home
            if (response.ok) {
                window.location.href = "/";
            } else {
                alert(data.error || "Erro no login");
            }
        });

        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== "") {
                let cookies = document.cookie.split(";");
                for (let i = 0; i < cookies.length; i++) {
                    let cookie = cookies[i].trim();
                    if (cookie.startsWith(name + "=")) {
                        cookieValue = cookie.substring(name.length + 1);
                        break;
                    }
                }
            }
            return cookieValue;
        }