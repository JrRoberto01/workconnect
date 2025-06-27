document.addEventListener("DOMContentLoaded", function () {

  document.querySelectorAll(".open-edit-modal").forEach((btn) => {
    btn.addEventListener("click", function () {
      const editModal = document.getElementById("editarModal");
      if (!editModal) return;

      editModal.querySelector("#edit-evento-id").value = this.dataset.id;
      
      editModal.querySelector("#id_nome").value = this.dataset.nome;
      editModal.querySelector("#id_descricao").value = this.dataset.descricao;
      editModal.querySelector("#id_tipo").value = this.dataset.tipo;
      editModal.querySelector("#id_data").value = this.dataset.data;
      editModal.querySelector("#id_modalidade").value = this.dataset.modalidade;
      editModal.querySelector("#id_link").value = this.dataset.link;

      const participantesData = this.dataset.participantes;
      const participantesIds = participantesData ? participantesData.split(",") : [];

      const selectParticipantes = editModal.querySelector("#id_participantes"); 
      
      if (selectParticipantes) {
        for (const option of selectParticipantes.options) {
          option.selected = participantesIds.includes(String(option.value));
        }
        selectParticipantes.dispatchEvent(new Event('change'));
      }
    });
  });

  function setupPillRendering(selectElement, containerElement) {
    if (!selectElement || !containerElement) {
      return;
    }

    function renderPills() {
      containerElement.innerHTML = "";
      Array.from(selectElement.selectedOptions).forEach(option => {
        const userSpan = document.createElement("span");
        userSpan.classList.add("selected-user");
        userSpan.textContent = option.text;

        const removeBtn = document.createElement("span");
        removeBtn.textContent = " ×";
        removeBtn.classList.add("remove-user");
        removeBtn.addEventListener("click", () => {
          option.selected = false;

          selectElement.dispatchEvent(new Event('change'));
        });

        userSpan.appendChild(removeBtn);
        containerElement.appendChild(userSpan);
      });
    }

    selectElement.addEventListener("change", renderPills);

    renderPills();
  }
  const createSelect = document.querySelector("#createEventModal #id_participantes");
  const createContainer = document.querySelector("#createEventModal #selected-users");
  setupPillRendering(createSelect, createContainer);

});