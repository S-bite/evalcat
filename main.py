# coding:utf-8
from flask import Flask, render_template, redirect, request
import pickle
import random

app = Flask(__name__)


@app.route("/")
def root():
    return redirect("/ranking")


@app.route("/picklerating")
def picklerating():
    with open("rating.pkl", "wb") as f:
        pickle.dump(rating, f)
    return "OK"


@app.route("/cat")
def cat():
    id = request.args.get('id')
    return render_template('cat.html', id=id, rate=rating[id], latents=cats[id])


@app.route("/result")
def result():
    win = request.args.get('win')
    lose = request.args.get('lose')
    rate_win = rating[win]
    rate_lose = rating[lose]
    odds = 1/(1+10**((rate_lose-rate_win)/400))

    # レートの更新
    K = 100
    rate_win = rate_win+K*(1-odds)
    rate_lose = rate_lose+K*(0-odds)
    print("win", win)
    print("lose", lose)
    print("win : {} -> {}".format(rating[win], rate_win))
    print("lose : {} -> {}".format(rating[lose], rate_lose))
    rating[win] = rate_win
    rating[lose] = rate_lose

    return redirect("/compare")


@app.route("/index")
def index():
    return render_template('ranking.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/ranking")
def ranking():
    catinfo = []
    for id, rate in rating.items():
        catinfo.append({"id": id, "rate": int(rate)})
    catinfo.sort(key=lambda x: x["rate"], reverse=True)
    return render_template('ranking.html', catinfo=catinfo)


@app.route("/compare")
def compare():
    img1 = ""
    img2 = ""
    while (img1 == img2):
        img1, _ = random.choice(list(cats.items()))
        img2, _ = random.choice(list(cats.items()))

    return render_template('compare.html', img1=img1, img2=img2)


with open('latentsdict.pkl', 'rb') as f:
    cats = pickle.load(f)

with open("rating.pkl", "rb") as f:
    rating = pickle.load(f)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, threaded=True)
