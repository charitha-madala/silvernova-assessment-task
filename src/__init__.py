import logging
from src.operations.ask import LLMAsker
from src.operations.search import SearchEngine
from src.operations.embed import EmbedService
from src.operations.extract import MarkdownExtractor
from src.tests import Tester 
import argparse
from pathlib import Path

class App:
  """ The main class of the application. """

  def __init__(self):
    self.markdown_extractor = MarkdownExtractor(input_dir="./documents", output_dir="./output")
    self.embed = EmbedService('embedded_doc.json')
    self.llm_asker = LLMAsker()
    self.search_engine = SearchEngine()
    self.tester = None
  

  def run(self):
    parser = argparse.ArgumentParser(description='Ask questions about the files of a case.')
    
    # Add optional "mode" argument (with values "load-files" and "ask-question" (default))
    parser.add_argument('--mode', choices=['load-files', 'ask-question', 'search', 'get-markdown', 'test'], default='ask-question', help='The mode of the application.')

    # Add question argument as required positional argument if mode is "ask-question"
    parser.add_argument('question', nargs='?', type=str, help='The question to ask about the files of a case.', default = 'Where is ABC Innovations GmbH located?')

    args = parser.parse_args()

    if args.mode == 'load-files':
      self.load_files()
    elif args.mode == 'ask-question':
      question = args.question
      if not question or question.isspace():
        parser.error('The question argument is required in "ask-question" mode.')
      self.ask_question(question)
    elif args.mode == 'search':
      question = args.question
      if not question or question.isspace():
        parser.error('The query argument is required in "search" mode.')
      self.search(question)
    elif args.mode == 'get-markdown':
      self.get_markdown()
    elif args.mode == 'test':
      self.test_accuracy()

  def load_files(self):
    # ToDo: Load the files and index them in a db of your choosing for the rag
    
    output_dir = Path('output')
    for file in output_dir.iterdir():  
      if file.is_file():
        try:
          with open(file, "r", encoding="utf-8") as md_file:
              file_content = md_file.read()
              # Store file metadata with the chunks
              metadata = {"filename": file.name, "source_path": str(file)}
              self.embed.embed_and_store(file_content, metadata)
        except Exception as e:
          print(f"Error processing '{file}': {e}")               


  def search(self, query):
    response = self.search_engine.search_similar(query, 5)
    return response

  def get_markdown(self):
    self.markdown_extractor.process_directory()

  def ask_question(self, question):
    
    logging.info(f'Asking question: {question}')

    operator = LLMAsker()

    response = operator.ask(question)

    print(response)
  
  def test_accuracy(self):
    """Run the accuracy test using the tester module"""
    if self.tester is None:
        def asker_function(question):
            return self.llm_asker.ask(question)       
      
        self.tester = Tester()
        
        self.tester.test_rag_accuracy = asker_function
        
    self.tester.run(self.tester.questions)
    print("Testing completed.")