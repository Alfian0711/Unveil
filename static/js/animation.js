const form = document.getElementById('scan-form');
const fileInput = document.getElementById('file-input');
const loadingIndicator = document.getElementById('loading-indicator');

form.addEventListener('submit', (e) => {
  e.preventDefault();

  const file = fileInput.files[0];
  const formData = new FormData();
  formData.append('file', file);

  fetch('/scan', {
    method: 'POST',
    body: formData,
  })
  .then((response) => response.json())
  .then((data) => {
    if (data.status === "loading") {
      // Tampilkan loading indicator
      loadingIndicator.style.display = 'block';

      // Tunggu hasil dari server
      const intervalId = setInterval(() => {
        fetch('/scan_result')
        .then((response) => response.json())
        .then((data) => {
          if (data.status === "success") {
            // Tampilkan hasil
            const art = data.art;
            const filename = data.filename;
            const confidence = data.confidence;

            // ...

            // Hilangkan loading indicator
            loadingIndicator.style.display = 'none';

            clearInterval(intervalId);
          } else if (data.status === "failed") {
            // Tampilkan pesan error
            console.error('Task gagal');

            // Hilangkan loading indicator
            loadingIndicator.style.display = 'none';

            clearInterval(intervalId);
          }
        })
        .catch((error) => console.error(error));
      }, 1000);
    }
  })
  .catch((error) => console.error(error));
});
// JavaScript untuk smooth scroll

// Inisialisasi ScrollReveal
const sr = ScrollReveal({
    duration: 1000, // Durasi animasi (ms)
    easing: 'ease',
    distance: '50px', // Jarak elemen muncul dari bawah
    origin: 'bottom', // Arah elemen muncul
    reset: true // Elemen kembali tersembunyi saat menggulir kembali
});

// Menentukan elemen yang akan dianimasikan
sr.reveal('.scroll-reveal', {
    interval: 200 // Interval antara setiap elemen
});


sr.reveal(`.about__Unveil`)
sr.reveal(`.about,.about`, {delay: 500})
sr.reveal(`.home__social`, {delay: 600})
sr.reveal(`.about_section, .layout_padding`,{origin: 'left'})
sr.reveal(`.book_section`,{origin: 'right'})
sr.reveal(`.footer_section`,{interval: 1000})
