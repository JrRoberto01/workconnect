document.getElementById("logout-btn").addEventListener("click", async function () {
<<<<<<< HEAD
        try {
            let response = await fetch("/api/logout/", {
                method: "POST",
                credentials: "include",  // Inclui cookies na requisição
            });

            if (!response.ok) {
                throw new Error("Erro ao deslogar");
            }

            let data = await response.json();
            window.location.href = "/login_user/";  // Redireciona para login
        } catch (error) {
            alert("Erro ao deslogar. Tente novamente!");
            console.error("Erro no logout:", error);
        }
    });
=======
    try {
        let response = await fetch("/api/logout/", {
            method: "POST",
            credentials: "include",  // Garante que os cookies são enviados
        });

        if (!response.ok) {
            throw new Error("Erro ao deslogar");
        }

        let data = await response.json();
        window.location.href = "/login_user/";
    } catch (error) {
        alert("Erro ao deslogar. Tente novamente!");
        console.error("Erro no logout:", error);
    }
});
>>>>>>> e09d17a6c6ec6a6c753edcaac26d90424efdbbaf
