
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, Response, request

import sys
import requests
#import gdown
app = Flask(__name__)
# Replace with your actual Google Drive file ID
GOOGLE_DRIVE_FILE_ID = "1fqSeQJTyCtAQ5kiaxoEf4p3ghXHDAiWd"
GOOGLE_DRIVE_URL = f"https://drive.google.com/uc?export=download&id=1fqSeQJTyCtAQ5kiaxoEf4p3ghXHDAiWd"
#try:
introVideo = "videos/cammy arcade wasn't me.MP4"
print("introVideo worked")
#except:
    #introVideo = None




VIDEOS = {
   "eW2_9F3zCiA": "slopes" ,
    "1rc5WnThFTc": "Virtual vs Reality, Soccer fails",
    "hsQ6eFETIgw":"Wasn't me",
    "__nZvCn6hvk": "Myles Smith",
    "NDR1LjgezcE?si=J67QtXbTuwFANTzk":"We are girls together",
    "QQh4G-1eOZE": "Perception Project",
    "RF1DaGNalPg":"Day with Arina",
    "d0cViyNfQeI":"Cabaret",
    "Sx_jMElcNuo":"CERAMICS",
    "RzyQohEYFFQ":"Fire Drill Musings"
}

VIDEO_TITLES = {
    "slopes": "eW2_9F3zCiA",
    "intro": "iRpL07Gxc14",
    "Perception Project":"QQh4G-1eOZE",
    "Myles Smith": "__nZvCn6hvk",
    "wasn't me": "hsQ6eFETIgw",
    "frisbee b&w":"grwdj7Kd6ao",
    "teacher gossip":"7DtGSQ8vIvo",
    "TTRPG Knighting":"AhStJ8VgcI4",
    "We are girls together":"NDR1LjgezcE",
    "Strange Brew Promo":"V_QHj2jM07A",
    "Day with Arina":"RF1DaGNalPg",
    "Jonas":"T0zg9JKHiFI",
    "Casey":"7Dlk-Rh0XU8",
    "Strange Brew, Way Down South":"vaq7Cn_hfD4"
}


# Define video groups for segmentation
VIDEO_GROUPS = {
    "Jacobson's": {
        "title": "School Jacobson's",
        "description": "a",
        "content": ["Jonas","Casey"]
    },
    "Strange Brew Crew": {
        "title": "Strange Brew Crew",
        "description": "Strange Brew Crew band",
        "content":["Strange Brew Promo","Strange Brew, Way Down South"]
    },
    "Blue and White Day": {
        "title": "Group 1 Videos",
        "description": "First set of test videos",
        "content": ["frisbee b&w","teacher gossip", "TTRPG Knighting"]
    },
}

def get_video_url(video_id):
    return f"https://drive.google.com/uc?export=download&id={video_id}"

def download_video():
    response = requests.get(GOOGLE_DRIVE_URL, stream=True)
    if response.status_code == 200:
        print("video should have worked?")
        return response.content
    return None

def download_video_main(video_id):
    response = requests.get(get_video_url(video_id), stream=True)
    if response.status_code == 200:
        print(GOOGLE_DRIVE_URL == get_video_url(video_id))
        print("video should have worked?")
        return response.content
    return None

@app.route('/video')
def stream_video():
    video_content = download_video()
    if video_content:
        print(f"Video size: {len(video_content)} bytes")
        return Response(video_content, mimetype="video/mp4")
    print(f"Video size: {len(video_content)} bytes")
    print(f"Video size: {len(video_content)} bytes")
    print(f"Video size: {len(video_content)} bytes")
    return "Failed to load video", 404

@app.route('/video_player')
def video_page():
    return render_template("video.html")

@app.route('/video_player/<video_id>')
def video_player(video_id):
    print(str(VIDEO_TITLES.values()) + str("     ") + video_id)
    if video_id in VIDEOS:
        return render_template("video.html", video_id=video_id, title=VIDEOS[video_id])
    elif video_id in VIDEO_TITLES.values():
        title = next(key for key, value in VIDEO_TITLES.items() if value == video_id)
        return render_template("video.html", video_id=video_id, title=title)
    else:
        return render_template("video.html", video_id=video_id, title="Title not found")
    #return "Video Not Found", 404

@app.route('/videos/<video_id>')
def stream_videos(video_id):
    video_content = None #download_video_main(video_id)
    if video_content:
        print("video should have worked?")
        print(f"Video size: {len(video_content)} bytes")
        return Response(video_content, mimetype="video/mp4")
    return "Failed to load video", 404

"""@app.route('/videos/<video_id>')
def stream_videos(video_id):

     Stream video with support for byte-range requests
    try:
        if video_id not in VIDEOS:
            return "Video Not Found", 404

        headers = {'Range': request.headers.get('Range')} if request.headers.get('Range') else {}
        headers["Content-Disposition"] = "inline"
        response = requests.get(get_video_url(video_id), stream=True, headers=headers)
        print(response.headers)
        if response.status_code in [200, 206]:  # 206 means partial content
            try:
                return Response(response.iter_content(chunk_size=512), status=response.status_code, headers=dict(response.headers), content_type="video/mp4")
            except BrokenPipeError:
                print("same client disconnected error in stream")
            except OSError as e:
                print(f"OSWrite error: {e}")
        return "Failed to load video", 404
    except OSError as e:
        print(f"Write error occurred: [e]")
        return "Stream interrupted idk try again", 500"""


"""@app.route('/group/<group_id>')
def group_page(group_id):
    Render a page for a specific group of videos
    if group_id in VIDEO_GROUPS:
        group_info = VIDEO_GROUPS[group_id]
        group_videos = {vid_id: VIDEOS[vid_id] for vid_id in group_info["videos"] if vid_id in VIDEOS}
        return render_template("group.html", title=group_info["title"], description=group_info["description"], videos=group_videos)
    return "Group Not Found", 404"""

def resolve_video_title(video_id):
    return VIDEO_TITLES.get(video_id, video_id)  # Default to ID if not found

@app.route('/group/<path:group_path>')
def group_page(group_path):
    levels = group_path.split("/")
    current_group = VIDEO_GROUPS

    # Traverse nested groups properly
    group_info = None  # Track the current group metadata
    for level in levels:
        if isinstance(current_group, dict) and level in current_group:
            group_info = current_group[level]  # Update metadata reference
            current_group = group_info["content"]
        else:
            return "Group Not Found", 404

    # Prepare template variables
    description = group_info.get("description", "") if group_info else ""

    # Check if the current group holds videos or further sub-groups
    if isinstance(current_group, list):
        video_dict = {vid: VIDEO_TITLES.get(vid, vid) for vid in current_group}  # Map IDs to titles
        return render_template("group.html", videos=video_dict, title=group_info["title"], description=description, titles = current_group)

    return render_template("group.html", subgroups=current_group, title=group_info["title"], description=description)



@app.route('/about')
def about_page():
    return render_template("about.html")

@app.route('/')
def hello_world():
    return render_template("landing.html")

    #return 'Hello from Flask!'

@app.route('/index')
def index():
    return render_template("index.html", videos=VIDEOS, groups = VIDEO_GROUPS)

if __name__ == "__main":
    app.run(debug=True)