const chatInput = document.getElementById('chat-input');
const toggleIcon = document.getElementById('toggle-icon');
const msgBox = document.getElementById('msg_box');
let btnStatus = 'inactive', mediaRecorder, chunks = [];

function sendDataToStreamlit(data) {
    const jsonData = JSON.stringify(data);
    window.parent.postMessage({ type: 'input_data', value: jsonData }, '*');
    console.log("Data sent to Streamlit:", jsonData);
}

chatInput.addEventListener('input', () => {
    if (chatInput.value.trim().length > 0) {
        toggleIcon.innerHTML = '<i class="fas fa-paper-plane"></i>';
    } else if (btnStatus !== 'recording') {
        toggleIcon.innerHTML = '<i class="fas fa-microphone"></i>';
    }
});

toggleIcon.addEventListener('click', () => {
    if (chatInput.value.trim().length > 0) {
        sendDataToStreamlit({ text: chatInput.value });
        chatInput.value = '';
        toggleIcon.innerHTML = '<i class="fas fa-microphone"></i>';
    } else {
        if (btnStatus === 'inactive') {
            startRecording();
        } else if (btnStatus === 'recording') {
            stopRecording();
        }
    }
});

function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.start();
        btnStatus = 'recording';
        toggleIcon.innerHTML = '<i class="fas fa-stop"></i>';
        msgBox.innerHTML = 'Recording...';

        mediaRecorder.ondataavailable = event => {
            chunks.push(event.data);
        };

        mediaRecorder.onstop = () => {
            const audioBlob = new Blob(chunks, { 'type': 'audio/ogg; codecs=opus' });
            chunks = [];
            handleAudioInput(audioBlob);
        };
    }).catch(error => {
        console.error("Error accessing microphone:", error);
        msgBox.innerHTML = 'Error accessing the microphone';
    });
}

function stopRecording() {
    if (mediaRecorder) {
        mediaRecorder.stop();
        btnStatus = 'inactive';
        toggleIcon.innerHTML = '<i class="fas fa-microphone"></i>';
        msgBox.innerHTML = 'Press the microphone to start recording';
    }
}

function handleAudioInput(audioBlob) {
    const reader = new FileReader();
    reader.readAsDataURL(audioBlob);
    reader.onloadend = function () {
        const base64String = reader.result.split(',')[1];
        sendDataToStreamlit({ audio: base64String });
    };
}