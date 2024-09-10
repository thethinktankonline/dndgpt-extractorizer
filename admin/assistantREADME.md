# OpenAI Assistant Readme

This script uses two (2) hyper specialized OpenAI GPT 4o Mini Assistants. 

Store each Assistant's ID in .env after they are created. 

# Assistant 1—Monster Assistant

This assistant's purpose in life is to look through the D&D SRD 5.1 which is connected to it via a Vector Store, with a guess or a name of what it is looking for, then to fully extract and pre-structure the information for the next step. 

Personally, I find it much easier to work with Assistants via https://platform.openai.com rather than programatically. 



## How to Build Assistant 1

1. Create a new Assistant on https://platform.openai.com. 
2. Copy and paste [dndgpt_monster_assistant_instructions.txt] (/admin/dndgpt_monster_assistant_instructions.txt) into the Assistant's System Instructions.
3. Upload the knowledge base to File Store, [dndgpt_srd_cc_v5.1_monstersatok.pdf] (/admin/dndgpt_srd_cc_v5.1_monsters_atok.pdf) and [dndgpt_srd_cc_v5.1_monsters_ltoz.pdf] (dndgpt_srd_cc_v5.1_monsters_ltoz.pdf).
4. Create a Vector Store from the files and attach it to the First Assistant.
5. Response Format: Text
6. I've been experimenting with Temperature = 0.5, and Top P = 0 to reduce variation in the response.
7. Record the Assistant ID and add it the .env file as DNDGPT_MONSTER_ASSISTANT_ID

## Notes on Assistant 1
Assistant 1 uses a Vector Store. Any version of the SRD 5.1 PDF, which is over 400 pages long, can be used. However, experimentation has shown that cutting down the size of the pdf to the section being searched, and futher cutting it into sub-sections [significantly reduce Tokens In. ](https://community.openai.com/t/the-dndgpt-case-study-for-you-and-me/745668/23?u=thinktank).

Using a guess with 4o Mini has proven accurate and cost-effective. 



# Assistant 2—Monster Assistant Structured Output

Assistant 2's whole job is to take the response from Assistant 1 it finds in the Thread, and structure the response so it can be put into the local CSV. 

It uses [response_format](https://platform.openai.com/docs/guides/structured-outputs/function-calling-vs-response-format), and is exceptionally accurate.

## How to Build Assistant 2
1. Create another new assistant.
2. Copy / Paste the [System Instructions](/admin/dndgpt-monster_assistant_structured_output_instructions.txt) provided.
3. Set Response Format: JSON Schema
4. Copy / Paste [the provided JSON Schema](/admin/dndgpt_spreadsheet_structured_response_schema.json) in the window OpeanAI provides.
5. Record the Assistant ID and add it to the .env file as DNDGPT_MONSTER_ASSISTANT_STRUCTURED_OUTPUT_ID.

## Notes on Assistant 2
Structured Output has proven wildly accurate. In 7 complete runs (so far) there have been zero issues with properly structuing the values of the response and assigning them to the appropriate column in the spreadsheet. The biggest challenge here has been variability in actual content, and the ocassional use of illegal characters. 

The latter has been solved by programatically normalizing the line before it is added to the spreadsheet. The former is detailed in "issues." 
