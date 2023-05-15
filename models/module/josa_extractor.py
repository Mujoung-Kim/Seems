from _init import *

from commons import string_util

class JosaExtractor :
    '''
        Constructor
        1. text : 들어온 문장
        2. extract_text : 추출한 단어목록
        3. josa_set : 조사 어미 사전
    '''
    def __init__(self) :
        self.text = ""
        self.extract_text = []
        # ~하며 부터는 해당 케이스에서 보이는 걸 추가한 것
        self.josa_set = [ "고", "하고", "부터", "와", "에게", "로써", "를", "은", "라고", "이랑", "이", "에서", "으로", "이다", "의", "가", "을", "까지", "로서", "서", "나", "께서", "이며", "에", "라", "과", "는", "조차", "랑", "도", "야말로", "보다", "로", "에다", "야", "마저", "이라고", "하며", "한다", "면", "해", "이었다", "였다", "했다", "에는", "으며", "으면", "있다", "입니다", "합니다", "이라는", "었다", "다", "한", "섰다" ]

    '''
        Methods
        1. set_text
        2. extract_josa
        3. add_keyword_set
        4. _print
    '''
    # text setting
    def set_text(self, text) :
        self.text = text

    # josa extract
    def extract_josa(self) :
        eojeols = self.text.split()
        eojeols = string_util.trim(eojeols, True)

        for eojeol in eojeols :
            eojeol = eojeol.replace(".", "").replace("'", "").replace('"', "").replace(",", "").replace("…", "")

            # 해당 어절의 끝에 조사가 포함되어 있는지 검사
            for josa in sorted(list(self.josa_set), reverse=True) :
                josa_len = len(josa)

                if eojeol.endswith(josa) :
                    eojeol = eojeol[:-josa_len]
                    break

            # 조사를 분리한 어절의 길이가 1이거나 숫자로만 구성된 경우 제외
            if len(eojeol) == 1 or eojeol == "" :
                continue

            if str(eojeol).isdigit() :
                continue

            self.extract_text.append(eojeol)

        return self.extract_text

    # add keyword_set
    def add_keyword_set(self, result_set: set) :
        for keyword in self.extract_text :
            result_set.add(keyword)

    # check member variable
    def _print(self) :
        print(f"text : {self.text}\n")

        print(f"extrat_text_len : {len(self.extract_text)}")
        print(f"extrat_text : {self.extract_text}\n")

        print(f"josa_set len : {len(self.josa_set)}")
        print(f"all josa_set : {self.josa_set}")

# main
# if __name__ == "__main__" :
#     text = "단음계이다."
#     keyword_set = {"터키", "온천", "민물고기", "마른버짐", "시리아", "대한민국", "스파", "이란", "일본"}

#     print(keyword_set, len(keyword_set))

#     josa = Josa()
#     josa.set_text(text)
#     josa.extract_josa()
#     josa.add_keyword_set(keyword_set)
#     print(keyword_set, len(keyword_set))
#     print()
#     josa._print()