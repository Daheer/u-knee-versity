import os
import reflex as rx
import google.generativeai as genai


# Checking if the API key is set properly
if not os.getenv("GOOGLE_API_KEY"):
    raise Exception("Please set GOOGLE_API_KEY environment variable.")


class QA(rx.Base):
    """A question and answer pair."""

    question: str
    answer: str


DEFAULT_CHATS = {
    "Intros": [
        QA(
            question="",  # Empty question to indicate it's a system message
            answer="Hello! I'm KneeGPT, your expert guide to knee anatomy and surgery. Ready to explore the intricate world of knee health? Let me know what you'd like to learn today, and I'll help you navigate through our interactive 3D model and answer any questions you might have. Open it by clicking the \"View 3D Model\" button above"
        )
    ],
}


class State(rx.State):
    """The app state."""

    # A dict from the chat name to the list of questions and answers.
    chats: dict[str, list[QA]] = DEFAULT_CHATS

    # The current chat name.
    current_chat = "Intros"

    # The current question.
    question: str

    # Whether we are processing the question.
    processing: bool = False

    # The name of the new chat.
    new_chat_name: str = ""

    def create_chat(self):
        """Create a new chat."""
        # Add the new chat to the list of chats.
        self.current_chat = self.new_chat_name
        self.chats[self.new_chat_name] = []

    def delete_chat(self):
        """Delete the current chat."""
        del self.chats[self.current_chat]
        if len(self.chats) == 0:
            self.chats = DEFAULT_CHATS
        self.current_chat = list(self.chats.keys())[0]

    def set_chat(self, chat_name: str):
        """Set the name of the current chat.

        Args:
            chat_name: The name of the chat.
        """
        self.current_chat = chat_name

    @rx.var
    def chat_titles(self) -> list[str]:
        """Get the list of chat titles.

        Returns:
            The list of chat names.
        """
        return list(self.chats.keys())

    async def process_question(self, form_data: dict[str, str]):
        # Get the question from the form
        question = form_data["question"]

        # Check if the question is empty
        if question == "":
            return

        model = self.gemini_process_question

        async for value in model(question):
            yield value

    async def gemini_process_question(self, question: str):
        """Get the response from the Google Gemini API.

        Args:
            question: The user's question.
        """
        # Configure the Gemini API
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

        # Add the question to the list of questions.
        qa = QA(question=question, answer="")
        self.chats[self.current_chat].append(qa)

        # Clear the input and start the processing.
        self.processing = True
        yield

        # Prepare the conversation history
        chat_history = []
        for qa in self.chats[self.current_chat][:-1]:
            chat_history.append({
                'role': 'user',
                'parts': [{'text': qa.question}]
            })
            chat_history.append({
                'role': 'model',
                'parts': [{'text': qa.answer}]
            })

        # Create the model
        model = genai.GenerativeModel(
            model_name = 'gemini-1.5-flash',
            system_instruction = '''
            You are a KneeGPT, you work at a U-Knee-Versity.
            You are a knee surgery expert who helps students learn about knee surgery
            There is a 3D interactive model that you  refer students to 
            The 3D model is labelled and the labels are as follows
            1. Patellar Tendon
            2. Quadriceps Tendon
            3. Tibial Tuberosity
            4. Medial Collateral Ligament
            5. Medial Meniscus
            6. Posterior Cruciate Ligament
            7. Posterior Meniscofemoral Ligament
            8. Anterior Cruciate Ligament
            9. Lateral Meniscus
            10. Lateral Collateral Ligament
            11. Transverse Ligament
            '''
        )
        
        # Start the chat
        chat = model.start_chat(history=chat_history)

        # Send the question and stream the response
        try:
            response = chat.send_message(question, stream=True)
            
            full_answer = ""
            for chunk in response:
                answer_text = chunk.text
                full_answer += answer_text
                self.chats[self.current_chat][-1].answer = full_answer
                self.chats = self.chats
                yield
        except Exception as e:
            # Handle any potential API errors
            error_message = f"An error occurred: {str(e)}"
            self.chats[self.current_chat][-1].answer = error_message
            self.chats = self.chats
            yield

        # Toggle the processing flag.
        self.processing = False