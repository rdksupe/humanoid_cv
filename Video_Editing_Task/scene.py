import cv2
from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import AdaptiveDetector
from moviepy.editor import concatenate_videoclips, VideoFileClip
import numpy as np

def detect_scenes(video_path, threshold=30.0, min_scene_length=5):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    scene_list = []
    last_frame = None
    start_time = 0
    scene_start_time = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
        
        if last_frame is not None:
            diff = cv2.absdiff(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), last_frame)
            non_zero_count = np.count_nonzero(diff)
            
            if non_zero_count > threshold * frame.size / 100:
                if (current_time - scene_start_time) >= min_scene_length:
                    scene_list.append((scene_start_time, current_time))
                    scene_start_time = current_time
        
        last_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    cap.release()
    return scene_list

def create_highlight_reel(video_path, output_path, scene_list, highlight_duration=5, padding=1, crossfade_duration=1, max_length=60):
    video_clips = []
    video_clip = VideoFileClip(video_path)
    total_duration = 0

    for scene in scene_list:
        start, end = scene
        duration = end - start
        if duration >= highlight_duration:
            clip_duration = highlight_duration + padding
            if total_duration + clip_duration > max_length:
                break
            clip = video_clip.subclip(start, (start + highlight_duration))
            clip = clip.set_duration(clip.duration + padding)  # Add padding
            video_clips.append(clip)
            total_duration += clip_duration

    
    final_clip = concatenate_videoclips(video_clips, method="compose", padding=-crossfade_duration)
    
   
    final_clip = final_clip.resize(newsize=(720, 1280))
    
   
    final_clip.write_videofile(output_path, codec='libx264', fps=30)





video_path = 'C:/Users/rishi/humanoid/robot.mp4'
output_path = 'C:/Users/rishi/humanoid/edited89.mp4'
scene_list = detect_scenes(video_path)
print(scene_list)
create_highlight_reel(video_path, output_path, scene_list)
