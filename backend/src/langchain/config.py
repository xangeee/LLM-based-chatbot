PAPER_AGENT_PROMPT="hwchase17/openai-functions-agent"
AGENT_CHAT_MODEL="gpt-3.5-turbo-1106"
OPENAI_MODEL="gpt-3.5-turbo-0125"

paper_template = """Your job is to use the ML research paper dataset
to answer questions about a specific paper. Use the following context to answer questions.
Be as detailed as possible, but don't make up any information
that's not from the context. If you don't know an answer, say
you don't know.

{context}
"""

TOOL_PAPER="""Useful when you need to answer questions
                about Machine Learning and Deep Learning Research Papers.
                Not useful for answering generic questions.
                Pass the entire question as input to the tool. For instance,
                if the question is "Can you provide a summary of the paper titled 'Attention is All You Need' and its impact on the field?",
                the input should be "Can you provide a summary of the paper titled 'Attention is All You Need' and its impact on the field?"
                """
                
TOOL_CITY="""Use when asked about the temperature of a specific city. This tool can only get the current
                temperature for non US cities. This tool returns temperature in
                centigrade. Do not pass the word "city" as input,
                only the city name itself. For instance, if the question is
                "What is the temperature in Barcelona?", the input should be "Barcelona".
                """