from pytube import YouTube
from flask import Flask, url_for, request, redirect, render_template, flash, send_file, Response
import time
import sys, os

file_size = 0
file_title = ""
download_path = 'Users/wegosh/Desktop/ytMovies/'
download_title = 'YTDownload'
download_ext = '.mp4'
progresVariable = 0
videoDetails = []

def getMovie(movieUrl):
    ytMovie = YouTube(movieUrl, on_progress_callback=testProgress)
    ytMovie.prefetch()
    stream = ytMovie.streams.first()
    global file_size
    file_size=stream.filesize
    stream.download('/Users/wegosh/Desktop/ytMovies')
    #print(ytMovie.streams)
    #stream.download()
    


app = Flask(__name__, static_url_path='/static', static_folder='static')


# @app.route('/', methods=['GET', 'POST'])
# def hello_world():
#     if request.method == 'POST':
#         ytUrl = request.form['ytDownloadUrl']
#         getMovie(ytUrl)
#         return redirect(url_for('progress'))
#     return render_template('main.html')

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        ytUrl = request.form['ytDownloadUrl']
        ytMovie = YouTube(ytUrl, on_progress_callback=testProgress)
        ytMovie.prefetch()
        stream = ytMovie.streams.first()
        videoDetails.append("siusiak")
        global file_size
        file_size = stream.filesize
        global file_title
        file_title=ytMovie.title
        stream.download('/Users/wegosh/Desktop/ytMovies', "YTDownload", skip_existing=False)
        return render_template('main.html', videoDetails = videoDetails)

    return render_template('main.html')


def testProgress() -> None:
    if os.path.exists(download_path + download_title + download_ext) != True:
        pass
    curSize = os.path.getsize('/Users/wegosh/Desktop/ytMovies/YTDownload.mp4')
    sys.stdout.write("current size: " + str(curSize) + "\nTotal size: " + str(file_size))
    sys.stdout.flush()
    global progresVariable
    progresVariable = percent(curSize, file_size)
    return percent(curSize, file_size)

def testProgress(stream, chunks, filesize) -> None:
    if os.path.exists(download_path + download_title + download_ext) != True:
        pass
    curSize = os.path.getsize('/Users/wegosh/Desktop/ytMovies/YTDownload.mp4')
    sys.stdout.write("current size: " + str(curSize) + "\nTotal size: " + str(file_size))
    sys.stdout.flush()
    global progresVariable
    progresVariable = percent(curSize, file_size)
    return percent(curSize, file_size)




@app.route('/progress')
def progress():
    def generate():
        x = 0
        while x <= 100:
            yield "data:" + str(x) + "\n\n"
            x = progresVariable
            time.sleep(0.5)
            
            
    return Response(generate(), mimetype= 'text/event-stream')



def percent(tem, total):
    if tem < 1:
        return 0
    perc = round((float(tem) / float(total)) * float(100))
    print(perc)
    return perc

# @app.route('/download/<ytUrl>', methods=['POST', 'GET'])
# def VideoDownload(ytUrl):
#     getMovie(ytUrl)
#     return render_template('main.html')
