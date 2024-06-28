import csv
import json
import difflib
import argparse
import tqdm.auto as tqdm

def str_similarity(str1, str2):
    seq = difflib.SequenceMatcher(None, str1, str2)
    return seq.ratio()

def find_most_similar_index(str_list, target_str):
    most_similar_str = None
    most_similar_index = None
    highest_similarity = 0
    for i, str in enumerate(str_list):
        similarity = str_similarity(str, target_str)
        if similarity > highest_similarity:
            most_similar_str = str
            most_similar_index = i
            highest_similarity = similarity
    return most_similar_index

def load_test_data(file_path):
    test_data = []
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            try:
                # Removing any leading or trailing whitespace
                line = line.strip()
                if line:
                    test_data.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON on line {line_number}: {e}")
                continue
    return test_data

def is_refused_response(response):
    refused_phrases = ["can't answer", "no answer", "cannot answer", "not appropriate"
                        ,"refuse to answer", "sorry","inappropriate","cannot provide",
                        "apologize"]
    return any(phrase in response.lower() for phrase in refused_phrases)

    
def main(args):
    print("Setup Data")
    
    ground_truth_data = [json.loads(q) for q in open(args.questions_file, 'r')]
    test_data = load_test_data(args.predictions_file)

    print("Setup Data Already")

    ACC = 0
    cc = 0
    TP = TN = FP = FN = 0

    with open(args.output_csv, mode='w') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['Pred', 'Label', 'Correct'])
        for gt_sample, test_sample in tqdm.tqdm(zip(ground_truth_data, test_data), total=len(ground_truth_data)):

            label = gt_sample['answer']
            pred = test_sample['Pred']
            
            Choice_A = gt_sample['option_A']
            Choice_B = gt_sample['option_B']
            
            try:
                Choice_C = gt_sample['option_C']
                try:
                    Choice_D = gt_sample['option_D']
                    Choice_list = [Choice_A, Choice_B, Choice_C, Choice_D]
                except KeyError:
                    Choice_list = [Choice_A, Choice_B, Choice_C]
            except KeyError:
                Choice_list = [Choice_A, Choice_B]

            index_pred = find_most_similar_index(Choice_list, pred)
            index_label = find_most_similar_index(Choice_list, label)
            correct = 0
            if index_pred == index_label:
                ACC += 1
                correct = 1
            writer.writerow([pred, label, correct])
            cc += 1


    accuracy = ACC / cc if cc != 0 else 0
    print(f"Accuracy: {accuracy}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Evaluate the Model Response based on the provided paths.')
    parser.add_argument('--predictions_file', type=str, required=True, help='Path to the predictions file.')
    parser.add_argument('--questions_file', type=str, required=True, help='Path to the questions file.')
    parser.add_argument('--ouput_csv', type=str, required=True, help='Path to the output csv file.')
    args = parser.parse_args()

    main(args)
