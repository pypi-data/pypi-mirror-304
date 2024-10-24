import sys
import argparse
#from utils.Preprocess import Preprocess
#from train_tools.create_dict import create_dict
#from dict.bind_dict import bind_dict
#from IntentModel import IntentModel
#from intent_classification_module import *

import intent_classification as ic


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                        prog='intent_classification',
                        description='사용자 입력에 따른 의도 분석을 진행하는 프로그램입니다. 학습 데이터를 입력 받아 CNN 기반 학습 이후 의도 분석 진행합니다.')

#    parser.add_argument('-i', '--inputdata', nargs='+', help="학습 시 사용할 데이터를 입력해야 합니다.")
    parser.add_argument('-d', '--dict', nargs='*', help="인물, 클래스, 장르, 소재, 감성 순으로 사전을 입력해야 합니다.")
    parser.add_argument('-tr', '--train_result', help="저장할 CNN 기반 학습 결과 파일 이름을 입력하세요. 파일 형태는 keras이여야 합니다.")

    parser.add_argument('-tf', '--train_file', nargs='*', help="학습 시 사용할 데이터를 입력해야 합니다.")
    parser.add_argument('-uf', '--userdic_file', help="사용자 정의 사전 파일을 입력합니다. 파일을 사용하지 않을 시 괄호와 같이 입력해주세요('')")
    parser.add_argument('-wf', '--word2index_file', help="단어 인덱스 사전 파일을 입력합니다. 파일 형태는 bin이어야 합니다. 파일을 사용하지 않을 시 괄호와 같이 입력해주세요('')")
    parser.add_argument('-L', '--MAX_SEQ_LEN', type=int, help="의도 분석 시 사용할 MAX_SEQ_LEN 값을 입력합니다. 해당 값은 CNN 기반 학습 진행했을 때의 MAX_SEQ_LEN값과 동일해야 합니다.")

    parser.add_argument('-u', '--userdic', help="사용자 정의 사전 파일 생성합니다.", action = 'store_true')
    parser.add_argument('-w', '--word2index', help="단어 인덱스 사전 파일 생성합니다. 파일 형태는 bin이어야 합니다.", action = 'store_true')
    parser.add_argument('-CL', '--calc_LEN', help="의도 분석 시 사용할 MAX_SEQ_LEN 값을 입력합니다. 해당 값은 CNN 기반 학습 진행했을 때의 MAX_SEQ_LEN값과 동일해야 합니다.", action = 'store_true')
    parser.add_argument('-t', '--training', help="CNN 기반 학습 진행합니다. 학습 진행 후 종료합니다.", action = 'store_true')
    parser.add_argument('-a', '--all_execute', help="의도 분석 진행합니다. 모든 작업 진행합니다.", action = 'store_true')
    args = parser.parse_args()

    print('dictList')
#    dictList = read_dict(args.dict[0], args.dict[1], args.dict[2], args.dict[3], args.dict[4])
    dictList = ic.read_dict(args.dict)

    if args.all_execute == True:
        print('create user_dict')
        ic.bind_dict(args.dict, args.userdic_file)

        print('create word2index_dict')
        ic.create_dict(args.train_file, args.word2index_file, args.userdic_file)

        print('data extracting')
        data = ic.data_extraction(args.train_file)

        print('labeling')
        df = ic.labeling(data, dictList)

        if args.calc_LEN == True:
            print('calc length')
            length = ic.length_calc(df)
            print(length)

        print('training using CNN')

        print(args.MAX_SEQ_LEN)

        if args.calc_LEN == True:
            ic.intent_classification_using_CNN(df, args.word2index_file, args.userdic_file, false, args.train_result)
        else:
            ic.intent_classification_using_CNN(df, args.word2index_file, args.userdic_file, args.MAX_SEQ_LEN, args.train_result)

        print('predict')
        p = ic.Preprocess(word2index_dic=args.word2index_file, userdic=args.userdic_file)
        if args.calc_LEN == True:
            intent = ic.IntentModel(model_name=args.train_result, preprocess=p, MAX_SEQ_LEN=length)
        else:
            intent = ic.IntentModel(model_name=args.train_result, preprocess=p, MAX_SEQ_LEN=args.MAX_SEQ_LEN)

        while 1:
            print("입력: ")
            input_ = input()

            if input_ == "exit":
                print('프로그램 종료')
                break

            else:
                NE = ic.named_entity(input_, dictList)
                print("개체명 인식: ", str(NE))
                print("의도 예측")
                classifying_data = intent.classify(input_)
                predict = intent.predict_class(classifying_data)
                predict_label = intent.labels[predict]
                print("의도 예측 레이블: ", predict_label)

    elif args.training == True:
        if args.userdic == True:
            print('create user_dict')
            ic.bind_dict(args.dict, args.userdic_file)

        if args.word2index == True:
            print('create word2index_dict')
            ic.create_dict(args.train_file, args.word2index_file, args.userdic_file)

        print('data extracting')
        data = ic.data_extraction(args.train_file)

        print('labeling')
        df = ic.labeling(data, dictList)

        if args.calc_LEN == True:
            print('calc length')
            length = ic.length_calc(df)
            print(length)

        print('training using CNN')

        if args.calc_LEN == True:
            ic.intent_classification_using_CNN(df, args.word2index_file, args.userdic_file, false, args.train_result)
        else:
            print(args.MAX_SEQ_LEN)
            ic.intent_classification_using_CNN(df, args.word2index_file, args.userdic_file, args.MAX_SEQ_LEN, args.train_result)

    else:
        print('predict')
        p = ic.Preprocess(word2index_dic=args.word2index_file, userdic=args.userdic_file)
        intent = ic.IntentModel(model_name=args.train_result, preprocess=p, MAX_SEQ_LEN=int(args.MAX_SEQ_LEN))

        while 1:
            print("입력: ")
            input_ = input()
    
            if input_ == "exit":
                print('프로그램 종료')
                break

            else:
                NE = ic.named_entity(input_, dictList)
                print("개체명 인식: ", str(NE))
                print("의도 예측")
                classifying_data = intent.classify(input_)
                predict = intent.predict_class(classifying_data)
                predict_label = intent.labels[predict]
                print("의도 예측 레이블: ", predict_label)
