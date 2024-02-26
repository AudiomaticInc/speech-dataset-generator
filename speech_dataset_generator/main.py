import argparse

from speech_dataset_generator.audio_processor.audio_processor import process_audio_files, get_local_audio_files, get_youtube_audio_files

def parse_range(value):
    try:
        start, end = map(int, value.split('-'))
        return start, end
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid range format. Please use 'start-end'.")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--input_file_path', type=str, help='Path to the input audio file.')
    group.add_argument('--input_folder', type=str, help='Path to the input folder containing audio files.')

    parser.add_argument("--youtube_download", nargs="*", help="YouTube playlist or video URLs")

    parser.add_argument("--output_directory", type=str, help="Output directory for audio files", default=".")
    parser.add_argument('--range_times', nargs='?', type=parse_range, default=(4, 10), help='Specify a range of two integers in the format "start-end". Default is 4-10.')
    parser.add_argument('--types', nargs='+', default=["deepfilternet"], help='List of types. Default is deepfilternet. You can combine filters too: --types deepfilternet enhance_audio_resembleai  . You can disable it with --types None')

    args = parser.parse_args()
    
    input_file_path     = args.input_file_path
    input_folder        = args.input_folder
    youtube_download    = args.youtube_download
    output_directory    = args.output_directory
    start, end          = args.range_times
    filter_types        = args.types

    if not input_file_path and not input_folder:
        raise Exception("input_file_path or input_folder is required")
    
    youtube_audio_files = get_youtube_audio_files(youtube_download, output_directory)

    if input_folder:
        local_audio_files = get_local_audio_files(input_folder)
        audio_files = local_audio_files + get_youtube_audio_files(youtube_download, output_directory)
        process_audio_files(audio_files, output_directory, start, end, filter_types)
    elif input_file_path:
        audio_files = [input_file_path] + get_youtube_audio_files(youtube_download, output_directory)
        process_audio_files(audio_files, output_directory, start, end, filter_types)
    else:
        process_audio_files(get_youtube_audio_files(youtube_download, output_directory), output_directory, start, end, filter_types)