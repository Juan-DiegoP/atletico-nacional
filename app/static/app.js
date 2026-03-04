document.addEventListener("DOMContentLoaded", function () {

    const modal = document.getElementById("modal");
    const openBtn = document.getElementById("openModalBtn");

    if (openBtn) {
        openBtn.addEventListener("click", () => {
            modal.style.display = "flex";
        });
    }

});