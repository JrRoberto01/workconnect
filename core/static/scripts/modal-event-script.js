document.addEventListener("DOMContentLoaded", function () {
  // Modal de edição
  document.querySelectorAll(".open-edit-modal").forEach(btn => {
    btn.addEventListener("click", function () {
      document.getElementById("edit-evento-id").value = this.dataset.id;
      document.getElementById("edit-nome").value = this.dataset.nome;
      document.getElementById("edit-descricao").value = this.dataset.descricao;
      document.getElementById("edit-tipo").value = this.dataset.tipo;
      document.getElementById("edit-data").value = this.dataset.data;
      document.getElementById("edit-modalidade").value = this.dataset.modalidade;
      document.getElementById("edit-link").value = this.dataset.link;
    });
  });

  // Modal de exclusão
  document.querySelectorAll(".open-delete-modal").forEach(btn => {
    btn.addEventListener("click", function () {
      const eventoId = this.dataset.id;
      const nome = this.dataset.nome;
      document.getElementById("delete-event-name").innerText = nome;
      document.getElementById("delete-form").action = `/agenda/deletar/${eventoId}/`; // ajuste se necessário
    });
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const select = document.getElementById("select-participantes");
  const selectedUsersContainer = document.getElementById("selected-users");

  function renderSelectedUsers() {
    selectedUsersContainer.innerHTML = "";
    Array.from(select.selectedOptions).forEach(option => {
      const userSpan = document.createElement("span");
      userSpan.classList.add("selected-user");
      userSpan.textContent = option.text;

      const removeBtn = document.createElement("span");
      removeBtn.textContent = " ×";
      removeBtn.classList.add("remove-user");
      removeBtn.addEventListener("click", () => {
        option.selected = false;
        renderSelectedUsers();
      });

      userSpan.appendChild(removeBtn);
      selectedUsersContainer.appendChild(userSpan);
    });
  }

  select.addEventListener("change", renderSelectedUsers);

  renderSelectedUsers();
});