import ffmpeg
import os
import argparse
from pathlib import Path

def convert_audio_to_stereo(input_path, output_file):
    try:
        print(f"Iniciando conversão de: {input_path}...")

        input_stream = ffmpeg.input(input_path)

        out = ffmpeg.output(
                           input_stream,
                           output_file, 
                           vcodec='copy', 
                           acodec='aac', 
                           ac=2, 
                           map_metadata=0)

        ffmpeg.run(out, overwrite_output=True, capture_stdout=True, capture_stderr=True)        
        print(f"Sucesso! Arquivo salvo como: {output_file}")

    except ffmpeg.Error as e:
        print(f"Ocorreu um erro no FFmpeg: {e.stderr.decode()}")
    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Batch Downmix 5.1 Audio to 2.0 Stereo")
    parser.add_argument("input", help="Input file or directory")
    parser.add_argument("-o", "--output", help="Output directory (optional)", default="output_stereo")

    args = parser.parse_args()
    input_path = Path(args.input)
    output_dir = Path(args.output)

    if not output_dir.exists():
        output_dir.mkdir()

    if input_path.is_file():
        files_to_process = [input_path]
    elif input_path.is_dir():
        files_to_process = list(input_path.glob("*.mkv")) + list(input_path.glob("*.mp4"))
    else:
        print("Error: Input path not found.")
        return

    for file in files_to_process:
        destination = output_dir / f"{file.stem}_stereo{file.suffix}"
        convert_audio_to_stereo(str(file), str(destination))

if __name__ == "__main__":
    main()

