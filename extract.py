import os

video_folder = r"D:\Audio feature extraction\videos\test\\"

print("Folder exists:", os.path.exists(video_folder))
print("Files inside:", os.listdir(video_folder))

import opensmile
import pandas as pd
import os
import glob

# 🔷 ✅ SET YOUR CORRECT PATH (test folder)
video_folder = r"D:\Audio feature extraction\videos\test\\"

# 🔷 Debug check
print("Folder exists:", os.path.exists(video_folder))
if os.path.exists(video_folder):
    print("Files inside:", os.listdir(video_folder))

# 🔷 Find all video files (robust: handles multiple formats)
video_files = []
for ext in ["*.mp4", "*.MP4", "*.avi", "*.mkv"]:
    video_files.extend(glob.glob(video_folder + "**/" + ext, recursive=True))

print("🔍 Found videos:", len(video_files))

if len(video_files) == 0:
    print("❌ No videos found. Check your folder path or file extensions.")
    exit()

# 🔷 Initialize openSMILE
smile = opensmile.Smile(
    feature_set=opensmile.FeatureSet.ComParE_2016,
    feature_level=opensmile.FeatureLevel.Functionals,
)

all_features = []

# 🔷 Process videos
for video_path in video_files:
    print("🎬 Processing:", video_path)
    
    audio_path = video_path.rsplit(".", 1)[0] + ".wav"
    
    # Convert video → audio
    cmd = f'ffmpeg -loglevel error -i "{video_path}" -ac 1 -ar 16000 "{audio_path}"'
    os.system(cmd)
    
    # Check if audio created
    if not os.path.exists(audio_path):
        print("⚠️ Audio extraction failed:", video_path)
        continue
    
    try:
        # Extract features
        features = smile.process_file(audio_path)
        features["file"] = os.path.basename(video_path)
        
        all_features.append(features)
    
    except Exception as e:
        print("⚠️ Feature extraction failed:", video_path)
        print("Error:", e)
    
    # Delete audio file
    os.remove(audio_path)

# 🔷 Save results
if len(all_features) == 0:
    print("❌ No features extracted.")
else:
    df = pd.concat(all_features)
    df.to_csv("features.csv", index=False)
    print("✅ Feature extraction complete!")
    print("📁 Saved as features.csv")