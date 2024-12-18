// Initialize a Map to store all audio players
const audioPlayers = new Map();

function initializeAudioPlayer(audioId) {
  const audioElement = document.getElementById(`audio-${audioId}`);
  const playIcon = document.getElementById(`play-icon-${audioId}`);
  const progressBar = document.querySelector(`#progress-${audioId}`);
  const timeDisplay = document.getElementById(`time-${audioId}`);
  const waveformBars = document.querySelectorAll(
    `#waveform-${audioId} .waveform-bar`
  );

  // Store the player components
  audioPlayers.set(audioId, {
    audio: audioElement,
    playIcon: playIcon,
    progressBar: progressBar,
    timeDisplay: timeDisplay,
    waveformBars: waveformBars,
    isPlaying: false,
  });

  // Add event listeners
  audioElement.addEventListener("timeupdate", () => updateProgress(audioId));
  audioElement.addEventListener("ended", () => onAudioEnded(audioId));
}

function togglePlay(audioId) {
  const player = audioPlayers.get(audioId);
  if (!player) return;

  // Stop all other playing audio
  audioPlayers.forEach((p, id) => {
    if (id !== audioId && !p.audio.paused) {
      p.audio.pause();
      p.playIcon.className = "fas fa-play";
      p.isPlaying = false;
    }
  });

  if (player.audio.paused) {
    player.audio.play();
    player.playIcon.className = "fas fa-pause";
    player.isPlaying = true;
    updateWaveform(audioId, true);
  } else {
    player.audio.pause();
    player.playIcon.className = "fas fa-play";
    player.isPlaying = false;
    updateWaveform(audioId, false);
  }
}

function updateProgress(audioId) {
  const player = audioPlayers.get(audioId);
  if (!player) return;

  const { audio, progressBar, timeDisplay } = player;
  const percent = (audio.currentTime / audio.duration) * 100;
  progressBar.value = percent;
  timeDisplay.textContent = formatTime(audio.currentTime);
  updateWaveform(audioId, true);
}

function onAudioEnded(audioId) {
  const player = audioPlayers.get(audioId);
  if (!player) return;

  player.playIcon.className = "fas fa-play";
  player.isPlaying = false;
  updateWaveform(audioId, false);
}

function updateWaveform(audioId, isPlaying) {
  const player = audioPlayers.get(audioId);
  if (!player) return;

  const { audio, waveformBars } = player;
  const progress = (audio.currentTime / audio.duration) * waveformBars.length;

  waveformBars.forEach((bar, index) => {
    if (isPlaying) {
      bar.style.animation = "waveform-animation 0.5s infinite";
      if (index <= progress) {
        bar.style.background = "#4CAF50";
      } else {
        bar.style.background = "#666";
      }
    } else {
      bar.style.animation = "none";
      bar.style.background = "#666";
    }
  });
}

function formatTime(seconds) {
  const minutes = Math.floor(seconds / 60);
  seconds = Math.floor(seconds % 60);
  return `${minutes}:${seconds.toString().padStart(2, "0")}`;
}

function playNext(currentId) {
  const audioElements = Array.from(document.querySelectorAll("audio"));
  const currentIndex = audioElements.findIndex(
    (audio) => audio.id === `audio-${currentId}`
  );
  const nextIndex = (currentIndex + 1) % audioElements.length;
  const nextId = audioElements[nextIndex].id.split("-")[1];
  togglePlay(nextId);
}

function playPrevious(currentId) {
  const audioElements = Array.from(document.querySelectorAll("audio"));
  const currentIndex = audioElements.findIndex(
    (audio) => audio.id === `audio-${currentId}`
  );
  const prevIndex =
    (currentIndex - 1 + audioElements.length) % audioElements.length;
  const prevId = audioElements[prevIndex].id.split("-")[1];
  togglePlay(prevId);
}

// Initialize all audio players when the page loads
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("audio").forEach((audio) => {
    const audioId = audio.id.split("-")[1];
    initializeAudioPlayer(audioId);
  });
});
