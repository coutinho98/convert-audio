import ffmpeg
import os

def converter_audio_to_stereo(input_file, output_file):
    try:
        if not os.path.exists(input_file):
            print("Erro: Arquivo de entrada não encontrado.")
            return

        print(f"Iniciando conversão de: {input_file}...")

        stream = ffmpeg.input(input_file)
    
        out = ffmpeg.output(stream, output_file, 
                           vcodec='copy', 
                           acodec='aac', 
                           ac=2, 
                           map_metadata=0)

        ffmpeg.run(out, overwrite_output=True)
        
        print(f"Sucesso! Arquivo salvo como: {output_file}")

    except ffmpeg.Error as e:
        print(f"Ocorreu um erro no FFmpeg: {e.stderr.decode()}")

arquivo_original = "Stranger.Things.S05E07.WEB-DL.1080p.x264.DUAL.5.1-SF.mkv"
arquivo_novo = "ep9.mkv"

converter_51_para_20(arquivo_original, arquivo_novo)
