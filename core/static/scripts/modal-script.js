modal_element = document.querySelector(".modal-box");
create_event_modal = document.getElementById("createEventModal");
bg_element = document.getElementById("fade-background");
edit_event_modal = document.getElementById("editarModal");
delete_modal =document.getElementById("deletarModal");

function openModal(){
    modal_element.classList.add("active");
    create_event_modal.classList.add("active");
    bg_element.classList.add("active");
}

function openEditEventModal(){
    edit_event_modal.classList.add("active");
    bg_element.classList.add("active");
}

function openDeleteEventModal(){
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