
class Tester:
    def __init__(self):
        # Example set of questions and corresponding correct answers
        self.questions = [
            "Welche Energiepreise sind im Dokument aufgeführt und wie sind sie strukturiert (z. B. Grundpreis, Preis pro kWh",
            "When did ABC Innovations GmbH and XYZ Solutions Ltd. enter a mutual non-disclosure agreement",
            "Where is ABC Innovations GmbH located?",
            "Which companies entered the Convertible Loan Agreement on 15 feb 2025?",
            "What is the decided intrest rate on the Convertible Loan Agreement?,3. Improve Product Quality",
            "What are the objectives of the yearly high-level OKRs"
        ]

        # Ground truth answers (correct answers)
        self.ground_truth_answers = [
            "Energiepreise: Arbeitspreis 43,61 Cent/kWh, Grundpreis 97,88 Euro/Jahr, Messpreis 10,00 Euro/Jahr (Nettopreise, zzgl. Umsatzsteuer).",
            "15 feb 2025",
            "Hauptstraße 123, 10115 Berlin, Deutschland",
            "BetaTech UG (haftungsbeschränkt) and Alpha Ventures GmbH",
            "6%",
            "1. Increase User Acquisition, 2. Enhance Customer Engagement, 3. Improve Product Quality",
        ]

    def test_rag_accuracy(self, question):
        pass

    def check_answer_contains(self, generated_answer, ground_truth_answer):
        """
        Check if the generated answer contains the ground truth answer
        or if ground truth contains generated answer.
        
        Returns:
        - bool: True if there's a match, False otherwise
        - float: Match score between 0.0 and 1.0
        """
        gen_lower = generated_answer.lower()
        truth_lower = ground_truth_answer.lower()
        
        if truth_lower in gen_lower:
            return True, 1.0
        elif gen_lower in truth_lower:
            return True, 1.0
        
        # Check for partial matches using keywords
        # Split ground truth into words and check how many appear in the generated answer
        truth_words = set(truth_lower.split())
        if not truth_words:
            return False, 0.0
            
        matching_words = sum(1 for word in truth_words if word in gen_lower)
        match_score = matching_words / len(truth_words)
        
        # Consider it a match if at least 70% of the keywords are present
        return match_score >= 0.7, match_score

    def run(self, questions):
        results = []

        for i, question in enumerate(questions):
            print(f"Processing Question {i+1}: {question}")

            generated_answer = self.test_rag_accuracy(question)
            print(f"Generated Answer: {generated_answer}")

            correct_answer = self.ground_truth_answers[i]
            print(f"Correct Answer: {correct_answer}")

            is_match, match_score = self.check_answer_contains(generated_answer, correct_answer)

            results.append({
                "question": question,
                "generated_answer": generated_answer,
                "correct_answer": correct_answer,
                "is_match": is_match,
                "match_score": match_score
            })

            print(f"Match: {is_match}, Score: {match_score:.2f}\n")

        matches = sum(1 for result in results if result["is_match"])
        accuracy = matches / len(results) if results else 0.0

        print(f"\nOverall Accuracy: {accuracy:.2f} ({matches}/{len(results)})")
        print("\nDetailed Results:")
        for result in results:
            print(f"Question: {result['question']}")
            print(f"Generated Answer: {result['generated_answer']}")
            print(f"Correct Answer: {result['correct_answer']}")
            print(f"Match: {result['is_match']}, Score: {result['match_score']:.2f}\n")