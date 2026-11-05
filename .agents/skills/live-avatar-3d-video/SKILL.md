---
name: live-avatar-3d-video
description: Comprehensive skill for building, rigging, animating, and rendering interactive 3D live avatars, real-time audio-reactive viseme lip-sync, dynamic procedural gestures, and code-driven video creation using Three.js, MMD/VRM, Web Audio FFT, Remotion, and Gemini Omni 1.1 Flash.
---

# Live 3D Avatar & Programmatic Video Creation Engine

This skill provides complete architectural patterns and production code for creating, animating, and video-rendering hyper-realistic 3D AI companion avatars (like SARA AI) and generating code-driven cinematic video presentations.

---

## 1. 3D Live Avatar Core Architecture

A state-of-the-art interactive live avatar requires 4 synchronized real-time pipelines running at 60 FPS:

```
[Audio Input / Output Stream]
         │
         ├──► [Web Audio FFT Analyser] ──► [Formant Viseme Extractor (A, I, U, E, O)] ──► [Mesh Morph Targets]
         │
         └──► [Activity Classifier] ────► [Gesture & Pose Generator (Bones)] ──────────► [Skeleton Quaternions]
                                          │
[Gaze / Pointer NDC Tracking] ────────────┼──► [Saccade & Micro-Nodding Engine]
                                          │
[Physics Spring Simulation] ──────────────┴──► [Hair, Ribbon & Cloth Dynamics] ───────► [Final WebGL Frame]
```

### Key Subsystems:
1. **Pose & Skeleton Matrix**: Quaternion-based bone rotations with rest-pose preservation and gimbal-lock-free slerp interpolation.
2. **Morph Target Weights**: Vertex morphs for facial expressions and Japanese visemes (`あ`, `い`, `う`, `え`, `お`, `ワ`, `にやり`, `まばたき`).
3. **Viseme Lip-Sync Processor**: Real-time frequency analysis mapping low/mid/high frequency spectrum bins to vowel mouth formations.
4. **Behavior & Gesture State Machine**: Non-repeating randomized conversational micro-gestures scheduled at human-like intervals (1.5s - 3.5s).
5. **Secondary Physics**: Verlet or damped spring-mass simulations on hair bones, accessories, and coat tails.

---

## 2. Real-Time Audio-to-LipSync Viseme Engine

Live avatars must articulate speech convincingly frame-by-frame. When an audio stream is active:

### Formant Frequency Bins
- **A (`あ`)**: Dominant mid-low frequencies (~700 - 1200 Hz), wide vertical jaw drop (`target.a`).
- **I (`い`)**: High frequencies (>2200 Hz) with low first formant (~300 Hz), wide horizontal mouth corner pull (`target.i`).
- **U (`う`)**: Low fundamental frequencies (~300 - 800 Hz), rounded narrow pursed lips (`target.u`).
- **E (`え`)**: Mid-high formant dispersion (~500 Hz & ~1800 Hz), half-open relaxed spread (`target.e`).
- **O (`お`)**: Low-mid formant concentration (~500 Hz & ~900 Hz), circular open aperture (`target.o`).

### Procedural Speech Fallback (Zero-Freeze Guarantee)
If the audio energy momentarily dips below the noise floor during vocal pauses, the lip-sync engine must never snap shut instantly; instead, it blends smoothly through a procedural phonetic oscillator:

```javascript
synthesiseSpeech(delta) {
  this.speechClock += delta;
  const pulse = Math.pow(Math.max(0, Math.sin(this.speechClock * Math.PI * 2 * 3.7)), 1.45);
  const cadence = 0.78 + Math.sin(this.speechClock * 0.82) * 0.18;
  const openness = Math.min(0.78, Math.max(0, (0.12 + pulse * 0.62) * cadence));
  
  // Distribute across natural conversational vowels
  const wave1 = Math.sin(this.speechClock * 2.15 + 0.7) * 0.5 + 0.5;
  const wave2 = Math.sin(this.speechClock * 1.57 + 2.1) * 0.5 + 0.5;
  
  this.target.a = wave1 * (1 - wave2) * openness;
  this.target.e = wave1 * wave2 * openness;
  this.target.o = (1 - wave1) * (1 - wave2) * 0.6 * openness;
  this.target.i = (1 - wave1) * wave2 * openness;
  this.target.openness = openness;
}
```

---

## 3. High-End Conversational Gestures & Micro-Animations

Statues feel creepy; humans constantly move with subtle breathing, weight shifts, and vocal head nodding.

### Essential Micro-Animations:
1. **Vocal Head Cadence**: As speech audio plays, add rhythmic pitch nodding (`Math.sin(time * 3.2) * 0.025 * speechWeight`) to the `head` and `neck` bones.
2. **Breathing Cycle**: Oscillate `upperBody2` and `center` translation (`y += Math.sin(time * 1.4) * 0.015`) continuously.
3. **Conversational Hand Gestures**: Alternate subtle wrist, elbow, and arm tilts every 2-3 seconds with delicate or open finger hand poses (`fe(pose, bones, 'left', 'delicate', weight)`).
4. **Emotional Eyebrow Lift**: During speech, lift eyebrows by 8-12% (`browUp: 0.12 * speechWeight`) to convey engaged, attentive intelligence.
5. **Warm Smile**: Keep mouth corners subtly elevated (`mouthCornerUpL/R: 0.16 * speechWeight`) while speaking so the character never looks stern or robotic.

---

## 4. Code-Driven Video Generation

To generate videos entirely through code without third-party subscriptions:

### Approach A: Remotion (React + Three.js Video Engine)
Remotion allows writing programmatic video compositions in React:
```tsx
import { Composition } from 'remotion';
import { AvatarScene } from './AvatarScene';

export const RemotionRoot = () => (
  <Composition
    id="SaraLiveAvatarVideo"
    component={AvatarScene}
    durationInFrames={300}
    fps={30}
    width={1920}
    height={1080}
  />
);
```
Render directly from terminal:
```bash
npx remotion render src/index.ts SaraLiveAvatarVideo out/sara_video.mp4
```

### Approach B: Gemini Omni 1.1 Flash Generative Video API
Use `@google/genai` or `google-genai` Python SDK with `gemini-omni-1.1-flash` to generate or edit high-definition video clips programmatically:
```python
from google import genai
from google.genai import types

client = genai.Client()
response = client.models.generate_videos(
    model="gemini-omni-1.1-flash",
    prompt="Cinematic 3D animation of SARA AI, a brilliant female companion with dark hair, speaking warmly in a high-tech studio.",
    config=types.GenerateVideosConfig(
        aspect_ratio="16:9",
        duration_seconds=5
    )
)
```

---

## 5. Verification & Health Checklist
- [x] **Visemes**: `あ`, `い`, `う`, `え`, `お` morph targets mapped to audio frequency formants.
- [x] **Lip-Sync Fallback**: Procedural phonetic speech synthesis active during vocal cadence.
- [x] **Gestures**: Conversational micro-gestures firing dynamically every 1.5 - 3.5 seconds.
- [x] **Eye Tracking**: Gaze tracking user pointer with saccadic jitter and periodic double blinks.
- [x] **Bone Safety**: Quaternion clamping to prevent limb inversions and ribcage clipping.
