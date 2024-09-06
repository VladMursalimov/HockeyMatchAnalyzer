import argparse
import annotation
import frames_to_video
from annotation_field import annotation_field
import mergeLabels
import mergeFrames
import detectTactics

def main():
    # Парсер аргументов командной строки
    parser = argparse.ArgumentParser(description='Process video and annotations.')
    parser.add_argument('--modelPathPlayers', type=str, required=True, help='Path to the YOLO model .pt')
    parser.add_argument('--modelPathField', type=str, required=True, help='Path to the YOLO model .pt')

    parser.add_argument('--videoPath', type=str, required=True, help='Path to the video file .mp4')
    #parser.add_argument('--type', type=int, required=True, help='type 0 for players, type 1 is fields')

    # Чтение аргументов
    args = parser.parse_args()
    #type = args.type
    modelPathPlayers = args.modelPathPlayers
    modelPathField = args.modelPathField
    videoPath = args.videoPath

    output_dir = annotation_field(modelPathPlayers, videoPath, '0')
    output_dir_field = annotation_field(modelPathField, videoPath, '1')

    labels_dir_players = "labels_" + videoPath.replace('.mp4', '') + '_players'
    labels_dir_field = "labels_" + videoPath.replace('.mp4', '') + '_field'
    output_merged_labels = 'merged_labels_' + videoPath.replace('.mp4', '')
    mergeLabels.merge_txt_files(labels_dir_players, labels_dir_field, output_merged_labels)

    mergeFrames.draw_bounding_boxes(output_merged_labels, output_dir, output_dir + "merged")

    tactics_folder = videoPath.replace('.mp4', '') + '_tactics'
    detectTactics.determine_tactics_and_draw(output_merged_labels, output_dir + "merged", tactics_folder, 30)

    frames_to_video.frames_to_video(tactics_folder, videoPath)


if __name__ == "__main__":
    main()
