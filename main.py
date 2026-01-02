import ffmpeg
import os
import argparse
import logging
from pathlib import Path
from datetime import datetime

log_filename = f"conversion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_filename, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def convert_audio_to_stereo(input_path, output_file):
    try:
        logging.info(f"Processing file: {os.path.basename(input_path)}")

        input_stream = ffmpeg.input(input_path)

        audio_filter = (
            input_stream.audio
            .filter('pan', 'stereo',
                    FL='1.0*FL + 0.707*FC + 0.707*BL', # needs testing 
                    FR='1.0*FR + 0.707*FC + 0.707*BR')
            .filter('loudhorm'))
 
        out = ffmpeg.output(
                           input_stream.video,
                           audio_filter,
                           output_file, 
                           vcodec='copy', 
                           acodec='aac', 
                           ac=2, 
                           map_metadata=0
                           )

        ffmpeg.run(out, overwrite_output=True, capture_stdout=True, capture_stderr=True)        
        logging.info(f"Successfully converted to stereo: {of.path.basename(output_file)}")

    except ffmpeg.Error as e:
       logging.error(f"FFmpeg error for file {os.path.basename(input_path)}: {e.stderr.decode()}")

def main():
    parser = argparse.ArgumentParser(description="batch downmix 5.1 audio to 2.0 stereo")
    parser.add_argument("input", help="input file or directory")
    parser.add_argument("-o", "--output", help="output directory (optional)", default="output_stereo")

    args = parser.parse_args()
    input_path = Path(args.input)
    output_dir = Path(args.output)

    if not output_dir.exists():
        output_dir.mkdir()
        logging.info(f"Created output directory: {output_dir}")

    if input_path.is_file():
        files_to_process = [input_path]
    elif input_path.is_dir():
        files_to_process = list(input_path.glob("*.mkv")) + list(input_path.glob("*.mp4"))
    else:
        logging.error("Input path is neither a file nor a directory.")
        return
    
    logging.info(f"Found {len(files_to_process)} files to process.")    

    for file in files_to_process:
        destination = output_dir / f"{file.stem}_stereo{file.suffix}"
        convert_audio_to_stereo(str(file), str(destination))

if __name__ == "__main__":
    main()

# python main.py film_name
# python main.py ./folder/