from baidu_engine import bing_search
import subprocess
import json

def execute_command_and_get_json(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            json_result = result.stdout.strip()
            print(json_result)
            try:
                data = json.loads(json_result)
                return data
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                return None
        else:
            print(f"Error executing command: {result.stderr}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

results = execute_command_and_get_json("python ./baidu_engine.py {} {}".format("斗战胜佛",3))

if isinstance(results, list):
    print("search results：(total[{}]items.)".format(len(results)))
    for res in results:
        print("    title: {}\n    description: {}\n    url: {} \n".format(res["title"], res["description"], res["url"]))
