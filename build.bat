pipenv run pyinstaller --onefile --clean --noconsole --distpath "../Build" --specpath "../.Building" --name "Musiques Youtube" --icon "../Sources/icon.ico" --workpath "../.Building" --add-data "../Sources/ffmpeg.exe;." --add-data "../Sources/ffprobe.exe;." Interface.py