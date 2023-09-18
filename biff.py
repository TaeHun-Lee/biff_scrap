from bs4 import BeautifulSoup
import requests

class Movie:
    def __init__(self, code, time, title_kor, title_eng):
      self.code = code
      self.time = time
      self.title_kor = title_kor
      self.title_eng = title_eng
    def __repr__(self):
      return repr((self.code, self.time, self.title_kor, self.title_eng))

## 수입작 표시
imported_list = [
  '괴물',
  '녹야',
  '가여운 것들',
  '공드리의 솔루션북',
  '나의 올드 오크',
  '더 킬러',
  '바튼 아카데미',
  '악은 존재하지 않는다',
  '추락의 해부',
  '키메라',
  '파리 아다망에서 만난 사람들',
  '폴른 리브스',
  '프렌치 수프',
  '라스트 썸머',
  '마거리트의 정리',
  '클럽 제로',
  '티처스 라운지',
  '립세의 사계',
  '하우 투 해브 섹스',
  '도그맨',
  '애니멀 킹덤',
  '패스트 라이브즈',
]

## 사이트 내에서 찾은 추천작 표시
muggle_recomm = [
  '괴물',
  '가여운 것들',
  '더 킬러',
  '바튼 아카데미',
  '추락의 해부',
  '키리에의 노래',
  '더 골드만 케이스',
  '레드 룸스',
  '본인 출연, 제리',
  '약속의 땅',
  '티처스 라운지',
  '하우 투 해브 섹스',
  '애니멀 킹덤',
  '패스트 라이브즈'
]


f = open('biff_md.md', 'w', -1, "UTF-8")

for day in range(6, 10):
  title_day = '# 10월 ' + str(day) + '일 상영시간표\n\n'
  f.write(title_day)
  URL = "https://www.biff.kr/kor/html/schedule/date.asp?day1=" + str(day)
  page = requests.get(URL)
  soup = BeautifulSoup(page.content, "html.parser")

  movies = []
  for elm in soup.select(".sch_it"):
      if "blank_wrap" in elm["class"]:
          continue
      code = elm.select_one('.code').get_text()
      time = elm.select_one('.time').get_text()
      title_kor = elm.select_one('.film_tit_kor').get_text()
      title_eng = elm.select_one('.film_tit_eng').get_text()
      movie_obj = Movie(code, time, title_kor, title_eng)
      movies.append(movie_obj)

  sorted_movies = sorted(movies, key = lambda movie: movie.time)
  for movie in sorted_movies:
      print_str = '---\n'
      print_str += '코드 : '
      print_str += movie.code
      print_str += '   '

      print_str += '시간 : '
      print_str += movie.time
      print_str += '   '

      print_str += '제목 : **'
      print_str += movie.title_kor
      print_str += "**   "

      found1 = any(imported_movie == movie.title_kor for imported_movie in imported_list)
      found2 = any(recomm_movie == movie.title_kor for recomm_movie in muggle_recomm)
      if (found1):
        print_str += "(수입작)"
      if (found2):
        print_str += "(추천작)"
      print_str += '\n\n'

      f.write(print_str)
  f.write('\n')
f.close()