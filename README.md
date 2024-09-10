![dndgpt_logo_extractorizer_full](https://github.com/user-attachments/assets/7643834e-a7fd-4a29-bee6-9535bf264e27)
# dndgpt-extractorizer
This is my first repository! It includes various tools for using multiple OpenAI Assistants to change sections of the open source Dungeons and Dragons SRD 5.1 PDF into structured data. 
Please let me know if there's anything I can do to better align with best practices. 

Imma noob, most of this code was written with ChatGPT. 😅

# Purpose
The purpose of this simple script is to be a learning device to better understand how to code, and how use AI. It uses open source data, and is offered under the same creative commons liscence as that data, so that everyone can have an opportunity to learn using the same (fun) data source. 

It uses a multi-Assistant flow to transfer the information from the alphabetically listed monsters in the SRD 5.1 into a csv. 

Finally, the CSV is to be used to help condense the [dndGPT, a customGPT on ChatGPT,](https://chatgpt.com/g/g-wIndOtOwd-dndgpt) knowledge base—which is limited to 20 files. 🤷‍♂️ But, a cGPT can make far more accurate lookups with the structured data vs using this extraction method; learn more from the [case study on the openai developer forum.](https://community.openai.com/t/the-dndgpt-case-study-for-you-and-me/) 

# Prerequisites
- This script requires roughly $1.00 USD worth of API calls to OpenAI's GPT 4o mini.
- It uses two (2) different Assistants. The System Instructions, and the JSON schema for these Assistants can be found in the Admin folder of this Repository. 
- The script requires a pre-populated list of the names to search, which is provided, as dndgpt_monsters.csv, and dndgpt_monsters_starter.csv. See "Issues" for more information. 

# How it Works
1. This script starts a few timers (for later analysis) and a kill switch if you want to exit or there's an error. 
2. It looks up the next empty row of the spreadsheet, and returns the monster_name, unique_id, and monster_parent fields which are used throughout the process to standardize the final results.
3. It creates an OpenAI Client then calls two premade, specialized OpenAI Assistants, all whose ids are stored in .env.
4. Both Assistants work on the same Thread. Results are displayed in the terminal, mostly to reassure that "it's working." 
  1. dnd_gpt_monster_assistant — Has vector store with the PDF being searched. This Assistant performs the intital search, retrieval, and pre-structuring of the data.
  2. dnd_gpt_monster_assistant_structured_output — Takes the response from Assistant 1 and structures it according to the specified json.
5. The script takes the final response, normalizes it to remove any illegal characters, changes it to a python dictionary, then appends it to the appropriate row of the CSV.
6. The script *should* terminate automatically. It takes roughly 90 minutes to run, and costs a whopping $0.84 cents. 

# Analytics
The structured output with normalization is exceptionally accurate at making sure the schema is properly followed. However, there are still variations in the actual content.

* simple_comparisson.py — The purpose of this script is to compare two different runs to see how different they are, and what is different. Ultimately I want to build a way to merge all of the files together to triage a 99.9% document which is accurate to the source.

# Resources
This project was very much supported by a variety of different resources. 
* [The Dungeons and Dragon's SRD] ([https://media.wizards.com/2023/downloads/dnd/SRD_CC_v5.1.pdf](https://www.dndbeyond.com/resources/1781-systems-reference-document-srd)
* The OpenAI Docs, Cookbook, and 
* [Linkedin Learning (Which is where the spinner came from) amongst other things.] (https://www.linkedin.com/learning/openai-api-building-assistants/)
* [The Python CustomGPT] (https://chatgpt.com/g/g-cKXjWStaE-python)
