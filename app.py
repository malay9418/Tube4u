from flask import Flask, render_template, request, send_file

app = Flask(__name__)

#icon
@app.route("/favicon.ico")
def icon():
	return send_file("static/img/favicon.ico")
#functions
def makeName(name):
	fileName = "Tube4U-"
	for x in name:
		if x.isalnum():
			fileName += x
		else:
			fileName += " "
	fileName += "(2022)"
	return fileName	

#file size calculator
def getSize(size_bytes):
   import math
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

#file downloader
def folder():
	import os
	i = 0
	while True:
		if os.path.exists(f"work{i}"):
			i += 1
			continue
		else:
			break
	os.mkdir(f"work{i}")
	return f"work{i}"			
		
#home
@app.route("/", methods=["GET", "POST"])
def home():
	from pytube import YouTube
	if request.method == "GET":
		return render_template("index.html")
	if request.method == "POST":
		data = {}
		url = request.form["url"]
		try:
			yt = YouTube(url)
			videoes = yt.streams
			data["url"] = url
			data["video"] = [{"type": "mp4", "res": item.resolution, "itag": item.itag, "size": getSize(item.filesize)} for item in videoes.filter(type="video", progressive=True)]
			data["audio"] = [{"type": "mp3", "res": item.abr, "itag": item.itag, "size": getSize(item.filesize)} for item in videoes.filter(type="audio")]
			data["title"] = yt.title
			data["name"] = makeName(yt.title)
			data["img"] = yt.thumbnail_url
			return render_template("final.html", data=data)
		except Exception as e:
			return f"{e}"	
		
#about
@app.route("/about/")
def about():
	return "there's nothing yet"

#contact
@app.route("/contact/")
def contact():
	return "there's nothing yet"

#download
@app.route("/media/")
def media():
		from pytube import YouTube
		import os
		url = request.args["url"]
		itag = request.args["itag"]
		fileName = request.args["fileName"]
		ext = request.args["ext"]
		yt = YouTube(url)
		directory = f"{folder()}"
		video = yt.streams.get_by_itag(itag)
		video.download(output_path=directory, filename=f"{fileName}.{ext}")
		resp = send_file(f"{directory}/{fileName}.{ext}", as_attachment=True)
		os.remove(f"{directory}/{fileName}.{ext}")
		os.rmdir(f"{directory}")
		return resp
		
#run	
if __name__ == "__main__":
	from waitress import serve
	serve(app, host="0.0.0.0", port="8080")
