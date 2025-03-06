let close_aside_icon = document.getElementById('close-aside');
let notification_icon = document.getElementById('notification-box');
let aside_elements = document.getElementsByTagName('aside');

close_aside_icon.addEventListener("click", function () {
    for (let aside of aside_elements) {
        aside.classList.toggle("aside-opened");
    }
});

notification_icon.addEventListener("click", function () {
    for (let aside of aside_elements) {
        aside.classList.toggle("aside-opened");
    }
});
  