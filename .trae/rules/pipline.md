# Video Printer Project Rules

## 1. Project Overview
This project is an automated video generation pipeline ("Video Printer") that converts a source URL and user prompt into a new video. It analyzes the source content, re-imagines it based on the prompt, and generates new assets (scripts, images, audio, video) to assemble the final output.

## 2. Directory Structure & Key Files
- `app.py`: Main Flask application entry point.
- `pipeline.py`: Core logic for the video generation pipeline.
- `templates/`: HTML templates for the UI.
- `static/`: Static assets (CSS, generated video output).
- `scripts/`: Text files for video analysis and scene scripts.
- `charectors/`: Python classes defining characters.
- `charectorImages/`: Generated images for characters.
- `backgrounds/`: Python classes defining scenes/backgrounds.
- `backgroundImages/`: Generated images for backgrounds.
- `frames/`: Keyframes generated for each scene.
- `footages/`: Video clips generated for each scene.
- `.env`: (Not committed) Stores API keys and secrets.
- `.env.example`: Template for environment variables.

## 3. Pipeline Steps & AI Model Requirements

### Step 1: Video Analysis
- **Input**: Source URL.
- **Action**: Analyze video content using `yt-dlp` (metadata) and LLM (content understanding).
- **Output**: `scripts/1video_description.txt` containing character, scene, event, action, and camera descriptions.
- **Model**: **LLM** (e.g., OpenAI GPT-4).

### Step 2: Character Generation
- **Input**: Character descriptions from Step 1.
- **Action**: Generate character visual consistency classes and reference images.
- **Output**: 
    - Images: `charectorImages/charectorImage_{name}.jpg`
    - Code: `charectors/{name}.py`
- **Models**: 
    - **Image Generation** (e.g., DALL-E 3, Midjourney).
    - **Audio Generation** (e.g., ElevenLabs) for character voice profiles.

### Step 3: Background Generation
- **Input**: Scene descriptions from Step 1.
- **Action**: Generate scene/background reference images and classes.
- **Output**:
    - Images: `backgroundImages/background_{name}.jpg`
    - Code: `backgrounds/{name}.py`
- **Models**:
    - **Image Generation** (e.g., DALL-E 3, Midjourney).
    - **Audio Generation** (e.g., ElevenLabs) for ambient sound profiles.

### Step 4: Script Generation
- **Input**: User prompt + Video Description (Step 1).
- **Action**: Generate a sequence of short scripts (3-5 seconds each).
- **Output**: `scripts/script_{index}.txt`.
- **Model**: **LLM** (e.g., OpenAI GPT-4).

### Step 5: Frame Generation
- **Input**: Scene scripts (Step 4) + Character/Background assets (Step 2 & 3).
- **Action**: Compose start/end frames for each event.
- **Output**: `frames/frame_{index}.jpg`.
- **Model**: **Image Generation** (e.g., DALL-E 3, Stable Diffusion) - strictly following asset consistency.

### Step 6: Footage Generation
- **Input**: Scripts + Frames.
- **Action**: Generate video clips from static frames and prompts.
- **Output**: `footages/footage_{index}.mp4`.
- **Model**: **Video Generation AI** (e.g., Runway Gen-2, Pika, Stable Video Diffusion).

### Step 7: Video Assembly
- **Input**: Footages.
- **Action**: Concatenate clips into final video.
- **Output**: `output.mp4` (in root and `static/`).
- **Tools**: `moviepy`.

## 4. Development Rules
- Use `.env` for all sensitive tokens. Never commit keys.
- Prefer MCP tools where applicable.
- Ensure the pipeline remains runnable even if some models are mocked (use fallback logic if keys are missing).
