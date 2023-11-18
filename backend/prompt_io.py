import json
import re


def load_prompt_template(path):
  with open(path, 'r') as file:
    file_content = file.read()
  return file_content


def parse_response(response):
    response = response.replace("\n", "")
    print("THE RESPONSE", response)
    return json.loads(response)

def parse_list_from_answer(answer):
    json_list_pattern = r'\[[^\]]*?\]'
    matches = re.findall(json_list_pattern, answer)
    print(matches)
    return json.loads(matches[0])