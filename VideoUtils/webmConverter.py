import os
import ffmpeg
import requests

#TODO auto select video codec ex. NVENC


"""Return path to converted file"""
def convert_webm_to_mp4(input_path : str):
    if "http" in input_path:
        #if url then download file
        input_path = download_file(input_path)
    name_out_file = os.path.basename(input_path)
    name_out_file = name_out_file.replace("webm", "mp4")
    stream = ffmpeg.input(input_path)
    stream = ffmpeg.filter(stream, "scale", "trunc(iw/2)*2:trunc(ih/2)*2")
    stream = ffmpeg.output(stream, name_out_file)
    print(ffmpeg.compile(stream))
    ffmpeg.run(stream)
    path_to_file = os.path.realpath(name_out_file)
    return path_to_file


def download_file(url : str):
    r = requests.get(url)
    filename = os.path.basename(url)
    file = open(filename, "wb")
    file.write(r.content)
    path_to_file = os.path.realpath(file.name)
    return path_to_file


"""Test"""
if __name__ == "__main__":
    url_video = "https://file-examples-com.github.io/uploads/2020/03/file_example_WEBM_1920_3_7MB.webm"
    #download
    r = requests.get(url_video)
    file = open("test.webm","wb")
    file.write(r.content)
    full_path = os.path.realpath(file.name)
    convert_webm_to_mp4(full_path)
