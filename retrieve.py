# with open('./chem.txt', 'r', encoding='utf-8') as file:
#     text_content = file.read()

# while "**Category**" in text_content and "**Raw Question**" in text_content:
#     index1 = text_content.find("**Category**")
#     index2 = text_content.find("**Raw Question**") + len("**Category**")
#     text_content = text_content[:index1] + text_content[index2:]

# while "<think>" in text_content and "</think>" in text_content:
#     index1 = text_content.find("<think>")
#     index2 = text_content.find("</think>") + len("<think>")
#     text_content = text_content[:index1] + text_content[index2:]

# with open("chem.txt", "w", encoding='utf-8') as f:
#     f.write(text_content)
