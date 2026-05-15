from recipes_downloader import *
import json

#################################################Test for LLMBlock##############################################
def test_process_llm_block():
  with open('./example_blocks/llm_block.json') as f:
    llmblock = json.load(f)
  with open('./transformed_blocks/llmblock_transformed.json', 'w') as o:
    o.write(json.dumps(process_llm_block("Global_Entry", llmblock)))

#################################################Test for WebhookBlock##############################################
def test_process_webhook_block():
  with open('./example_blocks/webhook_block.json') as f:
    webhookblock = json.load(f)
  with open('./transformed_blocks/webhookblock_transformed.json', 'w') as o:
    o.write(json.dumps(process_webhook_block("get_customer_details_cc", webhookblock)))

#################################################Test for TransferBlock##############################################
def test_process_transfer_block():
  with open('./example_blocks/transfer_block.json') as f:
    transferblock = json.load(f)
  with open('./transformed_blocks/transferblock_transformed.json', 'w') as o:
    o.write(json.dumps(process_transfer_block("transfer2", transferblock)))

#################################################Test for CloseBlock##############################################
def test_process_close_block():
  with open('./example_blocks/transfer_block.json') as f:
    closeblock = json.load(f)
  with open('./transformed_blocks/closeblock_transformed.json', 'w') as o:
    o.write(json.dumps(process_close_block("Close", closeblock)))


#################################################Test for APIBlock##############################################
def test_process_api_block():
  with open('./example_blocks/api_block.json') as f:
    apiblock = json.load(f)
  with open('./transformed_blocks/apiblock_transformed.json', 'w') as o:
    o.write(json.dumps(process_api_block("Api 1", apiblock)))


#################################################Test for CodeBlock##############################################
def test_process_code_block():
  with open('./example_blocks/code_block.json') as f:
    codeblock = json.load(f)
  with open('./transformed_blocks/codeblock_transformed.json', 'w') as o:
    o.write(json.dumps(process_code_block("Code 1", codeblock)))


#################################################Test for ConditionBlock##############################################
def test_process_condition_block():
  with open('./example_blocks/condition_block.json') as f:
    conditionblock = json.load(f)
  with open('./transformed_blocks/conditionblock_transformed.json', 'w') as o:
    o.write(json.dumps(process_condition_block("Condition 1", conditionblock)))

#################################################Test for MessageBlock Type##############################################
def test_get_message_block_type():
  for eg in ['./example_blocks/button_block.json', './example_blocks/question_block.json',
             './example_blocks/slider_block.json', './example_blocks/list_block.json',
             './example_blocks/media_block.json', './example_blocks/message_block.json']:
    with open(eg) as f:
      messageblock = json.load(f)
    get_message_block_type(messageblock)


def test_process_message_block():
    pass


def test_process_button_block():
    pass


def test_process_question_block():
    pass


def test_process_slider_block():
    pass


def test_process_list_block():
    pass


def test_process_media_block():
    pass