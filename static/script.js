const video = document.getElementById('video');
const fotosDiv = document.getElementById('fotos');
const btnEnviar = document.getElementById('enviar');
let fotos = [];

navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => { video.srcObject = stream });

function tirarFoto() {
  const canvas = document.createElement('canvas');
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext('2d').drawImage(video, 0, 0);
  const dataURL = canvas.toDataURL('image/jpeg');
  fotos.push(dataURL);
  const img = document.createElement('img');
  img.src = dataURL;
  img.width = 100;
  fotosDiv.appendChild(img);
  if (fotos.length === 3) {
    btnEnviar.disabled = false;
  }
}

function enviarFotos() {
  fetch('/upload', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ photos: fotos })
  })
    .then(res => res.json())
    .then(data => {
      document.getElementById('resultado').innerHTML = `
        <p><strong>Código:</strong> ${data.codigo}</p>
        <img src="/qrcode/${data.codigo}" width="150">
      `;
    });
}
