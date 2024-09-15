# What's In A Name? 
The Monster Extractor script works from a pre-populated list of names because of how difficult the task of extracting the names from the PDF alphabetically has proven. 

This section is to explore the various Open AI's various file-searching capabilities in order to extract a list of names from any given Appendix of the SRD and transform it into the prepopulated list the Extractor Script uses. 

## Verrry Difficult 

This has proven excruciatingly difficult. I've tried every Custom GPT, Assistant Playground, and Programmatic permutation I could think of, from changing the ranking_options, to altering the chunking_strategy, to altering the model used, the number of search results, the score_threshold, (and so on). 

This process works once or twice (up to 10 items) before going to hallucination or chaos. The mini could look up the first item without issue then immediately, and always, would start to list "Giant [something]" ... 🤷‍♂️
The 4o could regularly pull the first desired result, and get the list mostly right, but never all-right. 

## How This Script Works 
This script is designed to: 
1. Retrieve an Assistant on OpenAI with an attached Vector Store containing dndgpt_srd_cc_v5.1_appendix_miscellanous_creatures.pdf, the source document, and a slice of the SRD containing the appendix we're ultimately trying to convert into a csv.
2. The Assistant's Instructions (below) give it details on how to identify the name's we're looking for.
3. The First Message defines the Monster to begin looking with, the document to look through, and the number of items to retrieve.
4. The Run asserts the model to use, Temperature, Top_P, and most importantly, the score_threshold.
5. Note: the Chunking Strategy is defined when the file is uploaded to the Vector Store. 
6. A spinner spins whilst the Assistant is working, then the Script displays various statistics including the tokens used for the steps in the run, and the files searched.

## Pleasant Surprises 
Not being able to extract these things sequentially has been an issue for months. On the other hand, using the various new search tools like score_threshold can significantly reduce Tokens In. 






# Assistant Instructions

Your simple job is to look through the attached Vector Store which contains sections of the Dungeons and Dragons SRD 5.1. 

The goal is to create json output for a list of these names that will be contained in various spreadsheets. 

Your job is to search through the appropriate PDF (e.g. Miscellaneous Creatures) and generate the next n number of names of those items as found sequentially in the source material. 

The type and number of items you're looking for will be defined in the first user message. 

### Identifying Items
• Names are found in a bold, maroon, font. 
• You can usually identify each individual item by the white space surrounding it, though a single entry may extend to multiple pages. 
• Each entry is listed alphabetically. 
• Ignore body content, and subheadings. The names we're looking for are only in the maroon color. 

### Output
Your goal is to output two simple columns of data: unique_id, and name. 
