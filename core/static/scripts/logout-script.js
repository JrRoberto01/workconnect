document.getElementById("logout-btn").addEventListener("click", async function () {
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
