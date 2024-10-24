from skcvideo.controlled_fps_video_capture import ControlledFPSVideoCapture as SKCControlledFPSVideoCapture
from ffmphisdp.video_reader import ControlledFPSVideoCapture as FFMVideoReader
from ffmphisdp.pyav_reader import ControlledVideoReader as PyAVReader
import boto3
from skcr_utils.s3 import AugmentedS3Path
from skcr_utils.utils import AWSRegionEnum
import cv2

MATCH_NAME = "20191102_Sheffield_Burnley"

bucket = "skcr-algo"
key = f"prod/{MATCH_NAME}/{MATCH_NAME}.mp4"

s3 = boto3.client("s3", region_name=AWSRegionEnum.us_east_1, config=boto3.session.Config(signature_version="s3v4"))
url = s3.generate_presigned_url(
    "get_object",
    ExpiresIn=3600,
    Params={
        "Bucket": bucket,
        "Key": key,
    },
)


skc_reader = SKCControlledFPSVideoCapture(url, fps="same")
ffm_reader = FFMVideoReader(url, fps="same")
frame_count = 178740
pyav_reader = PyAVReader(url, frame_infos=[i for i in range(frame_count)], frame_selection=[True for _ in range(frame_count)])

for i in range(99):
    skc_reader.read()
    ffm_reader.read()
    pyav_reader.read()

for i in range(16):
    ffm_reader.read()

_, skc_frame = skc_reader.read()
_, ffm_frame = ffm_reader.read()
_, pyav_frame = pyav_reader.read()

skc_ffm_diff = cv2.absdiff(skc_frame, ffm_frame) * 100
cv2.imwrite("skc_ffm_diff.png", skc_ffm_diff)

skc_pyav_diff = cv2.absdiff(skc_frame, pyav_frame) * 100
cv2.imwrite("skc_pyav_diff.png", skc_pyav_diff)

ffm_pyav_diff = cv2.absdiff(ffm_frame, pyav_frame) * 100
cv2.imwrite("ffm_pyav_diff.png", ffm_pyav_diff)
