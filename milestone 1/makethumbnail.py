import sys
import subprocess
cmd1=f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 video/{sys.argv[1]}'
runcmd1= subprocess.run(cmd1, shell=True, stdout=subprocess.PIPE)
time=float(runcmd1.stdout.decode('utf-8'))
if (time<=60):
    temp=time*(1/3)
    extract_convert=f'ffmpeg -i "video/{sys.argv[1]}" -vf "select=not(mod(n\,10))" -vsync vfr -q:v 2 -ss {temp} -t {temp} "frames/img_%04d.png" && convert -resize 480x360 -delay 10 -loop 0 "frames/*.png" "video/{sys.argv[2]}"'
    subprocess.run(extract_convert, shell=True)
else:
    temp=time*(2/3)
    extract_convert=f'ffmpeg -i "video/{sys.argv[1]}" -vf "select=not(mod(n\,10))" -vsync vfr -q:v 2 -ss {temp} -t 20 "frames/img_%04d.png" && convert -resize 480x360 -delay 10 -loop 0 "frames/*.png" "video/{sys.argv[2]}"'
    subprocess.run(extract_convert, shell=True)

delete=f'rm -r frames/*'
subprocess.run(delete, shell=True)