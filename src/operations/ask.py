from src.api import execute_prompt
from src.operations.search import SearchEngine


class LLMAsker:

  def __init__(self):
    self.search = SearchEngine()

  def ask(self, question: str) -> str:
    print('Thinking...')
    response = self.prepare_response(question)

    return response
  
  def prepare_response(self, question):
    """Find relevant documents, construct a prompt, and generate an LLM response."""
    print("Searching for relevant information...")

    search_results = self.search.search_similar(question, limit=5)

    if not search_results:
        return "Sorry, I couldn't find relevant information in the document database."
       
    context_snippets = []
    for doc in search_results:
        snippet = doc["content"][:700] 
        context_snippets.append(f"Document ID: {doc['id']}\nSnippet: {snippet}\n")

    context = "\n\n".join(context_snippets)

    prompt = f"""
    ### Role:
      You are an advanced AI legal assistant that provides precise, well-supported, and source-backed answers based on legal documents. Your responses must:
      - **Be Fact-Based**: Only use the provided document excerpts.
      - **Include Citations**: Point to the specific document and paragraph where the information is found.
      - **Ensure Legal Accuracy**: Avoid assumptions; if the answer is unclear, state it explicitly.
      - **Improve Understanding**: Ask clarifying questions before finalizing an answer.

      ---

      ### **User Query:**
      {question}

      ---

      ### **Step 1: Retrieve Relevant Context**
      The following are the most relevant excerpts retrieved from the document database:

      {context}

      ### **Step 2: Generate a Response**
      Structure your response as follows:

      **Answer:**  
      Provide a direct, well-structured response based on the document context.  

      **Source(s):**  
      List the document(s) used, including the **section, paragraph, or sentence number** if available. 
      
      Example:  
      - *Convertible Loan Agreement (CLA)*, Section 3.2: "If a Qualified Financing Round occurs before the Maturity Date, the Loan shall be converted into equity at a 20% discount."  
      - *Non-Disclosure Agreement (NDA)*, Clause 1.1.3: "Marketing strategies and financial projections are considered confidential information."  
      ---

      ### **Important Notes**
      - If no relevant information is found, clearly state: "The provided documents do not contain explicit details on this topic."
      - Always prioritize **clarity, legal accuracy, and document-based citations** in your response.

    """

    print("Generating response...")

  
    response = execute_prompt(prompt)

    return response.get("response", "Sorry, I couldn't generate a response.")
