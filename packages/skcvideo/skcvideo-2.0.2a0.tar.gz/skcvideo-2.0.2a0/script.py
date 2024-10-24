from skcvideo.controlled_fps_video_capture import ControlledFPSVideoCapture

cap = ControlledFPSVideoCapture(
    "/home/jhuguet/Downloads/20210127_Manchester U_Sheffield.mp4", fps=10, frame_selection_version="ffmphisdp"
)

idx = 0
while True:
    idx += 1
    ret, image_original_bgr = cap.read()
    if ret is False:
        exit(0)
    print(idx)
