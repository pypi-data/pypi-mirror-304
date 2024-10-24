import boto3
import cv2
import json
import ffmpeg
import numpy as np
from skcr_utils.s3 import AugmentedS3Path
from skcr_utils.utils import AWSRegionEnum

from skcvideo.controlled_fps_video_capture import ControlledFPSVideoCapture

FRAME = 100
# MATCH_NAME = "20191102_Sheffield_Burnley"
# DECODING_IDX = 325

# MATCH_ID = 9932
# MATCH_NAME = "20201018_Leicester_Aston Villa"
# DECODING_IDX = 3

MATCH_ID = 651546
MATCH_NAME = "20230227_Seattle_Colorado Rapids"
DECODING_IDX = 86

MATCH_ID = 611285
MATCH_NAME = "20020630_Germany_Brazil"
DECODING_IDX = 125

# MATCH_ID = 1097600
# MATCH_NAME = "20100711_Netherland_Spain"
# DECODING_IDX = 119

# MATCH_ID = 924939
# MATCH_NAME = "20230626_El Salvador_Martinique"
# DECODING_IDX = 110


# CONFIGURATION
bucket = "skcr-algo-dev"  # or 'skcr-algo' depending where your video file and the csvs are located
key = f"prod/{MATCH_NAME}/{MATCH_NAME}.mp4"
frames_key = f"prod/{MATCH_NAME}/frames.csv"
decoding_frame_key = f"prod/{MATCH_NAME}/decoding_frames_{DECODING_IDX}.csv"
detections_key = f"prod/{MATCH_NAME}/detections.pkl"

s3 = boto3.client("s3", region_name=AWSRegionEnum.us_east_1, config=boto3.session.Config(signature_version="s3v4"))
url = s3.generate_presigned_url(
    "get_object",
    ExpiresIn=3600,
    Params={
        "Bucket": "skcr-algo",
        "Key": key,
    },
)
print(url)

# print(json.dumps(ffmpeg.probe(url), indent=2))

# LOAD FRAME FILE FROM S3
# (files must have already been generated using Vidic), you can also use local files instead if you want/have them
df_all_frames = AugmentedS3Path(bucket, frames_key, region=AWSRegionEnum.us_east_1).read()
df_frames_selected = AugmentedS3Path(bucket, decoding_frame_key, region=AWSRegionEnum.us_east_1).read()
frame_infos = df_all_frames["FILE_INFOS_4"].values
frame_selected = df_frames_selected["FILE_INFOS_2"].values

# print(len(frame_infos), len(frame_selected))#
# print([(idx, pts, frame_selected[idx]) for idx, pts in enumerate(frame_infos) if idx > 168020 and idx < 168030])
# exit(0)

detections = AugmentedS3Path(bucket, detections_key, region=AWSRegionEnum.us_east_1).read()


# CREATE THE VIDEO READER
video_reader = ControlledFPSVideoCapture(
    url,
    frame_infos=list(frame_infos),
    frame_selection=frame_selected,
    frame_selection_version="ffmphisdp",
)
n_frames = video_reader.get(cv2.CAP_PROP_FRAME_COUNT)

# video_reader.set(cv2.CAP_PROP_POS_FRAMES, 83630)
# for i in range(10):
#     ret, frame = video_reader.read()
#     if not ret:
#         break
#     print(video_reader.current_frame_index, video_reader.current_frame.pts)
#     cv2.imwrite(f"frame_{video_reader.current_frame_index}_{video_reader.current_frame.pts}.png", frame)
    
# exit(0)

generated = 0
seek_random = False
# video_reader.set_frame_idx(83690)
seek_random = True
while generated < 10:
    # SEEK A SPECIFIC INDEX
    # as requested by tim, the index is local NOT global here, this will be converted automatically internally
    if seek_random:
        frame_index_seek = np.random.randint(0, n_frames)
        video_reader.set(cv2.CAP_PROP_POS_FRAMES, frame_index_seek)

    # GET A FRAME
    # bgr format just like before
    ret, frame = video_reader.read()
    frame_index = video_reader.get(cv2.CAP_PROP_POS_FRAMES)
    print(frame_index)
    pts = video_reader.current_frame.pts
    if seek_random:
        print("frame_index", frame_index, "frame_index_seek", frame_index_seek)
    if len(detections[frame_index]["individuals"]) == 0:
        continue

    print("frame:", type(frame), frame.dtype, frame.shape)
    image = cv2.resize(frame, [1280, 720])

    for object_type, coordinates in detections[frame_index].items():
        for x1, y1, x2, y2, score in coordinates:
            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
            # print(x1, y1, x2, y2)
            cv2.rectangle(image, (x1, y1), (x2, y2), color=(255, 255, 255), thickness=1)

    filename = f"{frame_index}_pts_{pts}.png"
    if seek_random:
        filename = f"{frame_index}_{frame_index_seek}_pts_{pts}.png"
    cv2.imwrite(filename, image)
    generated += 1
