import os
import re
import json
import time
import random
import pandas as pd
from tqdm import tqdm
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
os.environ['OpenAI_API_KEY'] 
client = OpenAI()
def get_completion(prompt: str):
    final_prompt = [
        {
            "role": "system",
            "content": "You are a knowledge expert, you are supposed to answer the multi-choice question to derive your final answer as `The answer is ...`."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
    response = client.chat.completions.create(
        model="gpt-4o-2024-05-13",
        messages=final_prompt,
        temperature=0.1,
        max_tokens=4096,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["Question:"]
    )

    return response.choices[0].message['content']

def load_mmlu_pro(csv_path_test, csv_path_val):
    test_df = pd.read_csv(csv_path_test)
    val_df = pd.read_csv(csv_path_val)
    test_df = preprocess(test_df)
    val_df = preprocess(val_df)
    return test_df, val_df

def preprocess(df):
    # Asegurarse de que las columnas necesarias existan
    if 'cot_content' not in df.columns:
        df['cot_content'] = "Let think step by step."
    else:
        df['cot_content'] = df['cot_content'].fillna("Let think step by step.")
    
    if 'category' not in df.columns:
        df['category'] = "default_category"
    
    if 'question_id' not in df.columns:
        df['question_id'] = range(1, len(df) + 1)
    
    df = df[df['options'] != 'N/A']
    res = df.groupby('category', group_keys=False, as_index=False).apply(lambda x: x.to_dict(orient='records')).to_dict()
    return res

def format_example(question, options, cot_content=""):
    options = options.split("; ")
    if cot_content.startswith("A: "):
        cot_content = cot_content[3:]
    example = "Question: {}\nOptions: ".format(question)
    choice_map = "ABCDEFGHIJ"
    for i, opt in enumerate(options):
        example += "{}. {}\n".format(choice_map[i], opt)
    example += "Answer: " + cot_content + "\n\n"
    return example

def extract_answer(text):
    pattern = r"answer is \(?([ABCDEFGHIJ])\)?"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1)
    else:
        print("extraction failed:\n", text)
        return None

def run_single_question(single_question, cot_examples_dict, exist_result):
    exist = True
    q_id = single_question.get("question_id")
    if not q_id:
        raise KeyError("Missing 'question_id' in single_question.")
    
    for each in exist_result:
        if q_id == each["question_id"] and single_question["question"] == each["question"]:
            print("already exists, skip it")
            return each["pred"], each["response"], exist
    exist = False
    category = single_question["category"]
    cot_examples = cot_examples_dict[category]
    question = single_question["question"]
    options = json.dumps(single_question["options"])
    options = json.loads(options)
    prompt = ""
    for each in cot_examples:
        prompt += format_example(each["question"], each["options"], each["cot_content"])
        
    prompt += format_example(question, options).strip()
    try:
        start = time.time()
        response = get_completion(prompt)
        print("requesting costs: ", time.time() - start)
    except Exception as e:
        print("error", e)
        return None, None, exist
    pred = extract_answer(response)
    return pred, response, exist

def update_result(output_res_path):
    category_record = {}
    res = []
    success = False
    while not success:
        try:
            if os.path.exists(output_res_path):
                with open(output_res_path, "r") as fi:
                    res = json.load(fi)
                    for each in res:
                        category = each["category"]
                        if category not in category_record:
                            category_record[category] = {"corr": 0.0, "wrong": 0.0}
                        if not each["pred"]:
                            random.seed(12345)
                            x = random.randint(0, len(each["options"]) - 1)
                            if x == each["answer_index"]:
                                category_record[category]["corr"] += 1
                                print("random hit.")
                            else:
                                category_record[category]["wrong"] += 1
                        elif each["pred"] == each["answer"]:
                            category_record[category]["corr"] += 1
                        else:
                            category_record[category]["wrong"] += 1
            success = True
        except Exception as e:
            print("Error", e, "sleep 2 seconds")
            time.sleep(2)
    return res, category_record

def evaluate(subjects, csv_path_test, csv_path_val):
    test_df, dev_df = load_mmlu_pro(csv_path_test, csv_path_val)
    if not subjects:
        subjects = list(test_df.keys())
    print("assigned subjects", subjects)
    
    for subject in subjects:
        test_data = test_df[subject]
        output_res_path = os.path.join(output_dir, subject + "_result.json")
        output_summary_path = os.path.join(output_dir, subject + "_summary.json")
        res, category_record = update_result(output_res_path)

        for each in tqdm(test_data):
            label = each["answer"]
            category = subject
            pred, response, exist = run_single_question(each, dev_df, res)
            if exist:
                continue
            if response is not None:
                res, category_record = update_result(output_res_path)
                if category not in category_record:
                    category_record[category] = {"corr": 0.0, "wrong": 0.0}
                each["pred"] = pred
                each["response"] = response
                res.append(each)
                if pred is not None:
                    if pred == label:
                        category_record[category]["corr"] += 1
                    else:
                        category_record[category]["wrong"] += 1
                else:
                    category_record[category]["wrong"] += 1
                save_res(res, output_res_path)
                save_summary(category_record, output_summary_path)
                res, category_record = update_result(output_res_path)
        save_res(res, output_res_path)
        save_summary(category_record, output_summary_path)

def save_res(res, output_res_path):
    temp = []
    exist_q_id = set()
    for each in res:
        if each["question_id"] not in exist_q_id:
            exist_q_id.add(each["question_id"])
            temp.append(each)
    with open(output_res_path, "w") as fo:
        json.dump(temp, fo)

def save_summary(category_record, output_summary_path):
    total_corr = 0.0
    total_wrong = 0.0
    for k, v in category_record.items():
        if k == "total":
            continue
        cat_acc = v["corr"] / (v["corr"] + v["wrong"])
        category_record[k]["acc"] = cat_acc
        total_corr += v["corr"]
        total_wrong += v["wrong"]
    acc = total_corr / (total_corr + total_wrong)
    category_record["total"] = {"corr": total_corr, "wrong": total_wrong, "acc": acc}
    with open(output_summary_path, "w") as fo:
        json.dump(category_record, fo)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--category", type=str, default="all")
    parser.add_argument("--csv_path_test", type=str, required=True, help="Path to the input CSV file for test data")
    parser.add_argument("--csv_path_val", type=str, required=True, help="Path to the input CSV file for validation data")
    args = parser.parse_args()

    assigned_subject = [args.category] if args.category != "all" else []
    output_dir = "eval_results/gpt4o/"
    os.makedirs(output_dir, exist_ok=True)
    evaluate(assigned_subject, args.csv_path_test, args.csv_path_val)
