# Prompt Engineering Assignment

## Tools Used
- **Claude Code** - AI-powered coding assistant by Anthropic
- **Google Gemini API** - Using the `google-genai` Python SDK (newer unified SDK)

---

## Initial Prompt to Claude Code

```
I have a coding assignment about prompt engineering that has three task. Here is the raw text of the assignment description:
```
Practice Prompt engineering in Python to complete the following tasks:
1. Prompt Chaining for a Customer Support AI
Goal: Build a simple prompt chain to simulate a customer service flow
2. Code Generation with ReACT Prompting
Goal: Generate Python code using reasoning before execution.
3. Self-Reflection Prompt for Improving Output
Goal: Ask the AI to critique and improve its summary.

Submission:
A document including:
1. The tools and prompts you used for each coding exercise
2. The GitHub links to your Python code as 3 separate Colab files with the successful output.
```

Here is what you need to accomplish:
- Finish each task as described in the assignment description. Start by asking clarifying questions, if any exist. Then, proceed with creating an execution plan, which I will approve or reject.
- At each prompting stage (including this one), document the prompt in the README.md in the /prompt_engineering directory. The README.md should document claude code as the tool used and all prompts while accomplishing this assignment.
- I have already created the /prompt_engineering directory as well as ipynb files for part 1-3 and the README.md. Complete those files in their respective places.
- Do any necessary web searches on prompt engineering techniques to clarify your understanding.
- To complete the prompt engineering tasks for this assignemnt, use the python google genai sdk (https://ai.google.dev/gemini-api/docs/quickstart). I have the GEMINI_API_KEY in the .env file, and the google-genai dependency has already been installed.
```

**Response**: Claude Code performed web research on prompt chaining, ReACT prompting, and self-reflection techniques, then created an execution plan that was approved.

---

## Task 1: Prompt Chaining for Customer Support AI

### Technique Overview
Prompt chaining breaks down a complex task into a series of smaller, sequential prompts where the output of one prompt becomes the input for the next. This improves transparency, controllability, and reliability of LLM applications.

### Implementation Approach
Create a 4-step chain for tech support:
1. **Intent Classification** - Identify the type of customer issue
2. **Information Gathering** - Extract relevant details from the query
3. **Solution Generation** - Create a tailored solution based on the issue
4. **Response Formatting** - Format as a professional customer service response

### Prompts Used

#### Prompt 1: Intent Classification
```
You are a customer support intent classifier. Analyze the following customer message and classify it into one of these categories: Technical Issue, Billing Question, Feature Request, Account Access, or General Inquiry.

Customer Message: {customer_message}

Respond with ONLY the category name.
```

#### Prompt 2: Information Gathering
```
Based on the customer message below and its classified intent, extract the key information needed to resolve this issue. List the specific details mentioned and any missing information that should be asked.

Intent: {intent}
Customer Message: {customer_message}

Provide a structured summary of:
1. Key details mentioned
2. Missing information needed
```

#### Prompt 3: Solution Generation
```
Generate a solution for this customer support case:

Intent: {intent}
Customer Message: {customer_message}
Key Information: {extracted_info}

Provide a clear, step-by-step solution or answer to address the customer's needs.
```

#### Prompt 4: Response Formatting
```
Format the following solution as a professional, empathetic customer support response:

Customer Issue: {customer_message}
Solution: {solution}

Create a complete response that:
- Acknowledges the customer's concern
- Provides the solution clearly
- Offers additional help
- Maintains a professional and friendly tone
```

---

## Task 2: Code Generation with ReACT Prompting

### Technique Overview
ReACT (Reasoning + Acting) prompting combines reasoning traces with task-specific actions. The LLM generates thoughts about the problem, then takes actions (like generating code), creating an interpretable chain of reasoning and execution.

### Implementation Approach
Generate Python code for data analysis using explicit Thought ’ Action ’ Observation cycles.

### Prompts Used

#### ReACT Prompt for Code Generation
```
You are a Python coding assistant using the ReACT framework (Reasoning + Acting). Generate code to analyze a CSV dataset containing sales data with columns: date, product, quantity, price.

Use this format:
Thought: [Your reasoning about what needs to be done]
Action: [The code you will write]
Observation: [What this code accomplishes]

Continue this pattern until you have complete code that:
1. Loads the CSV file
2. Calculates total revenue
3. Finds the best-selling product
4. Creates a simple visualization

After each Thought-Action-Observation cycle, move to the next step.
```

---

## Task 3: Self-Reflection Prompt for Improving Output

### Technique Overview
Self-reflection (Reflexion) enables AI to iteratively critique and improve its own outputs. The model acts as both creator and critic, using self-generated feedback to refine responses for better quality.

### Implementation Approach
Two-step process:
1. Generate an initial summary of a technical concept
2. Critique the summary and generate an improved version

### Prompts Used

#### Prompt 1: Initial Summary Generation
```
Summarize the concept of "API Rate Limiting" in 3-4 sentences. Explain what it is, why it's important, and how it works.
```

#### Prompt 2: Self-Critique and Improvement
```
Review the following summary and critique it based on these criteria:
1. Clarity - Is it easy to understand?
2. Completeness - Does it cover all key aspects?
3. Accuracy - Is the information correct?
4. Conciseness - Is it appropriately brief without losing important details?

Original Summary:
{original_summary}

Provide:
1. A critique identifying specific strengths and weaknesses
2. An improved version of the summary that addresses the weaknesses

Format your response as:
CRITIQUE:
[Your detailed critique]

IMPROVED SUMMARY:
[Your enhanced version]
```

---

## Files
- `part1.ipynb` - Prompt Chaining implementation
- `part2.ipynb` - ReACT Prompting implementation
- `part3.ipynb` - Self-Reflection implementation

## Results
All notebooks execute successfully with the Gemini API and demonstrate the respective prompt engineering techniques.
