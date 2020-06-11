import pickle
import os

# 미션 9 : 사용자의 가장 오래 버틴 생존 시간을 최대 10개까지 파일에 기록한다.
class RankingProcessor:
    def __init__(self, filename):
        self.filename = filename

        # 파일의 유무를 먼저 파악해 파일이 없을 경우 만들어줌
        self.chk_ranking_file(self.filename)
        self.records = self.load_ranking_file()

    # filename이 해당 디렉토리에 존재하지 않을 경우 새로 만들어줌
    # .gitignore에서 'ranking'이라는 이름의 파일을 스테이징 대상에서 제외함
    def chk_ranking_file(self, filename:str):
        if filename not in os.listdir():
            with open(filename, 'wb') as f:
                print("{}이 존재하지 않아 새로 생성합니다.".format(filename))


    # 랭킹 정보가 담긴 파일을 리스트로 변환하여 반환해줌
    def load_ranking_file(self)->list:
        f = open(self.filename, 'rb')
        try:
            # 파일로부터 데이터 가져오기
            data = pickle.load(f)
        except EOFError:
            # 파일에 아무 것도 저장되어 있지 않은 경우,
            # 기록이 없다는 의미이므로 빈 리스트를 리턴해주면 됨
            data = list()
        finally:
            # 파일 닫아주기
            f.close()
        
        return data

    # 개임 내에서 기록을 0.1초 단위로 기록하므로
    # 기록을 저장할 때는 소숫점 아래 1자리까지 표현하는 str로 저장(2번째 자리에서 반올림)
    def add_to_ranking_file(self, new_record:float):
        # 랭킹 정보 추가(소수점 아래 2번째에서 반올림해줌)
        self.records.append("{:0.1f}".format(round(new_record, 2)))
        # 랭킹 정렬(내림차순)
        self.records.sort(key=lambda r: float(r), reverse=True)
        
        # 상위기록 10개를 제외한 나머지 기록을 버림
        self.records = self.records[:10]

        # 기존 파일에 쓰기
        with open(self.filename, 'wb') as f:
            pickle.dump(self.records, f)
        

if __name__ == "__main__":
    filename = "ranking"
    ranking_class = Ranking(filename)
    for i in range(1, 100):
        ranking_class.add_to_ranking_file(i*1.13)
        print(ranking_class.load_ranking_file())
