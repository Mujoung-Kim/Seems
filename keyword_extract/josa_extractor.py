from _init import *

from commons import string_util

class JosaExtractor() :
	'''
		Constructor
		1. text : 들어온 문장
		2. josa_set : 조사 어미 사전
	'''
	def __init__(self, text: str, result_set: set) :
		self.text = text
		# ~하며 부터는 해당 케이스에서 보이는 걸 추가한 것
		self.josa_set = [ "고", "하고", "부터", "와", "에게", "로써", "를", "은", "라고", "이랑", "이", "에서", "으로", "이다", "의", "가", "을", "까지", "로서", "서", "나", "께서", "이며", "에", "라", "과", "는", "조차", "랑", "도", "야말로", "보다", "로", "에다", "야", "마저", "이라고", "하며", "한다", "면", "해", "이었다", "였다", "했다", "에는", "으며", "으면", "있다", "입니다", "합니다", "이라는", "었다", "다", "한", "섰다" ]

		self._set(result_set)

	'''
		Methods
		1. _set
		2. _print
	'''
	def _set(self, result_set: set) :
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

			result_set.add(eojeol)

	def _print(self) :
		print(f"eojeol : {self.text}\n")

		print(f"josa_set len : {len(self.josa_set)}")
		print(f"all josa_set : {self.josa_set}")

# main
# if __name__ == "__main__" :
# 	text = "가라루파는 터키의 온천에 사는 민물고기이다"
# 	text = "가 사무엘슨은 드러머로 1984년부터 1987년까지 메가데스의 일원이었다"
# 	text = "산란기는 4~8월로서 수컷은 산란기가 되면 몸 색이 흑청색으로 변화하며 물풀 등을 이용해 둥지를 만들고 암컷을 유인해 번식한다."
# 	text = "시코쿠 동북쪽에 있으며 서쪽에는 에히메현 남쪽에는 도쿠시마현 북쪽에는 세토 내해를 사이에 두고 오카야마현이 있다."
# 	result_set = {"터키", "온천", "민물고기"}

# 	josa = JosaExtractor(text, result_set)
# 	josa._print()

# 	print(result_set)