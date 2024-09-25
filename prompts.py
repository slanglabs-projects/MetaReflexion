JUDGE_PROMPT = """Your task is to assess the quality and effectiveness of AI responses across different tool types: query rewriter, router, and single-step tool.
Evaluate the response based on the following criteria, adapting your assessment to the specific tool type:

1. Relevance and Accuracy
2. Completeness and Level of Detail
3. Logical Reasoning and Coherence
4. Adherence to Instructions and Guidelines
5. Specificity and Actionability

For each tool type, focus on these specific aspects:

Query Rewriter:
- Query Continuation: Is it a logical continuation of the previous conversation?
- Query Refinement: How well does it use context or improve clarity?
- Response Accuracy: Does it accurately capture and refine the user's intent?

Router:
- Category Selection Explanation: Does the selected category align with the six predefined categories, and is it relevant to the user’s input? A good explanation should clarify if the chosen category is the best match based on the intent of the user’s query.
- Tool Selection Explanation: Is the tool selected the most effective and appropriate for resolving the user’s query? Evaluate if the chosen tool is not just correct, but optimal in terms of functionality and purpose.
- App Name Explanation: Assess whether the specified app is a valid provider within the selected category. The explanation should justify the app’s relevance based on the service it offers and whether it aligns with the category.
- Status Message Explanation: Does the status message communicate effectively in fewer than 10 words, clearly setting expectations for the user? The explanation should consider the clarity, brevity, and relevance of the message in guiding the user.
- Query Explanation: Focus on whether the user’s input was correctly interpreted, and whether the response accurately addressed the query.
- Overall Rating Explanation: Provide an expert evaluation of the response quality, considering the coherence of all components (category, tool, app, status, explanation), and whether they work together to offer an accurate and useful answer.
- Explanation Clarity: Is the response explanation clear, concise, and easy for the user to understand? The explanation should assess whether the response delivers the right information without unnecessary complexity.
- Improved Response Explanation: Does the suggested improved response provide more specificity and actionable steps? The explanation should focus on whether the enhancement makes the response more accurate, user-friendly, or better aligned with the user’s needs.

Single-Step Tool:
- Query: Was the user’s input properly interpreted, and does it directly guide the overall response?
- Overall Rating: Does it effectively and accurately address the user’s query?
- Single-Step Tool Explanation: Does the overall response maintain high quality by selecting appropriate tools and providing a coherent answer? Is there any room for improvement in the tool’s output or approach?
- Search Term Rating: If a search term was provided, how relevant and effective was it? If no search term is present, respond with "NA."
- Search Term Explanation: Is the chosen search term optimal? Does it capture the key aspects of the query and lead to accurate results? Analyze its strengths and weaknesses, suggesting improvements if needed.
- Suggestions Rating: How well do the suggestions align with the user’s needs? Are they useful, actionable, and tailored to the query?
- Suggestions Explanation: Does the explanation provide clear justifications for the ratings? Assess the quality, relevance, and practicality of the suggestions, identifying any gaps or strengths.
- Message Rating: Does it convey information effectively and with clarity?
- Message Explanation: Evaluate whether the message effectively communicates the intended content. Is it clear, concise, and easy for the end-user to understand?
- Improved Response: Does the improved version provide better accuracy, relevance, or actionable steps for the user?

Evaluation Process:
1. Analyze the input: Carefully review the user query, app_context, page_context, and any disambiguation_context provided.
2. Assess the response: Evaluate how well the AI assistant's response addresses the user's needs and adheres to the specific requirements of the tool type.
3. Consider e-commerce specifics: Keep in mind the Indian e-commerce context and the importance of product-specific terminology and categories.
4. Provide constructive feedback: Offer insights on strengths and areas for improvement.
5. Rate and explain: Assign a score out of 5 points and provide a detailed explanation for your evaluation.

Note: Don't be too less strict and too more stirct in your evaluation. If the outcome is correct, reasonable, and demonstrates clear logical thinking, give it a score of 5, even if the explanation is concise rather than extensive.

Your evaluation should include the total score out of 5 points, as well as an explanation justifying the score containing the strengths and weaknesses of the response. Think critically and consider all perspectives before providing your final evaluation. Ensure your assessment is thorough, fair, and provides valuable insights for improving the AI assistant's performance in the Indian e-commerce context.

Please respond with your evaluation in the following JSON format:

{
    "explanation": [an explanation justifying the score containing the strengths and weaknesses of the response after critical thinking and concise judgment],
    "score": [insert score out of 5 points]
}
"""


METAJUDGE_PROMPT = """you will be given a data like 
    UserQuestion:
    Response:
    Judgement A:
    Judgement B:
    Review the user's question and the corresponding response, along with two judgments.
    Determine which judgment is more accurate according to the rubric provided below. You SHOULD pick either of the two as the winner. The
    rubric used for the initial judgments is as follows:
    Your task is to assess the quality and effectiveness of AI responses across different tool types: query rewriter, router, and single-step tool.
Evaluate the response based on the following criteria, adapting your assessment to the specific tool type:

1. Relevance and Accuracy
2. Completeness and Level of Detail
3. Logical Reasoning and Coherence
4. Adherence to Instructions and Guidelines
5. Specificity and Actionability

For each tool type, focus on these specific aspects:

Query Rewriter:
- Query Continuation: Is it a logical continuation of the previous conversation?
- Query Refinement: How well does it use context or improve clarity?
- Response Accuracy: Does it accurately capture and refine the user's intent?

Router:
- Category Selection Explanation: Does the selected category align with the six predefined categories, and is it relevant to the user’s input? A good explanation should clarify if the chosen category is the best match based on the intent of the user’s query.
- Tool Selection Explanation: Is the tool selected the most effective and appropriate for resolving the user’s query? Evaluate if the chosen tool is not just correct, but optimal in terms of functionality and purpose.
- App Name Explanation: Assess whether the specified app is a valid provider within the selected category. The explanation should justify the app’s relevance based on the service it offers and whether it aligns with the category.
- Status Message Explanation: Does the status message communicate effectively in fewer than 10 words, clearly setting expectations for the user? The explanation should consider the clarity, brevity, and relevance of the message in guiding the user.
- Query Explanation: Focus on whether the user’s input was correctly interpreted, and whether the response accurately addressed the query.
- Overall Rating Explanation: Provide an expert evaluation of the response quality, considering the coherence of all components (category, tool, app, status, explanation), and whether they work together to offer an accurate and useful answer.
- Explanation Clarity: Is the response explanation clear, concise, and easy for the user to understand? The explanation should assess whether the response delivers the right information without unnecessary complexity.
- Improved Response Explanation: Does the suggested improved response provide more specificity and actionable steps? The explanation should focus on whether the enhancement makes the response more accurate, user-friendly, or better aligned with the user’s needs.

Single-Step Tool:
- Query: Was the user’s input properly interpreted, and does it directly guide the overall response?
- Overall Rating: Does it effectively and accurately address the user’s query?
- Single-Step Tool Explanation: Does the overall response maintain high quality by selecting appropriate tools and providing a coherent answer? Is there any room for improvement in the tool’s output or approach?
- Search Term Rating: If a search term was provided, how relevant and effective was it? If no search term is present, respond with "NA."
- Search Term Explanation: Is the chosen search term optimal? Does it capture the key aspects of the query and lead to accurate results? Analyze its strengths and weaknesses, suggesting improvements if needed.
- Suggestions Rating: How well do the suggestions align with the user’s needs? Are they useful, actionable, and tailored to the query?
- Suggestions Explanation: Does the explanation provide clear justifications for the ratings? Assess the quality, relevance, and practicality of the suggestions, identifying any gaps or strengths.
- Message Rating: Does it convey information effectively and with clarity?
- Message Explanation: Evaluate whether the message effectively communicates the intended content. Is it clear, concise, and easy for the end-user to understand?
- Improved Response: Does the improved version provide better accuracy, relevance, or actionable steps for the user?

Evaluation Process:
1. Analyze the input: Carefully review the user query, app_context, page_context, and any disambiguation_context provided.
2. Assess the response: Evaluate how well the AI assistant's response addresses the user's needs and adheres to the specific requirements of the tool type.
3. Consider e-commerce specifics: Keep in mind the Indian e-commerce context and the importance of product-specific terminology and categories.
4. Provide constructive feedback: Offer insights on strengths and areas for improvement.
5. Rate and explain: Assign a score out of 5 points and provide a detailed explanation for your evaluation.

Note: Don't be too strict nor too loose in your evaluation. If the outcome is correct, reasonable, and demonstrates clear logical thinking, give it a score of 5, even if the explanation is concise rather than extensive.

After examining the original question, response, and both judgments:
- Conclude with a clear statement of which judgment is better using the JSON format with the 3 fields, EITHER OF THE TWO SHOULD ONLY BE PICKED. :
"{
    judgement_a : [judgement_a]
    judgement_b : [judgement_b]
    winner : [winner of the both judgements "judgement_a" | "judgement_b" SHOULD ALWAYS BE EITHER 'judgement_a' or 'judgement_b']
}"
"""

IMPROVE_PROMPT = """Given:

A task provited by the user for which inference is to be made
A response(output) generated for that user query
A judgement on how that response(output) can be improved provided by a judge

Task: 
Analyze the judgement and use it to generate an improved response(output) that addresses the issues or feedback identified in the judgement.

Process:
Review the judgement and the task thoroughly and identify areas for improvement based on the two.
Adjust the scores in the output JSON that was generated accordingly and improve the explanations if needed.
Generate an improved response (THE FINAL JSON FOR THE USER'S QUERY WHICH HAS THE SAME FIELDS OF THE RESPONSE JSON) incorporating the changes.
Ensure the response is clear, concise, and addresses the feedback.

Return only the final improved response in a JSON format similar to the response generated (the output) by the LLM containing all the improvements made to the scores and the descriptions.
"""


SYS_PROMPT = """
Answer the User query with expert logical thinking and critical analysis think stepby step and process the given query, display the answer followed explanation containing the reason for the answer
return the response in a json format 
{
    query: [query asked by the user]
    response: [response generated]
}
"""