document.getElementById("logout-btn").addEventListener("click", async function () {
        try {
            let response = await fetch("/api/logout/", {
                method: "POST",
                credentials: "include",  // Inclui cookies na requisição
            });

            if (!response.ok) {
                throw new Error("Erro ao deslogar");
            }

            let data = await response.json();
            window.location.href = "/login_user";  // Redireciona para login
        } catch (error) {
            alert("Erro ao deslogar. Tente novamente!");
            console.error("Erro no logout:", error);
        }
    });