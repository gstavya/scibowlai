import streamlit as st
from openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate

client = OpenAI(
    api_key="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",
)

completion = client.chat.completions.create(
        model="ft:gpt-4o-mini-2024-07-18:personal::AykiQDzD",
        messages=[
            {"role": "developer", "content": "You ask Science Bowl questions. Science Bowl is a buzzer-based competition centered around speed and consisting of questions in five subjects: math, earth and space science, physics, chemistry, and biology. You write Science Bowl questions on a given topic. Each Science Bowl question consists of a toss-up, to be solved in under 5 seconds, and a bonus, to be done in under 20 seconds. Each toss-up and bonus must be either short answer (no answer choices) or multiple choice (4 choices given, designated with W, X, Y, and Z.."},
            {"role": "user", "content": f"Ask a Science Bowl question on Physics."}
        ]
)

question = completion.choices[0].message.content

print(question)