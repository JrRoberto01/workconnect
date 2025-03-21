modal_element = document.querySelector(".modal-box");
bg_element = document.getElementById("fade-background");

function openModal(){
    modal_element.classList.add("active");
    bg_element.classList.add("active");
}

bg_element.addEventListener("click", function(){
    modal_element.classList.remove("active");
    bg_element.classList.remove("active");
})