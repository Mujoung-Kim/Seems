## SEEMS (Sentence Eojeol Emjeol Morph Spell)
  - 보통 프로젝트들은 모델을 이용해여 결과를 내는 것에 치중했다면 우리의 프로젝트는 텍스트 데이터를 가지고 있다면 쉽게 모델 학습을 할 수 있으며, 이를 통해 결과를 볼 수 있다. 라는 차이가 있다.
  - 또한 텍스트에 따라 4가지의 모델(문장분리, 띄어쓰기 교정, 키워드 추출, 오타 교정)을 상황에 맞춰 사용할 수 있도록 하나의 라이브러리로 구성했으며, 해당 모델들의 유지보수를 용이하게 모듈화 시켰다.

## Dataset
  - Wikipedia에서 100만개의 쿼리를 이용해 80만 라인의 텍스트 문단/문장 크롤링
    - prototype model 은 1만개의 문장/문단을 이용하여 학습  
  - Labeling
    - sentence_model : 들어온 텍스트에서 "."을 기준으로 문장으로 분리 후 "."이 텍스트 내에 포함되어 있으면 1, 없으면 0
    - space_model : 들어온 텍스트를 공백을 기준으로 어절 단위로 나눈 후 해당 어절의 가장 마지막 음절에 1, 없으면 0
    - keyword_model : 들어온 텍스트를 공백을 기준으로 어절 단위로 나눈 후 해당 어절의 첫 음절부터 비교하여 키워드 사전에 있는 단어일 경우 있으면 1, 없으면 0
      > 만약 키워드 셋에 없지만 해당 단어의 뒤에 조사가 있다면 해당 단어도 키워드 사전에 추가
    - spell_model : 들어온 텍스트에 오타가 있으면 1, 없으면 0
<br>

## BertModel
  - bert_model
    - BERT는 Bidirectional Encoder Representations from Transformer의 약자로 2018년 구글에서 발표된 언어모델입니다. 사전 훈련된 모델을 활용하여 다양한 자연어처리 작업을 수행할 수 있는 다목적 언어모델입니다.
    - BERT모델은 크게 2가지 버전으로 나눌 수 있습니다. BERT-base는 12개의 인코더 층과 110M개의 파라미터를 가지는 모델입니다. 일반적인 자연어처리 작업에 대해 충분한 성능을 보여줍니다. BERT-large모델은 24개의 인코더 층과 340M개의 파라미터를 가지는 모델입니다. BERT-base보다 더 큰 모델로, 더욱 복잡한 자연어처리 작업에 대해 더 좋은 성능을 보여줍니다.
    - BERT모델의 특징은 첫 번째 사전 훈련 방법으로 양방향 언어 모델링을 사용합니다. 즉, 문장의 왼쪽과 오른쪽 모두를 동시에 고려하여 단어의 임베딩을 생성합니다. 이를 통해, 문장 내 단어의 문맥 정보를 더 잘 파악할 수 있습니다. 두 번재 BERT 모델은 사전 훈련된 모델을 활용하여, 다양한 자연어처리 작업에 적용할 수 있습니다. 예를 들어, 문장 분류, 질의 응답, 개체명 인식, 기계 번역 등의 작업에 사용됩니다. 마지막으로 다국어 자연어처리 작업에도 적용 가능합니다. 여러 언어의 텍스트 데이터를 이용하여 모델을 사전 훈련하고, 다양한 언어의 자연어처리 작업에 적용할 수 있습니다.
  - klue_bert_model
    - BERT-Klue 모델은 이번 개발에 사용될 모델이며 한국어 자연어처리를 위한 벤치마크 데이터셋으로 대규모의 한국어 텍스트 데이터를 사용하여 학습된 BERT모델을 평가하기 위한 목적으로 만들어졌습니다. 다양한 NLP태스크에 대한 데이터셋을 포함하고 있으며, 각각의 태스크는 여러 개의 라벨을 가지고 있습니다. 이 데이터셋을 이용하여 BERT와 같은 사전 학습된 모델의 성능을 평가할 수 있으며 이를 통해 모델 개발과 평가의 표준화 및 진보가 가능해졌습니다. Klue는 KLU(Korean Language Understanding Evaluation)팀에서 제작하였습니다.
<br>

## Library structural diagram

  ![](/figures/library_structural.png)
<br>


## Model process

  ![](/figures/model_preocess.png)
<br>

## Model performance

  ### Sentence split model
    - column : max_seq_len   batch_size   accuracy
    - index : model_layer
    - 위의 형태로 표 들어감
<br>

  ### Space correct model
    - column : max_seq_len   batch_size   accuracy
    - index : model_layer
    - 위의 형태로 표 들어감
<br>

  ### Keyword extract model
    - column : max_seq_len   batch_size   accuracy
    - index : model_layer
    - 위의 형태로 표 들어감
<br>

  ### Spell correct model
    - column : max_seq_len   batch_size   accuracy
    - index : model_layer
    - 위의 형태로 표 들어감
<br>

## Library run example

- code
  ```python
    from models.sentence_split_model import SentenceSplitModel

    # hyperparameter
    MAX_SEQ_LEN = 32
    EPOCHS = 50
    BATCH_SIZE = 128
    LEARNING_RATE = 1e-5
    PATIENCE = 10

    # 사용할 model
    model = SentenceSplitModel(MAX_SEQ_LEN)

    # raw_data path
    work_dir = "../../data/sentence_split/"
    in_path = work_dir + "inputs/"

    # train_data out path
    out_file_path = work_dir + "train_sentence_split.txt"

    # raw_data labeling & reformating
    model.make_train_data(in_path, out_file_path)
    # data load to data
    model.load_train_data(out_file_path, "\t", "UTF-8", 9, 1)

    # save model path
    model_path = work_dir + "sentence_split_model.h5"

    # model train
    model.train(model_path, EPOCHS, BATCH_SIZE, LEARNING_RATE, PATIENCE)

    # best model load
    model.load_model(model_path)

    # test text
    text = "가라루파는 터키의 온천에 사는 민물고기이다. 하지만 이 물고기가 실제로 피부병을 치료하는 데 효과가 있는지에 대해서는 논란이 있다. 가라루파는 주로 터키, 시리아, 이란, 그리고 이라크에 분포한다."

    # model predictions for the text
    sentences = model.predict(text)

    # print result
    for sentence in sentences :
      print(sentence)
  ```
<br>

- result
  ```cmd
    가라루파는 터키의 온천에 사는 민물고기이다.
    하지만 이 물고기가 실제로 피부병을 치료하는 데 효과가 있는지에 대해서는 논란이 있다.
    가라루파는 주로 터키, 시리아, 이란, 그리고 이라크에 분포한다.
  ```
<br>

## 개발 환경(Requirements)
   - Language
     - python == 3.9.13
   - Tool
     - vscode, colab, github
   - GPU Library
     - CUDA == 11.2
     - cuDNN == 8.1
   - Library
     - numpy >= 1.24.3
     - torch == 1.9.0
     - tensorflow == 2.10.0
     - tensorflow-addons >= 0.20.0
     - transformer == 4.28.1