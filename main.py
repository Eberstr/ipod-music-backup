import os
import re
import shutil
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4

# Constants
PATH = r"C:\Users\Eber\Desktop\ipod-music-backup\Music"
DEST_PATH = r"C:\Users\Eber\Desktop\Respaldo_iPod"

def copy_files(src, dest):
    if os.path.exists(src):
        try:
            shutil.copy2(src, dest)
        except FileNotFoundError as e:
                print(f"[!] File Not Found: {e.filename}")
        except PermissionError:
            print("[!] No permission to copy the file")
        except OSError as e:
            print(f"[!] Error del sistema: {e}")

def clean_tag(value, default="Unkown"):
    try:
        return re.sub(r'[\\/:*?";<>.|]', '', str(value))
    except:
        return default

def get_mp3_tag(track, key, default="Unkown"):
    tag = track.tags.get(key)
    if tag and tag.text:
        return clean_tag(tag.text[0], default)
    return default

def folder_structure(src_file, track="Unknown", artist="Unkown", album="Unkown"):
    #TODO: Agregar indice para canciones unknown para el mismo artista ej. Unkown_01, Unknown_02,...

    artist_dir = os.path.join(DEST_PATH, artist)
    os.makedirs(artist_dir, exist_ok=True)

    album_dir = os.path.join(artist_dir, album)
    ext = os.path.splitext(src_file)[1]
    os.makedirs(album_dir, exist_ok=True)
        
    dest_path = os.path.join(album_dir, track + ext)
    
    copy_files(src_file, dest_path)


def main():
    for root, dirs, files in os.walk(PATH):
        for file in files:
            src_file = os.path.join(root, file)
            print(src_file)

            if file.endswith('.mp3'):     
                track = MP3(src_file)

                track_title = get_mp3_tag(track, "TIT2")
                artist_name = get_mp3_tag(track, "TPE1")
                album_title = get_mp3_tag(track, "TALB")
                
                folder_structure(src_file, track_title, artist_name, album_title)                 

            elif file.endswith(('.mp4', '.m4a')):
                track = MP4(src_file)

                track_title = re.sub(r'[\\/:*?";<>.|]', '', str(track.tags["\xa9nam"][0]))
                try:
                    artist_name = re.sub(r'[\\/:*?";<>.|]', '', str(track.tags["\xa9ART"][0]))
                except KeyError:
                    print("[!] Nombre del Artista no encontrado en metadata")
                    artist_name = "Unkown"          

                try:
                    album_title = re.sub(r'[\\/:*?";<>.|]', '', str(track.tags["\xa9alb"][0]))
                except KeyError:
                    print("[!] Album no encontrado en metadata")
                    album_title = "Unkown"
                
                folder_structure(src_file, track_title, artist_name, album_title)

            print(f'Cancion {src_file} copiada en')

main()