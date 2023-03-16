# -*- coding:utf-8 -*-
title = """<h1 align="center">▪◾◼⬛BlackBots ChatGPT⬛◼◾▪"""
description = """<div align=center>

Developed by © Cloud Bots™ BlackBots [Supreme100](https://instagram.com/erikrai.art)

Visit Black Botss [Webstore](https://black-bots.github.io) to download other useful tools.

This app uses `gpt-3.5-turbo` large language model
</div>
</div>
"""
customCSS = """
code {
    display: inline;
    white-space: break-spaces;
    border-radius: 6px;
    margin: 0 2px 0 2px;
    padding: .2em .4em .1em .4em;
    background-color: rgba(175,184,193,0.2);
}
pre code {
    display: block;
    white-space: pre;
    background-color: hsla(0, 0%, 0%, 72%);
    border: solid 5px var(--color-border-primary) !important;
    border-radius: 10px;
    padding: 0 1.2rem 1.2rem;
    margin-top: 1em !important;
    color: #FFF;
    box-shadow: inset 0px 8px 16px hsla(0, 0%, 0%, .2)
}

*{
    transition: all 0.6s;
}


"""

summarize_prompt = "Please summarize the above conversation, no more than 100 words." # The prompt when summarizing the conversation
MODELS = ["gpt-3.5-turbo", "gpt-3.5-turbo-0301", "gpt-4","gpt-4-0314", "gpt-4-32k", "gpt-4-32k-0314"] # 可选的模型
websearch_prompt = """Web search results:

{web_results}
Current date: {current_date}

Instructions: Using the provided web search results, write a comprehensive reply to the given query. Make sure to cite results using [[number](URL)] notation after the reference. If the provided search results refer to multiple subjects with the same name, write separate answers for each subject.
Query: {query}
Reply in English"""

# 错误信息
standard_error_msg = "☹️An error occurred:" # Standard prefix for error messages
error_retrieve_prompt = "The connection timed out, unable to retrieve the conversation. Please check the network connection, or whether the API-Key is valid." # An error occurred while retrieving the conversation
connection_timeout_prompt = "The connection timed out, unable to get the conversation." # Connection timed out
read_timeout_prompt = "Read timed out, unable to get conversation." # Read timeout
proxy_error_prompt = "Proxy error, unable to get conversation." # Proxy error
ssl_error_prompt = "SSL error, unable to fetch session." # SSL error
no_apikey_msg = "The length of the API key is not 51 digits, please check whether the input is correct." # The length of the API key is less than 51 digits
max_token_streaming = 3600 # Maximum number of tokens for streaming conversations
timeout_streaming = 15 # Timeout for streaming conversations
max_token_all = 3600# Maximum number of tokens for non-streaming conversations
timeout_all = 200 # Timeout for non-streaming conversations
enable_streaming_option = True # Whether to enable the check box to choose whether to display the answer in real time
HIDE_MY_KEY = True # Set this value to True if you want to hide your API key in UI
