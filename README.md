# dndgpt-extractorizer
This is my first repository! It includes various tools for using multiple OpenAI Assistants to change sections of the open source Dungeons and Dragons SRD 5.1 PDF into structured data. 
Please let me know if there's anything I can do to better align with best practices. 

# Purpose
The purpose of this simple script is to be a learning device to better understand how to use AI. It uses open source data, and is offered under the same creative commons liscence as that data, so that everyone can have an opportunity to learn using the same (fun) data source. 

It uses a multi-Assistant flow to transfer the information from the alphabetically listed monsters in the SRD 5.1 into a csv. 

Finally, the CSV is to be used to help condense the [dndGPT, a customGPT on ChatGPT,](https://chatgpt.com/g/g-wIndOtOwd-dndgpt) knowledge base—which is limited to 20 files. 🤷‍♂️ But, a cGPT can make far more accurate lookups with the structured data vs using this extraction method; learn more from the [case study on the openai developer forum.](https://community.openai.com/t/the-dndgpt-case-study-for-you-and-me/) 

# Prerequisites
- This script requires roughly $1.00 USD worth of API calls to OpenAI's GPT 4o mini.
- It uses two (2) different Assistants. The System Instructions, and the JSON schema for these Assistants can be found in the Admin folder of this Repository. 
  1. dnd_gpt_monster_assistant — Has vector store with the PDF being searched. This Assistant performs the intital search, retrieval, and pre-structuring of the data.
  2. dnd_gpt_monster_assistant_structured_output — Takes the response from Assistant 1 and structures it according to the specified json.
- The script requires a pre-populated list of the names to search, which is provided, as dndgpt_monsters.csv, and dndgpt_monsters_starter.csv. See "Issues" for more information. 
