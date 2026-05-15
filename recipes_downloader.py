import os
import argparse
import json
import csv
from concurrent.futures import ThreadPoolExecutor

import requests

{
"url": "https://aubankuat.verloop.io/gateway/twirp/verloop.gateway.recipe.RecipeService/GetRecipe",
"body": 
{
  "RecipeID": "4bbb6d9f-4002-4881-b620-69dc03b976c5"
},
"Authorization": """eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJ1TjhBUE56aER2Mk0xTFAwSGlNaXA4M292MUNoQ28wWDdic2RfeXh6SVpVIn0.eyJleHAiOjE3Nzg1MDU1NzYsImlhdCI6MTc3ODQ2MjM3NiwianRpIjoiYzAzM2M5OWQtYzQ2NS00ODQ3LWJmNjItNjA3ZWJjOTA4NTZjIiwiaXNzIjoiaHR0cHM6Ly9pYW0udmVybG9vcC5pby9yZWFsbXMvdmVybG9vcCIsInN1YiI6IjIyMjAzYTlhLTEwM2ItNDg5Zi04ODRjLWI5NWE1NmVhODA2NiIsInR5cCI6IkJlYXJlciIsImF6cCI6ImF1YmFua3VhdCIsInNpZCI6ImJhYmQwOGJjLWQyNGUtNGQ0Yy1hMWVjLTQ2MDk2ZjQzYjE4ZCIsImFjciI6IjEiLCJhbGxvd2VkLW9yaWdpbnMiOlsiaHR0cHM6Ly9hdWJhbmt1YXQudmVybG9vcC5pby8qIiwiLyoiXSwicmVzb3VyY2VfYWNjZXNzIjp7ImF1YmFua3VhdCI6eyJyb2xlcyI6WyJkZWZhdWx0X3Zlcmxvb3A6YWRtaW4iXX19LCJzY29wZSI6ImVtYWlsIHByb2ZpbGUiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwibmFtZSI6Ikh1bmFpZCIsInZlcmxvb3BfZW50aXR5X25hbWUiOiJIdW5haWQiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJodW5haWQuY29udHJhY3RvckB2ZXJsb29wLmlvIiwidmVybG9vcF9lbnRpdHlfc3RhdHVzIjoiZW5hYmxlZCIsImdpdmVuX25hbWUiOiJIdW5haWQiLCJ2ZXJsb29wX2VudGl0eV9yb2xlIjoiZGVmYXVsdF92ZXJsb29wOmFkbWluIiwiZW1haWwiOiJodW5haWQuY29udHJhY3RvckB2ZXJsb29wLmlvIiwidmVybG9vcF9lbnRpdHlfaWQiOiIyNjM5OGM1OS1iOWY2LTRhY2MtYjRjNy1mMTc5NGM1YzM3ZGIifQ.QDm7acFr-3jvt3R9wR9c9S__1VWiqrxps5Jvhm6H1-VGDBH5B0U1m5DMEtx_nVaWa_XwDJ4KZTwut4VXMj4-zL4eMl0I8oHJS4N0HfX1w1UjuBy-ORys_MVhX8ZsWgd0hWLoPRWPlg_Pjt07dqN_M1buNrxp4h0MsGwTf6oKkMkych3KDXg5xLuazrr039gap901iU3NgGHThit9RUb7-PL35Fj2m-VBx_-1DPdzEbMvKOpxgNOyn_W6ZcCyNoh8hMSwvNb5uSox_7XmMw6mR4H7tft7-Mn9-k5pw0ucdKPyW-RAojnm3wH4axIKb9shu274AVBCvDWWZL4X-KaQyw"""
}
######################################## processing the recipe #####################################

def process_recipe(recipe: dict)-> dict:
    # returns a simplified recipe stripping away unnecessary details
    blockMap: dict = recipe.get('BlockMap', {})
    simplified_recipe: dict = {}

    for block in blockMap.values():
        if "LLMBlock" in block:
            name = block.get('Name', '')
            simplified_recipe[name] = process_llm_block(name, block.get('LLMBlock', {}))
            next_block_id = block.get('NextBlockId', '')
            next_block = block_str(next_block_id, blockMap)
            simplified_recipe[name]['NextBlock'] = next_block
            continue
        if "WebhookBlock" in block:
            name = block.get('Name', '')
            simplified_recipe[name] = process_webhook_block(name, block.get('WebhookBlock', {}))
            next_block_id = block.get('NextBlockId', '')
            next_block = block_str(next_block_id, blockMap)
            simplified_recipe[name]['NextBlock'] = next_block
            continue
        if "TransferBlock" in block:
            name = block.get('Name', '')
            simplified_recipe[name] = process_transfer_block(name, block.get('TransferBlock', {}))
            next_block_id = block.get('NextBlockId', '')
            next_block = block_str(next_block_id, blockMap)
            simplified_recipe[name]['NextBlock'] = next_block
            continue
        if "CloseBlock" in block:
            name = block.get('Name', '')
            simplified_recipe[name] = process_close_block(name, block.get('CloseBlock', {}))
            next_block_id = block.get('NextBlockId', '')
            next_block = block_str(next_block_id, blockMap)
            simplified_recipe[name]['NextBlock'] = next_block
            continue
        if "APIBlock" in block:
            name = block.get('Name', '')
            simplified_recipe[name] = process_api_block(name, block.get('APIBlock', {}))
            next_block_id = block.get('NextBlockId', '')
            next_block = block_str(next_block_id, blockMap)
            simplified_recipe[name]['NextBlock'] = next_block
            continue
        if "ConditionBlock" in block:
            name = block.get('Name', '')
            simplified_recipe[name] = process_condition_block(name, block.get('ConditionBlock', {}))
            next_block_id = block.get('NextBlockId', '')
            next_block = block_str(next_block_id, blockMap)
            simplified_recipe[name]['NextBlock'] = next_block
            continue
        if "CodeBlock" in block:
            name = block.get('Name', '')
            simplified_recipe[name] = process_code_block(name, block.get('CodeBlock', {}))
            next_block_id = block.get('NextBlockId', '')
            next_block = block_str(next_block_id, blockMap)
            simplified_recipe[name]['NextBlock'] = next_block
            continue
        if "MessageBlock" in block:
            name = block.get('Name', '')
            simplified_recipe[name] = process_message_block(name, block.get("MessageBlock", {}))
            next_block_id = block.get('NextBlockId', '')
            next_block = block_str(next_block_id, blockMap)
            simplified_recipe[name]['NextBlock'] = next_block
            continue

    return simplified_recipe


def process_llm_block(name: str, block: dict):
    llm_block: dict = {'Type': "LLMBlock"}
    llm_block['Name'] = name
    prompts_ = []
    for prompt in block.get('PromptValues', []):
        prompt_txt = prompt.get('Text', '')
        intents = prompt.get('Intent', [])
        
        # for each prompt get the text and the intents detected with in the prompt text
        if prompt_txt != "":
            tmp = {'Text': prompt_txt}
            intents_ = []      
            for intent in intents:
                if intent.get("SelectedText") != "":
                    intents_.append(intent)
            tmp['intents'] = intents_

            prompts_.append(tmp)

    llm_block['Prompts'] = prompts_
    llm_block["Expressiveness"] = block.get("Expressiveness", 0) 

    tools = []
    for tool in block.get('ToolVariables', []):
        tmp = {}
        tmp['name'] = tool.get('ToolName', "")
        tmp['description'] = tool.get('ToolDescription', '')
        tmp['type'] = tool.get('Type', '')
        tmp['enabled'] = tool.get('Enabled', False)
        tmp['inputs'] = []
        for ti in tool.get('ToolInputs', []):
            tmp['inputs'].extend(ti.get('AcceptedVAlues', []))
        tools.append(tmp)
    llm_block['Tools'] = tools

    return llm_block


def process_webhook_block(name: str, block: dict):
    webhook_block: dict = {'Type': "WebhookBlock"}
    webhook_block['Name'] = name
    webhook_block['URL'] = block.get('URL', '')
    webhook_block['ResponseVariables'] = block.get('ResponseVariables', [])

    return webhook_block
    

def process_transfer_block(name: str, block: dict):
    transfer_block: dict = {'Type': "TransferBlock"}
    transfer_block['Name'] = name
    transfer_block['TransferMessage'] = block.get('TransferMessage', {}).get('Text','')
    transfer_block['AssignmentStrategy'] = block.get('AssignmentStrategy', '')
    
    return transfer_block


def process_close_block(name: str, block: dict):
    close_block: dict = {'Type': "CloseBlock"}
    close_block['Name'] = name
    close_block['Message'] = block.get('Message', {}).get('Text','')
    
    return close_block


def process_api_block(name: str, block: dict):
    api_block: dict = {'Type': "APIBlock"}
    api_block['Name'] = name
    api_method = block.get('Method','')
    api_block['Method'] = api_method
    api_block['URL'] = block.get('URL','')

    if "QueryParams" in block and len(block["QueryParams"]) != 0:
        api_block['QueryParams'] = []
        for param in block["QueryParams"]:
            k = param["Key"]
            value_kind = param["ValueKind"]
            value = ""
            if "Variable" in value_kind:
                variable = value_kind["Variable"]
                value = f'{variable.get("Id", "")} Type: {variable.get("Type", "")} Scope: {variable.get("Scope", "")} kind: {variable.get("VariableKind", "")}'
            else:
                value = value_kind["StringValue"]
            api_block['QueryParams'].append({"key": k, "value": value})

    if "Headers" in block:
        headers: dict = block.get('Headers', {})
        api_block['Headers'] = []
        for k, v in headers.get("Data", {}).items():
            value = ""
            if "Variable" in v:
                variable = v["Variable"]
                value = f'{variable.get("Id", "")} Type: {variable.get("Type", "")} Scope: {variable.get("Scope", "")} kind: {variable.get("VariableKind", "")}'
            else:
                value = v["StringValue"]
            api_block['Headers'].append({"key": k, "value": value})

    if api_method and api_method != "GET":
        if 'FormUrlEncoded' in block:
            api_block['PayloadType'] = 'FormUrlEncoded'
            form_data = block['FormUrlEncoded'].get('Data', {})
            api_block['Payload'] = []
            for k, v in form_data.items():
                value = ""
                if "Variable" in v:
                    variable = v["Variable"]
                    value = f'{variable.get("Id", "")} Type: {variable.get("Type", "")} Scope: {variable.get("Scope", "")} kind: {variable.get("VariableKind", "")}'
                else:
                    value = v["StringValue"]
                api_block['Payload'].append({"key": k, "value": value})
        elif 'FormData' in block:
            api_block['PayloadType'] = 'FormData'
            form_data = block['FormData'].get('Data', {})
            api_block['Payload'] = []
            for k, v in form_data.items():
                value = ""
                if "Variable" in v:
                    variable = v["Variable"]
                    value = f'{variable.get("Id", "")} Type: {variable.get("Type", "")} Scope: {variable.get("Scope", "")} kind: {variable.get("VariableKind", "")}'
                else:
                    value = v["StringValue"]
                api_block['Payload'].append({"key": k, "value": value})
        elif 'JSON' in block:
            api_block['PayloadType'] = 'JSON'
            api_block['Payload'] = block['JSON']
        else:
            api_block['Payload'] = None
    
    return api_block

def process_code_block(name: str, block: dict):
    code_block: dict = {'Type': "CodeBlock"}
    code_block['Name'] = name
    code_block['Code'] = block.get('Code', '')
    CodeSuccessBlockId = block.get('CodeSuccessBlockId', '')
    plugins = block.get('SelectedPlugins', [])
    if len(plugins) > 0:
        code_block['plugins'] = []
    for plugin in plugins:
        code_block['plugins'].append({
            "id": plugin.get('be713ca8-df1d-4a31-ac40-6d0c255db68a', ''),
            "Type": plugin.get('Type', '')
        })
    if 'Variables' in block:
        code_block['variables'] = []
        for k, v in block.get('Variables').items():
            code_block['variables'].append(f'{k} Type: {v.get("Type", "")} Scope: {v.get("Scope", "")} kind: {v.get("VariableKind", "")}')


    # if CodeSuccessBlockId != "":
    #     code_block['CodeSuccessBlock'] = block_str(CodeSuccessBlockId)
    
    return code_block


def process_condition_block(name: str, block: dict):
    condition_block: dict = {'Type': "ConditionBlock"}
    condition_block['Name'] = name
    conditions = []
    for condition in block.get('Conditions', []):
        formatted_condition = format_condition(condition)
        conditions.append(formatted_condition)
    condition_block['Conditions'] = conditions    

    return condition_block

def format_condition(condition: dict):
    next_block_id = condition.get('NextBlockId','')
    # next_block = block_str(next_block_id)
    condition_list = condition.get('ConditionList', {})
    condition_str = ""
    if 'ConditionWrapper' in condition_list:
        # compound the condition with 'OR' or 'AND'
        condition_wrapper: dict = condition_list.get('ConditionWrapper', {})
        conditions_arr: list = []
        conditions: list = condition_wrapper.get('Conditions', [])
        op_compound: str = condition_wrapper.get('Operator', 'OR')
        op_compound = f" {op_compound} "
        for cond in conditions:
            cond_ = cond.get('Condition', {})
            lhs = cond_.get('LHS', {}).get('Variable', {}).get('Id', '')
            op = cond_.get('Operator', {})
            rhs_dict = cond_.get('RHS', {})
            rhs = ""
            if "Variable" in rhs_dict:
                rhs = rhs_dict.get('Variable', {}).get('Id', '')
            else:
                rhs_value = rhs_dict.get('Value', {})
                if 'StringValue' in rhs_value:
                    rhs = rhs_value.get('StringValue', '')
                else:
                    arr = rhs.get('StringList', [])
                    rhs = f"[{', '.join(arr)}]" 
            conditions_arr.append(f"{lhs} {op} {rhs}")

        condition_str = op_compound.join(conditions_arr)
    else:
        cond_ = condition_list.get('Condition', {})
        lhs = cond_.get('LHS', {}).get('Variable', {}).get('Id', '')
        op = cond_.get('Operator', {})
        rhs_dict = cond_.get('RHS', {})
        rhs = ""
        if "Variable" in rhs_dict:
            rhs = rhs_dict.get('Variable', {}).get('Id', '')
        else:
            rhs_value = rhs_dict.get('Value', {})
            if 'StringValue' in rhs_value:
                rhs = rhs_value.get('StringValue', '')
            else:
                arr = rhs.get('StringList', [])
                rhs = f"[{', '.join(arr)}]" 
        condition_str = f"{lhs} {op} {rhs}"

    return {'NextBlock': next_block_id, "Condition": condition_str}


def process_message_block(name: str, block: dict):
    msg_block_type = get_message_block_type(block)
    message_block['Name'] = name
    message_block: dict = {'Type': msg_block_type}

    leading_message_block = block.get('LeadingMessage', {})
    if msg_block_type == "ButtonBlock":
        message_block['content'] = process_button_block(leading_message_block)
    elif msg_block_type == "QuestionBlock":
        message_block['content'] = process_question_block(leading_message_block)
    elif msg_block_type == "SliderBlock":
        message_block['content'] = process_slider_block(leading_message_block)
    elif msg_block_type == "ListBlock":
        message_block['content'] = process_list_block(leading_message_block)
    elif msg_block_type == "MediaBlock":
        message_block['content'] = process_media_block(leading_message_block)
    else:
        message_block['Content'] = leading_message_block.get('Text', '')

    return message_block


def get_message_block_type(block: dict):
    block_type = "MessageBlock"
    leading_message = block.get("LeadingMessage", {})
    if "Button" == block.get('Type', ''):
        block_type = "ButtonBlock"
    elif "Question" == block.get('Type', ''):
        block_type = "QuestionBlock"
    elif "Card" == block.get('Type', ''):
        block_type = "SliderBlock"
    elif "List" == block.get('Type', ''):
        block_type = "ListBlock"
    elif leading_message.get('Attachments', {}):
        block_type = "MediaBlock"
    print(block_type)
    return block_type


def process_message_block(leading_message: dict):
    pass

def process_media_block(leading_message: dict):
    pass

def process_question_block(leading_message: dict):
    question_block: dict = {"Text": leading_message.get("Text", "")}
    quick_replies = []
    for qr in leading_message.get('QuickReplies', []):
        qr_text = qr.get("TextQuickReply", {}).get('Title')
        quick_replies.append(qr_text)
    question_block['QuickReplies'] = quick_replies
    return question_block 

def process_button_block(leading_message: dict):
    button_template = leading_message.get("Template", {}).get("ButtonTemplate", {})
    button_block: dict = {"Text": button_template.get('Title')}
    buttons = []
    for button in button_template.get('Buttons', []):
        b_text = button.get("Title", '')
        buttons.append(b_text)
    button_block['Buttons'] = buttons
    return button_block 


def process_slider_block(leading_message: dict):
    slider_block: dict = {}
    cards= []
    for card in leading_message.get('cards', []):
        title = card.get('Title', '')
        sub_title = card.get('Subtitle', '')
        buttons = []
        for btn in card.get('Buttons', []):
            buttons.append(btn.get('Title', ''))
        cards.append({'title': title, 'sub_title': sub_title, 'buttons': buttons})
    slider_block['cards'] = cards
    return slider_block 


def process_list_block(leading_message: dict):
    list_block: dict = {}
    cards= []
    for card in leading_message.get('cards', []):
        title = card.get('Title', '')
        sub_title = card.get('Subtitle', '')
        buttons = []
        for btn in card.get('Buttons', []):
            buttons.append(btn.get('Title', ''))
        cards.append({'title': title, 'sub_title': sub_title, 'buttons': buttons})
    list_block['cards'] = cards
    return list_block 


def block_str(block_id: str, block_map: dict):
    if block_id in block_map:
        block = block_map[block_id]
        block_types = ["LLMBlock", "WebhookBlock", "TransferBlock", "OrderDetailBlock", 
                       "APIBlock", "ConditionBlock", "FAQBlock", "CodeBlock", "MessageBlock", "CloseBlock"]
        for block_type in block_types:
            if "MessageBlock" in block:
                block_type = get_message_block_type(block)
            block_name = block['Name']
            return f"{block_type}({block_name})"
    else:
        return ""



######################################## fetching/saving the recipes ############################################

LIST_RECIPES = "/gateway/twirp/verloop.gateway.recipe.RecipeService/ListRecipes"
GET_RECIPE = "/gateway/twirp/verloop.gateway.recipe.RecipeService/GetRecipe"

OUTPUT_DIR = os.path.join(os.getcwd(), "fetched_recipes")

auth_key = os.getenv('auth_key', '')



def listRecipes(base_url: str):
    url = base_url + LIST_RECIPES
    headers = {"content-type": "application/json",
               "authorization": auth_key,
               }
    payload = { "params": [] }
    resp = requests.post(
        url = url,
        json = payload,
        headers=headers
    ).json()
    return resp['Recipes']

def getRecipe(base_url: str, recipe_id: str):
    url = base_url + GET_RECIPE
    headers = {"content-type": "application/json",
               "authorization": auth_key,
               }
    payload = { "RecipeID": recipe_id }
    resp = requests.post(
        url = url,
        json = payload,
        headers=headers
    ).json()

    return resp

def fetch_and_save_recipe(base_url: str, recipe_id: str):
    recipe = getRecipe(base_url, recipe_id)
    file_name = os.path.join(OUTPUT_DIR, f'{recipe_id}.json')
    with open(file_name, 'w') as f:
        json.dump(recipe, f)


def build_id_name_map(base_url: str):
    recipe_list = listRecipes(base_url)
    recipe_id_list = [item['Meta']['Id'] for item in recipe_list]
    
    id_name = []
    for recipe_id in recipe_id_list:
        recipe = getRecipe(base_url, recipe_id)
        id_name.append({"recipe_id": recipe_id, "recipe_name": recipe['Recipe']['Name']})


    print(id_name)

    with open('id_name-mapping.csv', 'w', newline='') as csvfile:
        fieldnames = ['recipe_id', 'recipe_name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(id_name)
    

def main(base_url: str, max_workers=3):
    recipe_list = listRecipes(base_url)
    recipe_id_list = [item['Meta']['Id'] for item in recipe_list]
    os.mkdir(OUTPUT_DIR)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(fetch_and_save_recipe, base_url, recipe_id) for recipe_id in recipe_id_list]
        for f in futures:
            f.result()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A basic greeting script.")
    parser.add_argument("--base_url", help="client dashboard")
    args = parser.parse_args()

    if auth_key == "":
        print("Please provide your authorization key to access the verloop api")
    else:
        print(args)
        print(args.base_url)
        # main(base_url=args.base_url)
        build_id_name_map(args.base_url)
