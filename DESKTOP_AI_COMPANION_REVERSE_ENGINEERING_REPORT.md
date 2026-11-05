# Reverse Engineering & Architecture Audit: Desktop AI Companion, Desktop Maid & SARA Integration

**Prepared For**: Muhammad Mubashar (Pasha Dev)  
**System**: SARA AI (Live 3D Neural Desktop Companion)  
**Date**: October 2026  
**Audited Targets**:
1. [Desktop AI Companion by Dokk75](https://dokk75.itch.io/desktop-ai-companion) (Itch.io / Steam)
2. [DesktopCompanion by heshanthenura](https://github.com/heshanthenura/DesktopCompanion) (GitHub)
3. **Desktop Maid / DesktopMate** (Steam Community)
4. [TalkingHead by met4citizen](https://github.com/met4citizen/TalkingHead) (GitHub)

---

## 1. Executive Summary & Benchmark Matrix

| Feature / Metric | Dokk75 Desktop AI Companion | Desktop Maid (Steam) | TalkingHead (met4citizen) | SARA AI (Pasha Dev Edition) |
|---|---|---|---|---|
| **App Runtime** | Electron (Windows Overlay) | Unity / C++ Layered Window | Three.js / Web Browser | **Electron + React 19 + Three.js 0.180** |
| **Window Mode** | Always-on-top transparent overlay | Layered frameless desktop pet | Web canvas container | **Frameless desktop companion on port 3344** |
| **Model Formats** | **VRM** (3D) + **Live2D** (2D) | **VRM** (VRoid Humanoid) | **GLB** (Mixamo / ReadyPlayerMe) | **PMX (Cyber SARA) + GLB (vroid.glb, brunette.glb)** |
| **Lip-Sync Method** | Web Audio FFT + Amplitude Envelope | Waveform jaw-flap / blendshapes | Phoneme viseme rules + FFT binning | **Hardcore Audio-Reactive FFT + Procedural Phonetic Visemes** |
| **Idle Animation** | Breathing, random blinking, gaze | Spring bones, mouse tracking | Saccadic eye drift, head tilts | **3x Boosted Idle Breathing, Sway, Gaze & Saccades** |
| **Screen Vision** | Periodic desktop screenshots | None / limited | None | **Live electron desktopCapturer (1440p) to Gemini Live** |
| **Voice / Brain** | Ollama / Gemini / Kokoro / ElevenLabs | Local LLM / Cloud API | Web Speech / Cloud TTS | **Gemini 3.1 Live 24kHz Bidirectional WebSocket** |
| **System Autonomy** | Chat companion only | Chat & desktop decoration | Visualizer only | **77+ Windows Desktop Tools (Paint Tutor, Browser, WhatsApp)** |

---

## 2. Deep Reverse Engineering: Dokk75 Desktop AI Companion

### Architecture & Runtime
* **Shell**: Windows Electron application utilizing:
  ```javascript
  const win = new BrowserWindow({
    transparent: true,
    frame: false,
    alwaysOnTop: true,
    hasShadow: false,
    webPreferences: { backgroundThrottling: false }
  });
  ```
* **Graphics Engine**: WebGL with transparent canvas (`gl.clearColor(0,0,0,0)`), allowing the anime character to sit directly on the Windows wallpaper or float above active IDEs and browser windows.
* **Model Pipeline**:
  * Leverages `@pixiv/three-vrm` to parse `.vrm` files (which are glTF 2.0 archives containing VRM humanoid extensions, spring-bone definitions, and standardized blendshape expressions).
  * Shipped with 9 preset personas (*Alice, Michael, Amelia, Yui, Rei, Iris, Lyra, Marc, Kiki*), plus an open file importer allowing users to drag and drop any VRM from VRoid Hub or Booth.pm.
* **Audio & Lip-Sync Pipeline**:
  * Audio is split through a Web Audio `AnalyserNode` (`fftSize = 256` or `512`).
  * Energy in the 300Hz–3500Hz vocal spectrum is binned into 5 vowel targets:
    * Low frequency energy -> `Fcl_MTH_A` / `Fcl_MTH_O` (open jaw).
    * Mid-high energy -> `Fcl_MTH_I` / `Fcl_MTH_E` (wide smile/teeth).
    * Low energy / pauses -> smooth exponential release to closed mouth.

---

## 3. Reverse Engineering: Desktop Maid (Steam)

### Capabilities & Gotchas
* **Rendering**: Built in Unity, using Windows native user32 APIs (`SetWindowLong`, `SetLayeredWindowAttributes`, `DwmExtendFrameIntoClientArea`) to produce transparent click-through or interactive zones.
* **Physics Rig**: Features spring bones for hair, breasts, ribbons, and aprons that react to desktop window movement and cursor velocity.
* **Key Limitation Identified**: On initial launch, Desktop Maid downloads a heavy local model (~5 minutes of CPU thrashing) which frustrates users on integrated graphics machines. SARA avoids this by connecting directly to Gemini Live WebSocket for zero local GPU overhead.

---

## 4. Implementation in SARA: Hardcore Avatar Overhaul

Based on the reverse engineering of Dokk75 and Desktop Maid, the following upgrades have been completed in SARA:

### 1. Audio-Reactive Lip-Sync Engine (Fixing Frozen Lips)
* **Root Cause Found**: In `index-qnLjC2CG.js`, speech authority was gated strictly on `T.activity === "talking"`. When Gemini Live emitted `activity: "speaking"`, speech authority dropped to zero and reset the mouth morphs to 0 every frame.
* **Engineering Fix**:
  ```javascript
  let hasAudio = false;
  if (T.outputAnalyser) {
    try {
      const dArr = new Uint8Array(32);
      T.outputAnalyser.getByteFrequencyData(dArr);
      let sum = 0;
      for (let k = 0; k < dArr.length; k++) sum += dArr[k];
      if (sum > 60) hasAudio = true;
    } catch(e) {}
  }
  const A = T.activity === "talking" || T.activity === "speaking" || 
            this.currentActivity === "talking" || this.currentActivity === "speaking" || 
            hasAudio || this.speechAuthority > 0.1;
  ```
  Now, whenever audio is detected in the output analyser OR speech activity is flagged, SARA's mouth animates dynamically with vocal pitch and volume.

### 2. Multi-Model 3D Asset Roster
Downloaded and packaged industry-standard 3D humanoid models in `D:\MARAA AI\SARA\resources\app\dist\assets\characters\`:
1. **SARA Cyber Live** (`evelyn/model.pmx`): Customized metallic platinum silver-lilac hair, electric sapphire glowing irises, and obsidian cyberpunk jacket.
2. **SARA Anime VRM** (`vroid/vroid.glb`): 2.34 MB compact Anime 3D humanoid avatar with full ARKit blendshapes and spring hair physics.
3. **SARA Real 3D** (`brunette/brunette.glb`): 4.50 MB ReadyPlayerMe companion avatar with photorealistic facial rig.

### 3. MS Paint AI Tutor & Foreground Browser Automation
* **MS Paint**: Upgraded `explain_concept_in_paint` in `sara_neural_brain.py` to auto-activate the Paint window via `$wshell.AppActivate('Paint')` and maximize via `Alt+Space, X`.
* **Browser**: Integrated `navigate_and_interact_browser` which activates Chrome/Edge in the foreground, targets the address bar with `Ctrl+L`, safely pastes text using the Windows Unicode clipboard pipeline, and presses `Enter`.
