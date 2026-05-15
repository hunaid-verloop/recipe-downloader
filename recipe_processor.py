import json


from recipes_downloader import getRecipe

def process_recipe(recipe: dict)-> dict:
    # returns a simplified recipe stripping away unnecessary details
    blockMap: dict = recipe.get('BlockMap', {})
    simplified_recipe: dict = {}
    for _, block in blockMap.items():
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
                    arr = rhs_value.get('StringList', {})
                    arr_value = arr.get('Array', [])
                    rhs = f"[{', '.join(arr_value)}]" 
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
                arr = rhs_value.get('StringList', {})
                arr_value = arr.get('Array', [])
                rhs = f"[{', '.join(arr_value)}]" 
        condition_str = f"{lhs} {op} {rhs}"

    return {'NextBlock': next_block_id, "Condition": condition_str}


def process_message_block(name: str, block: dict):
    message_block: dict = {}
    msg_block_type = get_message_block_type(block)
    message_block['Name'] = name
    message_block: dict = {'Type': msg_block_type}

    # leading_message_block = block.get('LeadingMessage', {})
    # if msg_block_type == "ButtonBlock":
    #     message_block['content'] = process_button_block(leading_message_block)
    # elif msg_block_type == "QuestionBlock":
    #     message_block['content'] = process_question_block(leading_message_block)
    # elif msg_block_type == "SliderBlock":
    #     message_block['content'] = process_slider_block(leading_message_block)
    # elif msg_block_type == "ListBlock":
    #     message_block['content'] = process_list_block(leading_message_block)
    # elif msg_block_type == "MediaBlock":
    #     message_block['content'] = process_media_block(leading_message_block)
    # else:
    #     message_block['Content'] = leading_message_block.get('Text', '')

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
    # print(block_type)
    return block_type


#TODO
def process_message_block_todo(leading_message: dict):
    pass

#TODO
def process_media_block_todo(leading_message: dict):
    pass

#TODO
def process_question_block_todo(leading_message: dict):
    question_block: dict = {"Text": leading_message.get("Text", "")}
    quick_replies = []
    for qr in leading_message.get('QuickReplies', []):
        qr_text = qr.get("TextQuickReply", {}).get('Title')
        quick_replies.append(qr_text)
    question_block['QuickReplies'] = quick_replies
    return question_block 

#TODO
def process_button_block_todo(leading_message: dict):
    button_template = leading_message.get("Template", {}).get("ButtonTemplate", {})
    button_block: dict = {"Text": button_template.get('Title')}
    buttons = []
    for button in button_template.get('Buttons', []):
        b_text = button.get("Title", '')
        buttons.append(b_text)
    button_block['Buttons'] = buttons
    return button_block 

#TODO
def process_slider_block_todo(leading_message: dict):
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

#TODO
def process_list_block_todo(leading_message: dict):
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
            bt = block_type
            if "MessageBlock" in block:
                bt= get_message_block_type(block)
            block_name = block['Name']
            return f"{bt}({block_name})"
    else:
        return ""

if __name__ == '__main__':
    base_url = "https://hunaidc.verloop.io"
    recipe_id = "c0cc82e2-a29d-41e0-ae66-2caf55a2a44a"
    recipe = getRecipe(base_url, recipe_id)

    with open('unprocessed_recipe.json', 'w') as f:
        f.write(json.dumps(recipe))

    simplified_recipe = process_recipe(recipe.get("Recipe"))

    with open('processed_recipe.json', 'w') as f:
        f.write(json.dumps(simplified_recipe))
