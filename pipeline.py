import os
import json
import yt_dlp
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, concatenate_videoclips, AudioFileClip, TextClip, CompositeVideoClip
import time
import random

# Ensure directories exist
DIRS = [
    'scripts', 'charectorImages', 'backgrounds', 'backgroundImages', 
    'charectors', 'frames', 'footages', 'static'
]
for d in DIRS:
    os.makedirs(d, exist_ok=True)

def step1_analyze_video(url):
    """
    Step 1: Analyze URL video content.
    Uses yt-dlp to fetch metadata as a proxy for 'analysis'.
    """
    print(f"[*] Step 1: Analyzing {url}...")
    
    # If it's not a valid URL, just use the string as description
    if not url.startswith('http'):
        description = f"User provided text input: {url}"
    else:
        ydl_opts = {
            'quiet': True,
            'extract_flat': True,  # Don't download, just get metadata
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                description = f"Title: {info.get('title', 'Unknown')}\n"
                description += f"Description: {info.get('description', 'No description')[:500]}..."
                description += f"\nDuration: {info.get('duration')}s"
        except Exception as e:
            description = f"Failed to analyze URL: {e}. Treating as raw text."

    # Save to file
    with open('scripts/1video_description.txt', 'w', encoding='utf-8') as f:
        f.write(description)
    
    return description

def _generate_placeholder_image(filename, text, bg_color=(0, 0, 0), text_color=(255, 255, 255)):
    """Helper to generate an image with text using PIL"""
    width, height = 1280, 720
    img = Image.new('RGB', (width, height), color=bg_color)
    d = ImageDraw.Draw(img)
    
    # Try to load a font, fallback to default
    try:
        # Mac usually has Arial or Helvetica
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
    except:
        try:
             font = ImageFont.truetype("arial.ttf", 40)
        except:
             font = ImageFont.load_default()

    # Simple word wrap or center text
    # For simplicity, just center the first few lines
    lines = text.split('\n')
    y_text = height / 2 - (len(lines) * 25)
    for line in lines:
        # textbbox was added in Pillow 8.0.0
        bbox = d.textbbox((0, 0), line, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        d.text(((width - text_w) / 2, y_text), line, font=font, fill=text_color)
        y_text += text_h + 10

    img.save(filename)
    return filename

def step2_generate_characters(description):
    """Step 2: Generate character images and classes."""
    print("[*] Step 2: Generating characters...")
    # Mocking character extraction from description
    # In a real app, LLM would extract names. Here we pick a generic one.
    char_name = "Protagonist"
    
    # Generate Image
    img_path = f"charectorImages/charectorImage_{char_name}.jpg"
    _generate_placeholder_image(img_path, f"CHARACTER: {char_name}\n(Generated from video analysis)", bg_color=(50, 50, 150))
    
    # Generate Class File
    class_content = f"""
class {char_name}:
    def __init__(self):
        self.name = "{char_name}"
        self.image_path = "{img_path}"
"""
    with open(f"charectors/{char_name}.py", 'w') as f:
        f.write(class_content)
        
    return [char_name]

def step3_generate_backgrounds(description):
    """Step 3: Generate background images and classes."""
    print("[*] Step 3: Generating backgrounds...")
    bg_name = "MainScene"
    
    img_path = f"backgroundImages/background_{bg_name}.jpg"
    _generate_placeholder_image(img_path, f"BACKGROUND: {bg_name}\n(Cyberpunk/Tech Style)", bg_color=(20, 20, 20))
    
    class_content = f"""
class {bg_name}:
    def __init__(self):
        self.name = "{bg_name}"
        self.image_path = "{img_path}"
"""
    with open(f"backgrounds/{bg_name}.py", 'w') as f:
        f.write(class_content)
        
    return [bg_name]

def step4_generate_scripts(prompt, char_names):
    """Step 4: Generate scene scripts based on user prompt."""
    print("[*] Step 4: Generating scripts...")
    # Mock splitting prompt into 3 scenes
    scenes = [
        f"Scene 1: Intro - {prompt}",
        f"Scene 2: Conflict - {char_names[0]} takes action",
        f"Scene 3: Conclusion - The result of {prompt}"
    ]
    
    script_files = []
    for i, scene in enumerate(scenes):
        idx = i + 1
        fname = f"scripts/script_{idx}.txt"
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(scene)
        script_files.append(fname)
    
    return script_files

def step5_generate_frames(script_files):
    """Step 5: Generate start/end frames for each script."""
    print("[*] Step 5: Generating frames...")
    frames = []
    for i, script_file in enumerate(script_files):
        idx = i + 1
        with open(script_file, 'r') as f:
            content = f.read()
            
        frame_path = f"frames/frame_{idx}.jpg"
        _generate_placeholder_image(frame_path, f"FRAME {idx}\n{content}", bg_color=(random.randint(0,50), random.randint(0,50), random.randint(0,50)))
        frames.append(frame_path)
    return frames

def step6_generate_footages(frames):
    """Step 6: Generate video footages from frames."""
    print("[*] Step 6: Generating footages...")
    footages = []
    for i, frame_path in enumerate(frames):
        idx = i + 1
        footage_path = f"footages/footage_{idx}.mp4"
        
        # Create a 3-second clip from the image
        clip = ImageClip(frame_path, duration=3).with_fps(24)
        clip.write_videofile(footage_path, codec="libx264", audio=False, logger=None)
        
        footages.append(footage_path)
    return footages

def step7_merge_videos(footages, output_path="static/output.mp4"):
    """Step 7: Merge footages into final video."""
    print("[*] Step 7: Merging videos...")
    clips = [os.path.abspath(f) for f in footages]
    
    # Load clips using MoviePy
    video_clips = []
    for clip_path in clips:
        # Use a context manager logic or just load
        video_clips.append(os.path.abspath(clip_path))
        
    # To avoid 'OSError: WinError 6' style errors or file locks, we use the objects carefully
    # loaded_clips = [ImageClip(f, duration=3).with_fps(24) for f in footages] # Re-creating clips from images is safer than reloading mp4s sometimes for simple concatenation
    
    # Actually, let's load the generated MP4s to be true to the requirements "concatenate footages"
    # But for stability in this script, re-using ImageClip logic is cleaner if footages are just static images.
    # However, requirements say "splice video", so let's try VideoFileClip
    from moviepy import VideoFileClip
    
    real_clips = []
    for f in footages:
        real_clips.append(VideoFileClip(f))
        
    final_clip = concatenate_videoclips(real_clips)
    final_clip.write_videofile(output_path, codec="libx264", audio=False, logger=None)
    
    # Close clips to release file handles
    for c in real_clips:
        c.close()
    
    # Also copy to root as per project rules
    import shutil
    shutil.copy(output_path, "output.mp4")
        
    return output_path

def run_pipeline(url, prompt):
    print("=== Starting Video Generation Pipeline ===")
    
    # 1. Analyze
    desc = step1_analyze_video(url)
    
    # 2. Characters
    chars = step2_generate_characters(desc)
    
    # 3. Backgrounds
    step3_generate_backgrounds(desc)
    
    # 4. Scripts
    scripts = step4_generate_scripts(prompt, chars)
    
    # 5. Frames
    frames = step5_generate_frames(scripts)
    
    # 6. Footages
    footages = step6_generate_footages(frames)
    
    # 7. Merge
    output_video = step7_merge_videos(footages)
    
    print(f"=== Pipeline Completed. Output: {output_video} ===")
    return output_video

if __name__ == "__main__":
    # Test run
    run_pipeline("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "Test Prompt")
