from groq import Groq
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import AIMessage, HumanMessage

os.environ["GROQ_API_KEY"] = "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"
os.environ["OPENAI_API_KEY"] = "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"

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

llm = ChatOpenAI(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    model_name="gpt-4o-2024-11-20"
    )

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You generate AMC 12 questions. The AMC 12 helps students develop their problem-solving abilities and serves as the first step in qualifying for prestigious international mathematics competitions, including the USA International Mathematical Olympiad. Description: The AMC 12 is a 25-question, 75-minute multiple-choice competition designed for students in grades 12 and below. It covers the full high school mathematics curriculum, including trigonometry, advanced algebra, and advanced geometry. Calculus is excluded. All questions have numerical (not word-based) answers. No proofs."
        ),
        ("user", "{input}"),
    ]
)


chain = prompt | llm
result = chain.invoke(
    {
        "input": """

Generate an AMC 12-style, hard, combinatorics problem involving balls and bins. It should involve significant creative thinking.

        """
    }
)

print(result.content)

# question = """

# A particle of mass m moves in the xy plane with potential energy
# U(x, y) = -k(x^2+y^2)/2
# The closest point to the origin (x = 0, y = 0) during its motion was at a distance d, and the particle's speed at that point was v0. Which of the following statements is true regarding the path of the particle after a long time t (t >> d/v)?
# (A) The particle's trajectory will be circular.
# (B) The particle's trajectory will be asymptotic to a straight line pointing away from the origin.
# (C) The particle will spiral outwards away from the origin.
# (D) The particle will travel on a parabolic trajectory.
# (E) The particle will spiral inwards towards the origin.
# """

def generate():
        # prompt = f"""

        # The AMC 12 helps students develop their problem-solving abilities and serves as the first step in qualifying for prestigious international mathematics competitions, including the USA International Mathematical Olympiad. Description: The AMC 12 is a 25-question, 75-minute multiple-choice competition designed for students in grades 12 and below. It covers the full high school mathematics curriculum, including trigonometry, advanced algebra, and advanced geometry. Calculus is excluded. All questions have numerical (not word-based) answers. No proofs.

        # Create your own medium-difficulty, yet creative AMC 12 problem involving a clever probability problem involving placing balls in different bins. Solve your generated question and then output just the question and then the answer. Ensure that the answer is no bigger than 1,000.

        # """

        prompt = f"""

Generate an AMC 12-style, clever combinatorics problem that involves putting balls into bins. The solution must not be immediately obvious and it should require a lot of creative thinking.
        """

        # prompt = f"""

        # This is a question: {question}.

        # Don't output a solution or answer to the question. s
        
        # Simply output 4-5 techniques needed to solve the problem, without explaining them in the context of the problem. Just the topic that's it. Don't end your output with an answer. Just the 4-5 topics. Each topic listed should be no more than 2-3 words. No further explanation for each topic. Each topic should be one line. Short.

        # After outputting the topics, give a super generic sentence summary of the ideation behind the problem. No specifics, just a brief description of the motivaiton behind the problem.

        # """

        # prompt = f"""

        # Solve this equation:

        # x = (log 5)^3 + (log 20)^3 + (log 8)(log 0.25)

        # """

        # prompt = """

        # Solve this:

        # Two players take turns flipping a fair coin, starting with Player A. The first player to flip two heads in a row wins. What is the probability that Player A wins?

        # """

        # prompt = """

        # The F=ma exam is a 75-minute exam with 25 multiple choice questions focusing on mechanics.

        # Generate a moderate-difficulty question for the F=ma involving these topics:

        # 1. Potential Energy Analysis
        # 2. Force Calculation
        # 3. Equations of Motion
        # 4. Energy Conservation
        # 5. Trajectory Analysis

        # The problem involves understanding the long-term behavior of a particle in a specific potential, requiring analysis of forces, energy, and motion equations to determine the trajectory over time.

        # Output the multiple-choice question and the answer. Both the multiple-choice question and the answer. That's it!

        # """


        chat = client.chat.completions.create(
        messages=[
        {
            "role": "user",
            "content": prompt,
        }
        ],
        model="qwen-2.5-coder-32b",
        )

        return chat.choices[0].message.content

# def find_topics(question):
#         prompt = f"""

#         This is a question: {question}.

#         The question you are given is a relatively easy question. Don't act like it's hard or overcomplicate it.

#         Don't output a solution or answer to the question.
        
#         Simply output 4-5 techniques needed to solve the problem, without explaining them in the context of the problem. Just the topic that's it. Don't end your output with an answer. Just the 4-5 topics. Each topic listed should be super specific.

#         After outputting the topics, give a super generic sentence summary of the ideation behind the problem. No specifics, just a brief description of the motivaiton behind the problem.

#         """

#         chat = client.chat.completions.create(
#         messages=[
#         {
#             "role": "user",
#             "content": prompt,
#         }
#         ],
#         model="llama-3.3-70b-versatile",
#         )

#         return chat.choices[0].message.content

# amc_questions = ["The product of three integers is $60$. What is the least possible positive sum of the three integers?", "In $\Delta ABC$, $\angle ABC = 90^\circ$ and $BA = BC = \sqrt{2}$. Points $P_1, P_2, \dots, P_{2024}$ lie on hypotenuse $\overline{AC}$ so that $AP_1= P_1P_2 = P_2P_3 = \dots = P_{2023}P_{2024} = P_{2024}C$. What is the length of the vector sum\[\overrightarrow{BP_1} + \overrightarrow{BP_2} + \overrightarrow{BP_3} + \dots + \overrightarrow{BP_{2024}}?\]", "How many angles $\theta$ with $0\le\theta\le2\pi$ satisfy $\log(\sin(3\theta))+\log(\cos(2\theta))=0$?", "Let $M$ be the greatest integer such that both $M + 1213$ and $M + 3773$ are perfect squares. What is the units digit of $M$?", "Let $\alpha$ be the radian measure of the smallest angle in a $3{-}4{-}5$ right triangle. Let $\beta$ be the radian measure of the smallest angle in a $7{-}24{-}25$ right triangle. In terms of $\alpha$, what is $\beta$?"]

# for i in range(len(amc_questions)):
#     topics = find_topics(amc_questions[i])
#     print("**TOPICS**")
#     print(topics)
#     print("**TOPICS**")
#     prompt = f"""

#         The AMC 12 helps students develop their problem-solving abilities and serves as the first step in qualifying for prestigious international mathematics competitions, including the USA International Mathematical Olympiad. Description: The AMC 12 is a 25-question, 75-minute multiple-choice competition designed for students in grades 12 and below. It covers the full high school mathematics curriculum, including trigonometry, advanced algebra, and advanced geometry. Calculus is excluded. All questions have numerical (not word-based) answers. No proofs.

#         THERE IS NO CALCULATOR ALLOWED ON THE AMC 12.

#         Create your own moderate-difficulty problem on the AMC 12 that would require the following topics in order to solve it:

#         {topics}

#         Solve your generated question and then output just the question and then the answer.

#         Remember that all AMC 12 problems are multiple-choice, Calculus is excluded. All questions have numerical (not word-based) answers. No proofs.

#         Remember that this problem should be of moderate difficulty. This is a #1-5 question.

#         """
#     index = 0
#     result = generate(prompt)
#     for i in range(len(result)):
#       if(result[i:i+8]=="</think>"):
#         index = i+9
#     print(f"Problem {i+1}")
#     print(result[index:])

# def solve(question):
#     prompt = f"""

#     Solve this question: {question}.

#     If the question or answer does not make sense, feel free to change it. The question may be wrong a decent amount of the time. Make sure to explicitly state the problem and the answer at the end, once you are done.

#     """

#     chat = client.chat.completions.create(
#         messages=[
#         {
#             "role": "user",
#             "content": prompt,
#         }
#         ],
#         model="deepseek-r1-distill-llama-70b",
#         )

#     return chat.choices[0].message.content


# question = generate()
# print(question)
# print(solve(question))