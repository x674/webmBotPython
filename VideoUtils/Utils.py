from subprocess import check_output
import json
import ffmpeg
from pathlib import Path

def has_audio_streams(file_path):
  command = ['ffprobe', '-show_streams',
           '-print_format', 'json', file_path, '-v', 'error']
  output = check_output(command)
  parsed = json.loads(output)
  streams = parsed['streams']
  audio_streams = list(filter((lambda x: x['codec_type'] == 'audio'), streams))
  return len(audio_streams) > 0

def generate_thumbnail(in_filename):
    p = Path(in_filename)
    out_filename = str(p.with_suffix('.png'))
    probe = ffmpeg.probe(in_filename)
    videostream = next((x for x in probe['streams'] if 'width' in x), None)
    time = float(videostream['duration']) // 2
    width = videostream['width']
    try:
        (
            ffmpeg
            .input(in_filename, ss=time)
            .filter('scale', width, -1)
            .output(out_filename, vframes=1)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        return str(Path(out_filename))
    except ffmpeg.Error as e:
        print(e.stderr.decode(), file=sys.stderr)
        sys.exit(1)
