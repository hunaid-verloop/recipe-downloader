from recipe_processor import *
import json
import pytest

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


#################################################Test for MessageBlock##############################################
@pytest.mark.skip
def test_process_message_block():
  with open('./example_blocks/message_block.json') as f:
    msgblock = json.load(f)
  with open('./transformed_blocks/messageblock_transformed.json', 'w') as o:
    o.write(json.dumps(process_message_block("Message 1", msgblock)))


#################################################Test for MediaBlock##############################################
@pytest.mark.skip
def test_process_media_block():
  with open('./example_blocks/media_block.json') as f:
    mediablock = json.load(f)
  with open('./transformed_blocks/mediablock_transformed.json', 'w') as o:
    o.write(json.dumps(process_media_block_todo("Media 1", mediablock)))


#################################################Test for ButtonBlock##############################################
@pytest.mark.skip
def test_process_button_block():
  with open('./example_blocks/button_block.json') as f:
    buttonblock = json.load(f)
  with open('./transformed_blocks/buttonblock_transformed.json', 'w') as o:
    o.write(json.dumps(process_button_block_todo("Button 1", buttonblock)))


#################################################Test for QuestionBlock##############################################
@pytest.mark.skip
def test_process_question_block():
  with open('./example_blocks/question_block.json') as f:
    questionblock = json.load(f)
  with open('./transformed_blocks/questionblock_transformed.json', 'w') as o:
    o.write(json.dumps(process_question_block_todo("Question 1", questionblock)))


#################################################Test for SliderBlock##############################################
@pytest.mark.skip
def test_process_slider_block():
  with open('./example_blocks/slider_block.json') as f:
    sliderblock = json.load(f)
  with open('./transformed_blocks/sliderblock_transformed.json', 'w') as o:
    o.write(json.dumps(process_slider_block_todo("Slider 1", sliderblock)))


#################################################Test for ListBlock##############################################
@pytest.mark.skip
def test_process_list_block():
  with open('./example_blocks/list_block.json') as f:
    listblock = json.load(f)
  with open('./transformed_blocks/listblock_transformed.json', 'w') as o:
    o.write(json.dumps(process_list_block_todo("List 1", listblock)))
