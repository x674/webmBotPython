import os
import ffmpeg
import requests

#TODO auto select video codec ex. NVENC


"""Return path to converted file"""
def convert_webm_to_mp4(input_path : str):
    if "http" in input_path:
        #if url then download file
        r = requests.get(input_path)
        filename = os.path.basename(input_path)
        file = open(filename,"wb")
        file.write(r.content)
        input_path = os.path.realpath(file.name)
    outname = os.path.basename(input_path)
    outname = outname.replace("webm","mp4")
    stream = ffmpeg.input(input_path)
    stream = ffmpeg.output(stream, outname)
    ffmpeg.run(stream)


"""Test"""
if __name__ == "__main__":
    url_video = "https://file-examples-com.github.io/uploads/2020/03/file_example_WEBM_1920_3_7MB.webm"
    #download
    r = requests.get(url_video)
    file = open("test.webm","wb")
    file.write(r.content)
    full_path = os.path.realpath(file.name)
    convert_webm_to_mp4(full_path)
