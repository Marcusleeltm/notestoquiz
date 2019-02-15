import os
import random
import xml.etree.ElementTree as ET

import nltk
import spacy
from kivy.app import App
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListItemButton
from kivy.uix.popup import Popup
from nltk.tokenize.moses import MosesDetokenizer
from nltk import word_tokenize
from thesaurus import Word

Window.size = (550, 650)

Window.clearcolor = (0,.5,.5,0)
# Listing all the notes ins the main page
class NoteListButton(ListItemButton):
    # ListItemButton.background_color= (0,1,1,1)
    ListItemButton.selected_color = (0,.5,1,1)
    ListItemButton.deselected_color = (0,1,1,1)

    pass


# A Pop up with customizable text and button
class TextPopup(Popup):
    pass


# A pop up with a customizable button
class WarningPopup(Popup):
    pass


# A pop up to view the note that is selected
class ViewPopup(Popup):
    pass


# Window to create a new note
class NewPopup(Popup):
    pass

    # logic to create a new note
    def save_new_note(self):
        # Find the xml file where the note will be going to be entered into
        temp_note = []
        base_path = os.path.dirname(os.path.realpath(__file__))
        xml_file = os.path.join(base_path, "definition.xml")
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # getting all the title in the xml file to ensure no duplication happen later
        for Def in root.findall("Def"):
            module = Def.find('tags').text
            temp_note.append(module)

        # Getting the note from the textboxes
        note_module = self.module_text_input.text
        note_tags = self.tags_text_input.text
        note_definition_note = self.definitionNote_text_input.text

        a = note_tags
        # if title already exist, show error
        if a in temp_note:
            pop = WarningPopup(title="ERROR")
            pop.ids.warning.text = "This title already exist"
            pop.open()
        # else if the form is note fully filled up, show an error message
        elif note_module == "" or note_tags == "" or note_definition_note == "":
            pop = WarningPopup(title="ERROR")
            pop.ids.warning.text = "One or more field is empty"
            pop.open()
        # write the notes into xml file
        else:
            j = len(root) + 1
            new_note = ET.SubElement(root, "Def", id=str(j))
            new_note_module = ET.SubElement(new_note, "module")
            new_note_tag = ET.SubElement(new_note, "tags")
            new_note_description = ET.SubElement(new_note, "description")

            new_note_module.text = note_module
            new_note_tag.text = note_tags
            new_note_description.text = note_definition_note
            tree.write(xml_file)
            self.dismiss()


# window to edit existing note
class EditPopup(Popup):
    pass

    # logic to edit existing notes
    def editnote(self, tags):
        # getting the location of the xml file and get ready to read and write
        base_path = os.path.dirname(os.path.realpath(__file__))
        xml_file = os.path.join(base_path, "definition.xml")
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # getting the note from the textbox
        note_definition_note = self.definitionNote_text_input.text

        # replace the existing text with the new text taken from the textbox
        for Def in root.findall("Def"):
            t = Def.find('tags').text
            if t == tags.text:
                Def.find("description").text = note_definition_note

        tree.write(xml_file)


# window to asked subjective questions
class SubjectivePopup(Popup):
    pass

    # logic to show the full correct answer
    def Subjective_Answer(self):
        print(subjective_definition)
        c = TextPopup(title="   ")
        c.ids.txt.text = subjective_definition
        c.open()


# window to ask MCQ Question
# class MCQPopup(Popup):
#     pass
#
#     # logic to identify whether the answer is correct or incorrect
#     def mcqcheck(self, value):
#         # print(mcqanswer)
#         # print(value)
#         if mcqanswer == value:
#             pop = WarningPopup(title="Congratulation")
#             pop.ids.warning.text = "Correct"
#             pop.open()
#         else:
#             pop = WarningPopup(title="Sorry")
#             pop.ids.warning.text = "Incorrect"
#             pop.open()


# window to ask fill in the blanks question
class RemoveWordsPopup(Popup):
    pass

    # logic to show the correct answer
    def RWAnswer(self):
        print(definition)
        pop = TextPopup(title="Answer")
        pop.ids.txt.text = definition
        pop.open()


# window to ask true or false questions
class TrueFalsePopup(Popup):
    pass

    # logic to check the users answer
    def TFcheck(self, value):
        print(value)

        if TFAnswer == value:
            pop = WarningPopup(title="Congratulation")
            pop.ids.warning.text = "Correct"
            pop.open()
        else:
            pop = WarningPopup(title="Sorry")
            pop.ids.warning.text = "Incorrect"
            pop.open()


# main class
class NoteDB(BoxLayout):
    first_name_text_input = ObjectProperty()
    note_list = ObjectProperty()

    def new_note(self):
        pop = NewPopup()
        pop.open()

    def view_note(self):
        base_path = os.path.dirname(os.path.realpath(__file__))
        xml_file = os.path.join(base_path, "definition.xml")
        tree = ET.parse(xml_file)
        root = tree.getroot()
        # If a list item is selected
        if self.note_list.adapter.selection:
            # Get the text from the item selected
            selection = self.note_list.adapter.selection[0].text
            view_note_popup = ViewPopup(title=selection)
            for Def in root.findall("Def"):
                tags = Def.find('tags').text
                if tags == selection:
                    D = Def.find('description').text
                    M = Def.find('module').text
                    view_note_popup.ids.module.text = M
                    view_note_popup.ids.tags.text = tags
                    view_note_popup.ids.definitionNote.text = D
            view_note_popup.open()

    def quiz_note(self, value):
        m = value
        print(m)
        if self.note_list.adapter.selection:
            o = self.note_list.adapter.selection[0].text
            if m == 'Subjective':
                self.subjective(o)
            elif m == 'Blanks':
                self.removewords(o)
            elif m == 'True/False':
                self.tf(o)
            elif m == 'Random':
                ran = random.randint(0,2)
                # if m == 0:
                #     self.mcq(p)
                if ran == 0:
                    self.removewords(o)
                elif ran == 1:
                    self.tf(o)
                elif ran == 2:
                    self.subjective(o)
        elif not self.note_list.adapter.selection:
            l = len(self.note_list.adapter.data)
            k = random.randint(0, l - 1)
            rands = random.randint(0,2)
            j = self.note_list.adapter.data[k]
            # if m == 0:
            #     self.mcq(j)
            if rands == 0:
                self.removewords(j)
            elif rands == 1:
                self.tf(j)
            elif rands == 2:
                self.subjective(j)

    def subjective(self, p):

        base_path = os.path.dirname(os.path.realpath(__file__))
        xml_file = os.path.join(base_path, "definition.xml")

        tree = ET.parse(xml_file)
        root = tree.getroot()

        for Def in root.findall("Def"):
            module = Def.find('tags').text
            if module == p:
                SubDefine = Def.find('description').text
        print(SubDefine)
        x = random.randint(0, 1)

        global subjective_definition
        subjective_definition = SubDefine

        if x == 0:

            define = ['Define', 'In your own words, explain what is ']
            text = subjective_definition

            # separate sentence into individual words
            tokenOriText = word_tokenize(text)
            # print(tokenOriText)

            # identify the grammar of each words
            grammar = nltk.pos_tag(tokenOriText)
            # print(grammar)

            x = "is"
            if x in tokenOriText:
                t = tokenOriText.index('is')
                # print(t)
                tokenOriText[t] = define[random.randrange(len(define))]

                a = [tokenOriText[t]]

                i = 0
                while i < t:
                    a.append(tokenOriText[i])
                    i = i + 1

                # print(a)

                detokenizer = MosesDetokenizer()
                t = detokenizer.detokenize(a, return_str=True)

                print(t)
                pop = SubjectivePopup()
                pop.open()
                pop.ids.txt.text = t
            else:
                pop = WarningPopup(title="ERROR")
                pop.ids.warning.text = "subjective question is unavailable"
                pop.open()

        elif x == 1:
            nlp = spacy.load('en_core_web_sm')

            wholedefinition = SubDefine
            BreakDefinition = word_tokenize(wholedefinition)

            # TO FIND THE NAME ENTITY RECOGNITION IN THE TEXT
            document = nlp(wholedefinition)

            person = []

            # Make a list of all the names found in the text
            for ent in document.ents:
                if ent.label_ == 'PERSON':
                    person.append(ent)

            # CREATE A QUESTIONS REVOLVING AROUND THE PERSON
            if len(person) != 0:
                # REWRITE THE DEFINITION into a Questions
                print(BreakDefinition)
                ppl = person[0]
                o = wholedefinition.replace(str(ppl), 'Who')
                p1 = o + "?"
                p2 = "Who is " + str(ppl) + " ?"

                r = random.randint(0, 1)
                pop = SubjectivePopup()
                pop.open()

                if r == 0:
                    pop.ids.txt.text = p1
                elif r == 1:
                    pop.ids.txt.text = p2
            else:
                pop = WarningPopup(title="ERROR")
                pop.ids.warning.text = "subjective question is unavailable"
                pop.open()


    def tf(self, p):
        ca = TrueFalsePopup()
        ca.open()

        # SYSTEM WILL DECIDE RANDOMLY TO PRINT FALSE OR TRUE
        m = random.randint(0, 1)
        print(m)
        global TFAnswer

        base_path = os.path.dirname(os.path.realpath(__file__))
        xml_file = os.path.join(base_path, "definition.xml")

        tree = ET.parse(xml_file)
        root = tree.getroot()

        for Def in root.findall("Def"):
            module = Def.find('tags').text
            if module == p:
                j = Def.find('description').text
        print(j)

        definition = j

        # PRINT QUESTION
        if m == 1:
            ca.ids.L.text = definition
            TFAnswer = 0
        elif m == 0:

            # BREAK THE DEFINITION INTO INDIVIDUAL WORDS
            BreakDefinition = word_tokenize(definition)
            # print(BreakDefinition)

            # LABEL EACH WORD WITH ITS CORRESPONDING PART OF SPEECH TAG
            grammar = nltk.pos_tag(BreakDefinition)
            # print(grammar)

            # CREATE A LIST OF WORDS THAT HAS THE NN TAG
            is_noun = lambda pos: pos[:2] == 'NN'
            list_of_nn = [word for (word, pos) in grammar if is_noun(pos)]
            # shuffle = random.shuffle(list_of_nn)
            # print(list_of_nn)

            # IF THE LIST IS MORE THAN 3, TAKE ONLY 3
            if len(list_of_nn) >= 3:
                choice = random.sample(list_of_nn, 3)
            else:
                choice = list_of_nn
            print(choice)

            # FOR EACH OF THE WORD GET AN ALTERNATIVE WORD
            z = []
            for i in choice:
                print(i)
                thesaurus = Word(i)
                syn = thesaurus.synonyms()
                print(syn)
                if len(syn) < 1:
                    syn = i
                c = random.choice(syn)
                z.append(c)
                print(z)

            # REWRITE THE DEFINITION WITH THE ALTERNATIVE WORD
            a = 0
            for i in choice:
                j = BreakDefinition.index(i)
                BreakDefinition[j] = z[a]
                a = a + 1

            FalseStatement = " ".join(BreakDefinition)
            print(FalseStatement)
            la = FalseStatement
            ca.ids.L.text = la
            TFAnswer = 1

    def removewords(self, p):
        pop = RemoveWordsPopup()
        pop.open()

        base_path = os.path.dirname(os.path.realpath(__file__))
        xml_file = os.path.join(base_path, "definition.xml")

        tree = ET.parse(xml_file)
        root = tree.getroot()

        for Def in root.findall("Def"):
            module = Def.find('tags').text
            if module == p:
                j = Def.find('description').text
        print(j)

        global definition

        definition = j

        # BREAK THE DEFINITION INTO INDIVIDUAL WORDS
        BreakDefinition = word_tokenize(definition)
        # print(BreakDefinition)

        # LABEL EACH WORD WITH ITS CORRESPONDING PART OF SPEECH TAG
        grammar = nltk.pos_tag(BreakDefinition)
        # print(grammar)

        # CREATE A LIST OF WORDS THAT HAS THE NN TAG
        is_noun = lambda pos: pos[:2] == 'NN'
        list_of_nn = [word for (word, pos) in grammar if is_noun(pos)]
        # shuffle = random.shuffle(list_of_nn)
        # print(list_of_nn)

        # IF THE LIST IS MORE THAN 5, TAKE ONLY 5
        if len(list_of_nn) >= 5:
            choice = random.sample(list_of_nn, 5)
        else:
            choice = list_of_nn

        # REPLACE CHOSEN WORDS WITH (__) IN DEFINITION
        for i in choice:
            j = BreakDefinition.index(i)
            BreakDefinition[j] = '(____)'
        # print(j)
        # print(BreakDefinition)

        # PRINT THE QUESTION
        FinalQuestion = " ".join(BreakDefinition)
        print(FinalQuestion)

        # PRINT THE CHOICES
        shuffle = random.shuffle(choice)
        print(choice)

        pop.ids.Q.text = FinalQuestion
        pop.ids.A.text = "A. " + choice[0]
        pop.ids.B.text = "B. " + choice[1]
        pop.ids.C.text = "C. " + choice[2]
        pop.ids.D.text = "D. " + choice[3]
        pop.ids.E.text = "E. " + choice[4]

    # def mcq(self, p):
    #     c = MCQPopup()
    #     c.open()
    #
    #     base_path = os.path.dirname(os.path.realpath(__file__))
    #     xml_file = os.path.join(base_path, "definition.xml")
    #
    #     tree = ET.parse(xml_file)
    #     root = tree.getroot()
    #
    #     for Def in root.findall("Def"):
    #         module = Def.find('tags').text
    #         if module == p:
    #             j = Def.find('description').text
    #     print(j)
    #
    #     definition = j
    #
    #     # BREAK THE DEFINITION INTO INDIVIDUAL WORDS
    #     tokenizeDefinition = word_tokenize(definition)
    #     # print(tokenizeDefinition)
    #
    #     # LABEL EACH WORD WITH ITS CORRESPONDING PART OF SPEECH TAG
    #     grammar = nltk.pos_tag(tokenizeDefinition)
    #     # print(grammar)
    #
    #     # CREATE A LIST OF WORDS THAT HAS THE NN TAG
    #     is_noun = lambda pos: pos[:2] == 'NN'
    #     list_of_nn = [word for (word, pos) in grammar if is_noun(pos)]
    #     # print(list_of_nn)
    #
    #     # CHOOSE ONE WORD FROM THE LIST OF NN
    #     RandomWord = random.choice(list_of_nn)
    #     print('Random Word : ' + RandomWord)
    #
    #     # FIND LIST OF WORDS THAT ARE SIMILAR TO THE CHOSEN WORD
    #     thesaurus = Thesaurus(RandomWord)
    #     syn = thesaurus.get_synonym()
    #     # print(syn)
    #
    #     # IF THE LIST HAS LESS THAN 3 SIMILAR WORD CHOOSE ANOTHER WORD FROM THE LIST OF NN
    #     while len(syn) < 3:
    #         RandomWord = random.choice(list_of_nn)
    #         thesaurus = Thesaurus(RandomWord)
    #         syn = thesaurus.get_synonym()
    #
    #     # GET 3 SIMILAR WORDS
    #     choice = random.sample(syn, 3)
    #     # print(choice)
    #
    #     # MERGE THE 3 SIMILAR WORDS AND THE CHOSEN WORD
    #     choice.insert(randint(1, 4), RandomWord)
    #     FinalChoice = choice[:]
    #
    #     # REWRITE THE DEFINITION TEXT WITH A BLANK
    #     j = tokenizeDefinition.index(RandomWord)
    #     # print(j)
    #     tokenizeDefinition[j] = '(______)'
    #     # print(tokenizeDefinition)
    #
    #     # PRINT QUESTION AND CHOICES
    #     FinalQuestion = " ".join(tokenizeDefinition)
    #     print(FinalQuestion)
    #     i = ['A. ', 'B. ', 'C. ', 'D. ']
    #     for alpha, l in zip(i, FinalChoice):
    #         print(alpha, l)
    #
    #     c.ids.question.text = FinalQuestion
    #     c.ids.A.text = FinalChoice[0]
    #     c.ids.B.text = FinalChoice[1]
    #     c.ids.C.text = FinalChoice[2]
    #     c.ids.D.text = FinalChoice[3]
    #
    #     global mcqanswer
    #
    #     mcqanswer = FinalChoice.index(RandomWord)

    def edit_note(self):
        base_path = os.path.dirname(os.path.realpath(__file__))
        xml_file = os.path.join(base_path, "definition.xml")
        tree = ET.parse(xml_file)
        root = tree.getroot()
        # If a list item is selected
        if self.note_list.adapter.selection:
            # Get the text from the item selected
            selection = self.note_list.adapter.selection[0].text
            popup = EditPopup(title = selection)
            for Def in root.findall("Def"):
                tags = Def.find('tags').text
                if tags == selection:
                    D = Def.find('description').text
                    M = Def.find('module').text
                    ID = Def.attrib
                    popup.ids.module.text = M
                    popup.ids.tags.text = tags
                    popup.ids.definitionNote.text = D

            popup.open()

    def refresh(self):
        self.note_list.adapter.data.clear()
        base_path = os.path.dirname(os.path.realpath(__file__))
        xml_file = os.path.join(base_path, "definition.xml")

        tree = ET.parse(xml_file)
        root = tree.getroot()
        k = []

        for elem in root.iter('tags'):
            if elem.text not in k:
                k.append(elem.text)
                self.note_list.adapter.data.append(elem.text)
        # self.note_list.size_hint_x = "0.8"
        self.note_list._trigger_reset_populate()

        j = []
        for Def in root.iter("module"):
            if Def.text not in j:
                j.append(Def.text)

        self.ids.spinner_id.values = j

    def delete_note(self):

        base_path = os.path.dirname(os.path.realpath(__file__))
        print(base_path)

        xml_file = os.path.join(base_path, "definition.xml")
        print(xml_file)

        tree = ET.parse(xml_file)
        root = tree.getroot()

        # If a list item is selected
        if self.note_list.adapter.selection:
            # Get the text from the item selected
            selection = self.note_list.adapter.selection[0].text

            for Def in root.findall("Def"):
                module = Def.find('tags').text
                if module == selection:
                    root.remove(Def)
            tree.write(xml_file)

            # Remove the matching item
            self.note_list.adapter.data.remove(selection)

            # Reset the ListView
            self.note_list._trigger_reset_populate()

    def change_folder(self, value):
        self.note_list.adapter.data.clear()
        base_path = os.path.dirname(os.path.realpath(__file__))
        xml_file = os.path.join(base_path, "definition.xml")

        tree = ET.parse(xml_file)
        root = tree.getroot()
        k = []

        for Def in root.findall("Def"):
            module = Def.find('module').text
            if module == value:
                k = Def.find('tags').text
                self.note_list.adapter.data.append(k)
        # self.note_list.size_hint_x = "0.8"
        self.note_list._trigger_reset_populate()

    def search(self, value):
        # CLEAR THE ENTIRE LIST FIRST
        self.note_list.adapter.data.clear()

        # RETRIEVE DATA FROM XML FILE
        base_path = os.path.dirname(os.path.realpath(__file__))
        xml_file = os.path.join(base_path, "definition.xml")

        tree = ET.parse(xml_file)
        root = tree.getroot()

        # LOOK THROUGH EVERY NOTE ONE BY ONE
        for Def in root.iter("Def"):
            module = Def.find('module').text
            tags = Def.find('tags').text
            description = Def.find("description").text

            # TOKENIZE, SEARCH definition, modules and title for a MATCH
            tdesc = word_tokenize(description)
            if module == value:
                self.note_list.adapter.data.append(tags)
            elif tags == value:
                self.note_list.adapter.data.append(tags)
            elif value in tdesc:
                self.note_list.adapter.data.append(tags)

        # DISPLAY THE NOTES THAT HAS MATCHES
        if not self.note_list.adapter.data:
            self.note_list.adapter.data.append("-----List not found-----")
            self.note_list.adapter.data.remove("-----List not found-----")
            self.note_list._trigger_reset_populate()
        else:
            self.note_list._trigger_reset_populate()


class NotesApp(App):
    def build(self):
        return NoteDB()

dbApp = NotesApp(title = "NOTES TO QUIZ")
dbApp.run()
