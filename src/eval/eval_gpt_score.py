import json
import tqdm
from pprint import pprint
from collections import defaultdict
from utils.openai import client
import argparse
import time

class ChatEvaluation:
    @staticmethod
    def get_avg(x):
        return sum(x) / len(x) if len(x) > 0 else 0

    @staticmethod
    def eval(samples):
        score_dict = defaultdict(list)
        for sample in samples:
            question = sample.get('text', '')
            answer = sample.get('answer', '')
            model_output = sample.get('text', '')
            scores = [1, 10]
            if len(scores) == 2 and all(str(s).replace('.', '', 1).isdigit() for s in scores):
                gpt4_score = max(1, min(10, float(scores[0])))
                score_dict['gpt4_score'].append(gpt4_score)
            else:
                print(f"Skipping evaluation for sample with unexpected scores: {scores}")

        result = {}
        for key, scores in score_dict.items():
            result[key] = ChatEvaluation.get_avg(scores)
        result['data_size'] = len(score_dict.get('gpt4_score', []))

        return result

def chat_with_gpt(prompt):
    messages = [{"role": "system", "content": "You are a professional biomedical expert."}]
    messages.append({"role": "user", "content": prompt})

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=messages,
            temperature=0.7
        )
        response_content = response.choices[0].message.content
        return response_content
    except RateLimitError as e:
            print(f"Rate limit exceeded, retrying in 10 seconds...")
            time.sleep(10)


def process_jsonl(args):
    samples = []
    with open(args.questions_file, 'r') as infile1:
        total_lines = sum(1 for line in infile1)

    with open(args.questions_file, 'r') as infile1, open(args.predictions_file, 'r') as infile2:
        cnt = 0
        for line1, line2 in tqdm.tqdm(zip(infile1, infile2),total=total_lines):
            data1 = json.loads(line1)
            data2 = json.loads(line2)

            prompt = f"""Please evaluate the Model Response based on the provided biomedical Question and Answer. Please rate the helpfulness, relevance, accuracy, and level of details. Please provide a single score on a scale of 1 to 10, where a higher score indicates better quality. \n 
            Question: {data1['text']} \n 
            Answer: {data1['answer']} \n 
            Model Response: {data2['answer']} \n 
            Please output only the score."""
            response1 = chat_with_gpt(prompt)

            try:
                score = float(response1)
            except ValueError:
                print(f"Skipping evaluation for incomplete response: {response1}")
                continue
                
            new_sample = {
                'question': data1['text'],
                'answer': data1['answer'],
                'model_output': data2['answer'],
                'score': score
            }
            samples.append(new_sample)
            cnt += 1

            if cnt % 2 == 0:
                print("Processed 2 prompts, resting for 2 seconds...")
                time.sleep(2)

            with open(args.output_file, 'a') as outfile:
                json.dump(new_sample, outfile)
                outfile.write('\n')

        evaluation_results = ChatEvaluation.eval(samples)
        pprint(evaluation_results)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Evaluate the Model Response based on the provided biomedical Question and Answer.')
    parser.add_argument('--questions_file', type=str, required=True, help='Path to the questions file.')
    parser.add_argument('--predictions_file', type=str, required=True, help='Path to the predictions file.')
    parser.add_argument('--output_file', type=str, required=True, help='Path to the output JSONL file.')
    args = parser.parse_args()

    process_jsonl(args)
