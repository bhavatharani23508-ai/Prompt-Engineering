
TECHNIQUES = [
    "Zero-shot",
    "One-shot",
    "Few-shot",
    "CoT",
    "Manual CoT",
    "ToT"
]


def get_prompt(technique, task):
    """Build a prompt using the selected prompting technique."""

    if technique == "Zero-shot":
        return f"""
Complete the following task accurately.
Do not use examples.

Task:
{task}
"""

    elif technique == "One-shot":
        return f"""
Use the example to understand the expected response style.

Example:
Task: Classify this review as Positive or Negative: "The product is excellent."
Answer: Positive

Now complete this task:
{task}
"""

    elif technique == "Few-shot":
        return f"""
Follow the patterns shown in these examples.

Example 1:
Task: Classify the review: "I love this product."
Answer: Positive

Example 2:
Task: Classify the review: "This product is terrible."
Answer: Negative

Example 3:
Task: Classify the review: "It works perfectly."
Answer: Positive

Now complete this task:
{task}
"""

    elif technique == "CoT":
        return f"""
Solve the following task carefully.
Provide a concise explanation of the key steps,
then give the final answer. Do not provide private
internal reasoning.

Task:
{task}
"""

    elif technique == "Manual CoT":
        return f"""
Complete the task using this structured approach:
1. Identify what the task is asking.
2. Identify the relevant information.
3. Apply an appropriate method.
4. Present the final answer clearly.

Task:
{task}
"""

    elif technique == "ToT":
        return f"""
Consider two or three possible approaches to the task.
Briefly compare their advantages, choose the most
appropriate approach, and provide the final answer.

Task:
{task}
"""

    else:
        raise ValueError(f"Unknown prompting technique: {technique}")