import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta

app = Flask(__name__)


# HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')


# url 나눠보기
@app.route('/mypage')
def mypage():
    return 'This is mypage Hello Flask!!!'


# 받은 rank와 일치하는 영화 출력
@app.route('/test', methods=['GET'])
def test_get():
    rank_receive = request.args.get('rank_give')
    rank_receive = int(rank_receive)
    movie_info = db.movies.find_one({'rank': rank_receive}, {'_id': 0})
    return jsonify({'result': 'success', 'msg': movie_info})


# 받은 rank의 평점을 받은 star로 업데이트 하기
@app.route('/test', methods=['POST'])
def test_post():
    # rank_give로 클라이언트가 준 rank을 가져오기 & 숫자변환
    rank_receive = request.form['rank_give']
    print('순위' + rank_receive)
    rank_receive = int(rank_receive)

    # star_give로 클라이언트가 준 star를 가져오기 & 숫자변환
    star_receive = request.form['star_give']
    print('평점' + star_receive)
    star_receive = int(star_receive)


    print(rank_receive, star_receive)

    # 해당 순위의 영화를 받은 score로 업데이트 해주기
    db.movies.update_one({'rank': rank_receive}, {'$set': {'star': star_receive}})

    # 다했으면 성공여부만 보냄
    return jsonify({'result': 'success'})

# 포스팅 저장 API
@app.route('/post', methods=['POST'])
def saving():
    url_receive = request.form['url_give']  # 클라이언트로부터 url을 받는 부분
    comment_receive = request.form['comment_give']  # 클라이언트로부터 comment를 받는 부분
    author_receive = request.form['author_give']  # 클라이언트로부터 author를 받는 부분

    # print(url_receive)
    # print(comment_receive)
    # print(author_receive)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    og_image = soup.select_one('meta[property="og:image"]')
    og_title = soup.select_one('meta[property="og:title"]')
    og_description = soup.select_one('meta[property="og:description"]')

    url_image = og_image['content']
    url_title = og_title['content']
    url_description = og_description['content']

    article = {'author': author_receive, 'url': url_receive, 'comment': comment_receive, 'image': url_image,
               'title': url_title, 'desc': url_description}

    db.articles.insert_one(article)

    return jsonify({'result': 'success'})


# 포스팅 불러오기 API
@app.route('/post', methods=['GET'])
def listing():
    # author_give 클라이언트가 준 author를 가져오기
    author_receive = request.args.get('author_give')
    # author의 값이 받은 author와 일치하는 document 찾기 & _id 값은 출력에서 제외하기
    result = list(db.articles.find({'author': author_receive}, {'_id': 0}))
    print(result)
    # articles라는 키 값으로 기사정보 내려주기
    return jsonify({'result': 'success', 'articles': result})


# 포스팅 삭제하기 API
@app.route('/delete', methods=['POST'])
def delete():
    title_receive = request.form['title_give']
    # print(title_receive)

    db.articles.delete_one({'title': title_receive})
    return jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
