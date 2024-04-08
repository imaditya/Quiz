import json
import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class QuizApp(App):
    def build(self):
        with open('questions.json', 'r') as f:
            all_questions = json.load(f)
        self.questions = random.sample(all_questions, 20)
        self.score = 0
        self.current_question = 0
        self.root = BoxLayout(orientation='vertical')
        self.question_label = Label(text=self.questions[self.current_question]["question"])
        self.root.add_widget(self.question_label)
        self.buttons = []
        for i in range(4):
            button = Button(text=self.questions[self.current_question]["options"][i])
            button.bind(on_release=self.check_answer)
            self.buttons.append(button)
            self.root.add_widget(button)
        return self.root

    def check_answer(self, instance):
        if instance.text == self.questions[self.current_question]["answer"]:
            self.score += 1
        self.current_question += 1
        if self.current_question < len(self.questions):
            self.update_question()
        else:
            self.end_quiz()

    def update_question(self):
        self.question_label.text = self.questions[self.current_question]["question"]
        for i in range(4):
            self.buttons[i].text = self.questions[self.current_question]["options"][i]

    def end_quiz(self):
        for i in range(4):
            self.root.remove_widget(self.buttons[i])
        self.root.add_widget(Label(text="Score: " + str(self.score)))
        restart_button = Button(text="Restart")
        restart_button.bind(on_release=self.restart_quiz)
        self.root.add_widget(restart_button)

    def restart_quiz(self, instance):
        self.root.remove_widget(instance)
        self.root.remove_widget(self.root.children[0])
        self.score = 0
        self.current_question = 0
        self.update_question()
        for i in range(4):
            self.root.add_widget(self.buttons[i])

if __name__ == "__main__":
    QuizApp().run()
