import os
import re
import json
import time
import random
import pandas as pd
from tqdm import tqdm
import anthropic
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configuración de la API de Claude
client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

def get_completion(prompt: str):
    try:
        response = client.messages.create(
            #model="claude-3-haiku-20240307",
            model= "claude-3-5-sonnet-20240620",
            system="You are an knowledge expert, you are supposed to answer the multi-choice question to derive your final answer as `The answer is ...`.",
            max_tokens=1024,
            temperature=0.1,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text
    except Exception as e:
        print(f"Error: {e}")
        return None


def load_mmlu_pro(csv_path_test, csv_path_val):
    encodings = ['utf-8', 'latin1', 'iso-8859-1']

    for encoding in encodings:
        try:
            test_df = pd.read_csv(csv_path_test, encoding=encoding)
            dev_df = pd.read_csv(csv_path_val, encoding=encoding)
            return test_df, dev_df
        except UnicodeDecodeError:
            print(f"Failed to read with encoding {encoding}, trying next encoding.")
        except Exception as e:
            print(f"An unexpected error occurred with encoding {encoding}: {e}")

    raise UnicodeDecodeError("All encoding attempts failed for both test and validation CSV files.")



def preprocess(df):
    df = df[df['options'] != 'N/A']
    df['cot_content'].fillna("Let think step by step.", inplace=True)
    res = df.groupby('category', group_keys=False).apply(lambda x: x.to_dict(orient='records')).to_dict()
    return res


def format_example(question, options, cot_content=""):
    #print(f"*** options before formating: {options}")
    #input("Press Enter to continue...")
    if isinstance(options, str):
        options = options.replace('“', '"').replace('”', '"')
        try:
            #print("options is a string, loading JSON")
            options = json.loads(options)
        except json.JSONDecodeError:
            print(f"Failed to decode options: {options}")
            options = options.strip('][').split(', ')
            options = [opt.strip('"') for opt in options]
    #print(f"Formatted options: {options}")
    #input("Press Enter to continue...")
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
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else:
        print("extraction failed:\n", text)
        return None


def run_single_question(single_question, cot_examples_dict, exist_result):
    exist = True
    #print(f"*** options: {single_question['options']}")
    #print(f"*** single_question: {single_question}")
    q_id = single_question["question_id"]
    for each in exist_result:
        if q_id == each["question_id"] and single_question["question"] == each["question"]:
            print("already exists, skip it")
            return each["pred"], each["response"], exist
    exist = False
    category = single_question["category"]
    #print(f"cot_examples_dict: {cot_examples_dict}")
    cot_examples = cot_examples_dict[category]
    question = single_question["question"]
    options = json.dumps(single_question["options"])
    options = json.loads(options)
    #print(f"*** options luego de json.loads: {options}")
    prompt = ""
    #print(f"*** cot_examples: {cot_examples}")
    #input("Press Enter to continue...")
    for each in cot_examples:
        #print(f"*** each: {each}")
        prompt += format_example(each["question"], each["options"], each["cot_content"])
        
    prompt += format_example(question, options).strip()
    try:
        start = time.time()
        #print("******* prompt: ", prompt)
        response = get_completion(prompt)
        #print(f"******* response: {response}")
        prompt = response
        #print("requesting costs: ", time.time() - start)
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
    #test_df = test_df.to_dict('records') 
    #dev_df = dev_df.to_dict('records')
    if not subjects:
        subjects = list(test_df.keys())
    #print("assigned subjects", subjects)
    
    for subject in subjects:
        #test_data = test_df[subject]
        test_data = test_df.to_dict('records') 
        #print(f"*** test_data: {test_data}")
        output_res_path = os.path.join(output_dir, subject + "_sonnet_3.5_result.json")
        output_summary_path = os.path.join(output_dir, subject + "_sonnet_3.5_summary.json")
        res, category_record = update_result(output_res_path)

        cot_examples_dict = preprocess(dev_df)

        for each in tqdm(test_data):
            #print(f"*** each: {each}")
            label = each["answer"]
            category = subject
            pred, response, exist = run_single_question(each, cot_examples_dict, res)
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
    output_dir = "eval_results/claude/"
    os.makedirs(output_dir, exist_ok=True)
    evaluate(assigned_subject, args.csv_path_test, args.csv_path_val)