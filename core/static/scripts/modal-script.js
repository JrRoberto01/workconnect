let modal_element = document.querySelector(".modal-box");
let create_event_modal = document.getElementById("createEventModal");
let bg_element = document.getElementById("fade-background");
let edit_event_modal = document.getElementById("editarModal");
let delete_modal =document.getElementById("deletarModal");

function openModal(){
    modal_element.classList.add("active");
    bg_element.classList.add("active");
}

function openEditEventModal(){
    edit_event_modal.classList.add("active");
    bg_element.classList.add("active");
}

function openDeleteEventModal(button) {
    const eventoId = button.dataset.id;
    const nome = button.dataset.nome;

    document.getElementById("delete-event-name").innerText = nome;
    document.getElementById("delete-form").action = `/agenda/deletar/${eventoId}/`;

    delete_modal.classList.add("active");
    bg_element.classList.add("active");
}

bg_element.addEventListener("click", function(){
    modal_element.classList.remove("active");
    bg_element.classList.remove("active");
    create_event_modal.classList.remove("active");
    edit_event_modal.classList.remove("active");
    delete_modal.classList.remove("active");
})