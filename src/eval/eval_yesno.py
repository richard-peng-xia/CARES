import json
import argparse
from eval_utils import *

def evaluate_yes_no(answers, labels):

    for answer in answers:
        text = answer['text']

        # Only keep the first sentence
        if text.find('.') != -1:
            text = text.split('.')[0]

        text = text.replace(',', '')
        words = text.split(' ')
        if 'No' in words or 'not' in words or 'no' in words:
            answer['text'] = 'no'
        else:
            answer['text'] = 'yes'

    for i in range(len(labels)):
        label = labels[i]
        if label.find('.') != -1:
            label = label.split('.')[0]
        label = label.replace(',', '')
        label = label.split(' ')
        if 'No' in label or 'not' in label or 'no' in label:
            labels[i] = 0
        else:
            labels[i] = 1

    pred_list = []
    for answer in answers:
        pred = answer['text']
        if pred.find('.') != -1:
            pred = pred.split('.')[0]
        pred = pred.replace(',', '')
        pred = pred.split(' ')
        if 'No' in pred or 'not' in pred or 'no' in pred:
            pred_list.append(0)
        else:
            pred_list.append(1)

    pos = 1
    neg = 0

    TP, TN, FP, FN = 0, 0, 0, 0
    for pred, label in zip(pred_list, labels):
        if pred == pos and label == pos:
            TP += 1
        elif pred == pos and label == neg:
            FP += 1
        elif pred == neg and label == neg:
            TN += 1
        elif pred == neg and label == pos:
            FN += 1

    print('TP\tFP\tTN\tFN\t')
    print('{}\t{}\t{}\t{}'.format(TP, FP, TN, FN))

    precision = float(TP) / float(TP + FP)
    recall = float(TP) / float(TP + FN)
    f1 = 2*precision*recall / (precision + recall)
    acc = (TP + TN) / (TP + TN + FP + FN)
    print('Accuracy: {}'.format(acc))
    print('Precision: {}'.format(precision))
    print('Recall: {}'.format(recall))
    print('F1 score: {}'.format(f1))


def main(args):
    with open(args.questions_file, 'r') as f:
        labels = [json.loads(line)['answer'] for line in f]

    with open(args.predictions_file, 'r') as f:
        answers = [json.loads(line) for line in f]

    evaluate_yes_no(answers, labels)

    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process answers and questions files.')
    parser.add_argument('--predictions_file', type=str, required=True, help='Path to the predictions file.')
    parser.add_argument('--questions_file', type=str, required=True, help='Path to the questions file.')
    args = parser.parse_args()

    main(args)