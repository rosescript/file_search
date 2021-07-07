# inspired by Izzy Analytics

import os
import pickle
import PySimpleGUI as sg
sg.ChangeLookAndFeel('DarkTeal9')

class Gui:
    def __init__(self):
        self.layout = [
            # row 1
            [sg.Text("Search Terms", size=(10, 1)), 
            sg.Input(size=(45,1), focus=True, key="TERM"), 
            sg.Radio("Contains", group_id="choice", key="CONTAINS", default=True), 
            sg.Radio("StartsWith", group_id="choice", key="STARTSWITH"), 
            sg.Radio("EndsWith", group_id="choice", key="ENDSWITH")],

            # row 2
            [sg.Text("Root Path", size=(10,1)),
            sg.Input("C:/", size=(45,1), key="PATH"), 
            sg.FolderBrowse('Browse', size=(10,1)), 
            sg.Button("Re-Index", size=(10,1), key="_INDEX_"), 
            sg.Button("Search", size=(10,1), bind_return_key=True, key="_SEARCH_")],

            # row 3
            [sg.Output(size=(100,30))]
        ]
        self.window = sg.Window("File Search Engine").Layout(self.layout)


class SearchEngine:
    def __init__(self):
        self.file_index = [] #stores directory indexes that are found by the os walk function
        self.results = [] #stores search results
        self.matches = 0 #counts each matching file
        self.records = 0 #counts each record searched

    def create_new_index(self, values):
        # creates a new index and saves the file
        root_path = values["PATH"]
        self.file_index = [(root, files) for root, dirs, files in os.walk(root_path) if files]

        # save to file
        with open("file_index.pkl", "wb") as f:
            # opens the file or creates it if it doesnt exist
             pickle.dump(self.file_index, f) # dumps the contents of self.file_index to the file

    def load_existing_index(self):
        # loads existing indices
        
        try:
            with open("file_index.pkl", "rb") as f:
                self.file_index = pickle.load(f)
        except:
            self.file_index = []

    def search(self, values):
        # search for term based on search type
        
        #reset variables
        self.results.clear()
        self.matches = 0
        self.records = 0
        term = values["TERM"]

        #perform search
        for path, files in self.file_index:
            for file in files:
                self.records +=1

                # accounts for all possible search terms/options
                if (values["CONTAINS"] and term.lower() in file.lower() or
                    values["STARTSWITH"] and file.lower().startswith(term.lower()) or 
                    values["ENDSWITH"] and file.lower().endswith(term.lower())):

                    # formats the result, then stores it into results list, then incriments matches since a match was found
                    result = path.replace('\\','/') + '/' + file
                    self.results.append(result)
                    self.matches +=1
                else:
                    continue

        # save search results
        with open("search_results.txt", "w") as f:
            for row in self.results:
                f.write(row + '\n')


def test1():
    s = SearchEngine()
    s.load_existing_index()
    s.search("pickle")

    print("\n>> There were {:,d} matches out of {:,d} records searched.\n".format(s.matches, s.records))
    print("This query produced the following matches: \n")

    for match in s.results:
        print(match)

def test2():
    g = Gui()

    while True:
        event, values = g.window.Read()
        print(event, values)
    

def main():
    # create the gui and search engine objects
    g = Gui()
    s = SearchEngine()
    s.load_existing_index()

    while True:
        event, values = g.window.Read()

        if event is None: 
            break
        if event == "_INDEX_": # creates a new index
            s.create_new_index(values)
            print()
            print(">> New Index has been created")
            print()
        if event == "_SEARCH_":
            s.search(values)

            print()
            for result in s.results:
                print(result)
            
            print()
            
            print("\n>> There were {:,d} matches out of {:,d} records searched.\n".format(s.matches, s.records))
            print("Results saved in working directory as search_results.txt")
            
            



main()
