document.addEventListener("DOMContentLoaded", function () {

    const modal = document.getElementById("modal");
    const openBtn = document.getElementById("openModalBtn");
    const form = document.getElementById("videoForm");
    const feed = document.getElementById("feed");

    // 🔥 Abrir modal
    openBtn.addEventListener("click", () => {
        modal.style.display = "flex";
    });

    // 🔥 Cerrar modal al hacer click afuera
    modal.addEventListener("click", (e) => {
        if (e.target === modal) {
            modal.style.display = "none";
        }
    });

    // 🔥 Cargar videos
    async function cargarVideos() {
        try {
            const response = await fetch("/api/videos");
            const videos = await response.json();

            feed.innerHTML = "";

            videos.forEach(video => {
                const card = document.createElement("div");
                card.classList.add("video-card");

                card.innerHTML = `
                    <video src="${video.video_url}" autoplay muted loop playsinline></video>
                    <div class="info">
                        <h3>⚽ ${video.titulo}</h3>
                        <p>🏟 ${video.partido}</p>
                        <p>⏱ Min ${video.minuto}</p>
                        <p>👤 ${video.autor}</p>
                    </div>
                `;

                feed.appendChild(card);
            });

        } catch (error) {
            console.error("Error cargando videos:", error);
        }
    }

    // 🔥 Subir video
    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        const formData = new FormData(form);

        const response = await fetch("/api/videos", {
            method: "POST",
            headers: {
                "Authorization": "Bearer " + localStorage.getItem("token")
            },
            body: formData
        });

        if (response.ok) {
            modal.style.display = "none";
            form.reset();
            await cargarVideos(); // 🔥 Recarga el feed
        } else {
            alert("Error al subir video");
        }
    });

    // 🔥 Cargar al iniciar
    cargarVideos();

});