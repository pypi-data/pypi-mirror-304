import re

def convert_to_whatsapp_markdown(markdown_text):
    markdown_text = re.sub(r'(?<!\\)_(.*?)_', r'_\1_', markdown_text)
    
    markdown_text = re.sub(r'\*\*(.*?)\*\*', r'*\1*', markdown_text)
    
    markdown_text = re.sub(r'~~(.*?)~~', r'~\1~', markdown_text)
    
    markdown_text = re.sub(r'```(.*?)```', r'```\1```', markdown_text, flags=re.DOTALL)
    
    markdown_text = re.sub(r'(?m)^(\s*)- (.*?)$', r'\1* \2', markdown_text)
    markdown_text = re.sub(r'(?m)^(\s*)\* (.*?)$', r'\1* \2', markdown_text)
    
    markdown_text = re.sub(r'(?m)^(\d+)\. (.*?)$', r'\1. \2', markdown_text)
    
    markdown_text = re.sub(r'(?m)^> (.*?)$', r'> \1', markdown_text)
    
    markdown_text = re.sub(r'`(.*?)`', r'`\1`', markdown_text)
    
    return markdown_text