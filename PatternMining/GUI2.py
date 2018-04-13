from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from time import sleep
import multiprocessing
# from HypernymMining import HypernymMining
# from patternMining import PatternMining
# import sys
from HypernymMiningPhase3 import HypernymMining
import threading

import sys
sys.path.append('../')
from Scoring import scorer
from Misc import downloadData

class Dialog:

    def __init__(self):
        self.root = Tk()
        self.root.title("Hypernym Discovery")

        self.hyp = HypernymMining()
        self.total_files = 368

        mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        self.fscore = StringVar()
        self.spearman = StringVar()
        self.recall = StringVar()
        self.precision = StringVar()
        self.percent = StringVar()

        self.pattern_filename = StringVar()
        self.concept_filename = StringVar()
        self.gold_filename = StringVar()
        self.corpus_filename = StringVar()
        self.download_status = StringVar()

        self.percents_file = StringVar()
        self.results_file = StringVar()

        self.test_concept_filename = StringVar()
        self.test_gold_filename = StringVar()

        self.write_file = StringVar()

        self.found_string = StringVar()
        self.notfound_string = StringVar()

        self.results_gold = StringVar()
        self.results_concept = StringVar()

        self.results_gold.set("../MinedData/medical_hypernym_results.txt")
        self.results_concept.set("../SemEval2018-Task9/test/data/2A.medical.test.data.txt")

        self.pattern_filename.set("../MinedData/medical_patterns_revised.json")
        self.concept_filename.set("../SemEval2018-Task9/test/data/2A.medical.test.data.txt")
        self.gold_filename.set("../SemEval2018-Task9/test/gold/2A.medical.test.gold.txt")
        self.corpus_filename.set("../Data/2A_med_pubmed_tokenized/2A_med_pubmed_tokenized")

        self.percents_file.set("../MinedData/medical_hypernym_percents.txt")

        self.results_file.set("../MinedData/medical_hypernym_results.txt")

        self.test_concept_filename.set("../SemEval2018-Task9/test/data/2A.medical.test.data.txt")
        self.test_gold_filename.set("../SemEval2018-Task9/test/gold/2A.medical.test.gold.txt")

        self.write_file.set("../MinedData/medical_results.txt")

        self.found_string.set("Found Hypernyms")
        self.notfound_string.set("Not Found Hypernyms")

        self.hypernym_order = StringVar()
        self.hypernym_order.set("<Hyper>:<Hypo>")

        self.hypernym_query = StringVar()
        self.hypernym_query.set("")

        self.option = 'Select Dataset'
        self.default_option = StringVar()
        self.default_option.set(self.option)

        pattern_entry = ttk.Entry(mainframe, width=20, textvariable=self.pattern_filename)
        pattern_entry.grid(column=2, row=1, sticky=(W, E))

        concept_entry = ttk.Entry(mainframe, width=15, textvariable=self.concept_filename)
        concept_entry.grid(column=2, row=2, sticky=(W, E))

        gold_entry = ttk.Entry(mainframe, width=15, textvariable=self.gold_filename)
        gold_entry.grid(column=2, row=3, sticky=(W, E))

        corpus_entry = ttk.Entry(mainframe, width=15, textvariable=self.corpus_filename)
        corpus_entry.grid(column=2, row=4, sticky=(W, E))
        
        hypernym_entry = ttk.Entry(mainframe, width=15, textvariable=self.hypernym_query)
        hypernym_entry.grid(column=3, row=2, sticky=(W, E))

        ttk.Label(mainframe, textvariable=self.percent).grid(column=2, row=6, sticky=(W, E))

        ttk.Label(mainframe, textvariable=self.fscore).grid(column=2, row=7, sticky=(W, E))
        ttk.Label(mainframe, textvariable=self.spearman).grid(column=2, row=8, sticky=(W, E))
        ttk.Label(mainframe, textvariable=self.recall).grid(column=2, row=9, sticky=(W, E))
        ttk.Label(mainframe, textvariable=self.precision).grid(column=2, row=10, sticky=(W, E))
        ttk.Label(mainframe, textvariable=self.download_status).grid(column=3, row=0, sticky=(W, E))

        ttk.Label(mainframe, text="Enter a concept below").grid(column=3, row=1, sticky=(W, E))
        ttk.Label(mainframe, text="").grid(column=4, row=1, sticky=(W, E))

        # ttk.Label(mainframe, textvariable=self.pattern_filename).grid(column=2, row=2, sticky=(W, E))
        # ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=3, row=3, sticky=W)

        ttk.Button(mainframe, text="Run", command=self.run).grid(column=1, row=6, sticky=W)
        ttk.Button(mainframe, text="Pattern File", command=self.pattern_set).grid(column=1, row=1, sticky=W)
        ttk.Button(mainframe, text="Concept File", command=self.concept_set).grid(column=1, row=2, sticky=W)
        ttk.Button(mainframe, text="Gold File", command=self.gold_set).grid(column=1, row=3, sticky=W)
        ttk.Button(mainframe, text="Corpus File", command=self.corpus_set).grid(column=1, row=4, sticky=W)

        # ttk.Label(mainframe, text="F-Score").grid(column=3, row=1, sticky=W)
        # ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
        ttk.Label(mainframe, text="F-Score").grid(column=1, row=7, sticky=E)
        ttk.Label(mainframe, text="Spearman").grid(column=1, row=8, sticky=E)
        ttk.Label(mainframe, text="Recall").grid(column=1, row=9, sticky=E)
        ttk.Label(mainframe, text="Precision").grid(column=1, row=10, sticky=E)
        # ttk.Label(mainframe, text="Spearman").grid(column=3, row=2, sticky=W)

        ttk.Label(mainframe, textvariable=self.found_string).grid(column=3, row=3, sticky=(W, E))

        ttk.Label(mainframe, textvariable=self.notfound_string).grid(column=3, row=4, sticky=(W, E))

        # ttk.Label(mainframe, text="VISUALIZATION").grid(column=3, row=4, sticky=(W, E))

        # ttk.Button(mainframe, text="Clear", command=self.clear).grid(column=3, row=4, sticky=W)

        ttk.Button(mainframe, text="Display Found/Not Found", command=self.check_hypernym).grid(column=4, row=2, sticky=W)

        ttk.Button(mainframe, text="Load Previous Results", command=self.load).grid(column=4, row=1, sticky=W)

        choices = ['Choose Dataset', 'Medical', 'Music']
        ttk.OptionMenu(mainframe, self.default_option, *choices, command=self.set_data).grid(column=2, row=0, sticky=(W, E))

        ttk.Button(mainframe, text="Download Data", command=self.download_data).grid(column=1, row=0, sticky=(W, E))

        # option.pack(side='left', padx=10, pady=10)
        # button = tk.Button(root, text="check value slected", command=select)
        # button.pack(side='left', padx=20, pady=10)


        for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

        pattern_entry.focus()
        # root.bind('<Return>', calculate)

        self.root.mainloop()

    def load(self):

        self.hyp.load_results(self.concept_filename.get(), self.results_gold.get(), self.results_concept.get())

    def check_hypernym(self):
        found, notfound = self.hyp.check(self.hypernym_query.get())

        found_string = ""
        for f in found:
            found_string += f + ", "

        found_string.rstrip()

        notfound_string = ""
        for n in notfound:
            notfound_string += n + ", "

        notfound_string.rstrip()

        if len(found_string) < 1:
            found_string = "None found"
            notfound_string = ""

        self.found_string.set(found_string)
        self.notfound_string.set(notfound_string)

    def set_data(self, choice):
        print(choice)
        if choice == 'Medical':
            self.pattern_filename.set("../MinedData/medical_patterns_revised.json")
            self.concept_filename.set("../SemEval2018-Task9/test/data/2A.medical.test.data.txt")
            self.gold_filename.set("../SemEval2018-Task9/test/gold/2A.medical.test.gold.txt")
            self.corpus_filename.set("../Data/2A_med_pubmed_tokenized/2A_med_pubmed_tokenized")
            self.total_files = 368

            self.test_concept_filename.set("../SemEval2018-Task9/test/data/2A.medical.test.data.txt")
            self.test_gold_filename.set("../SemEval2018-Task9/test/gold/2A.medical.test.gold.txt")

            self.percents_file.set("../MinedData/medical_hypernym_percents.txt")

            self.results_file.set("../MinedData/medical_hypernym_results.txt")

            self.write_file.set("../MinedData/medical_results.txt")

            self.results_gold.set("../MinedData/medical_hypernym_results.txt")
            self.results_concept.set("../SemEval2018-Task9/test/data/2A.medical.test.data.txt")
        if choice == 'Music':
            self.pattern_filename.set("../MinedData/music_patterns.json")
            self.concept_filename.set("../SemEval2018-Task9/test/data/2B.music.test.data.txt")
            self.gold_filename.set("../SemEval2018-Task9/test/gold/2B.music.test.gold.txt")
            self.corpus_filename.set("../Data/2B_music_bioreviews_tokenized/2B_music_bioreviews_tokenized")
            self.total_files = 468

            self.test_concept_filename.set("../SemEval2018-Task9/test/data/2B.music.test.data.txt")
            self.test_gold_filename.set("../SemEval2018-Task9/test/gold/2B.music.test.gold.txt")

            self.percents_file.set("../MinedData/musical_hypernym_percents.txt")

            self.results_file.set("../MinedData/musical_hypernym_results.txt")

            self.write_file.set("../MinedData/music_results.txt")

            self.results_gold.set("../MinedData/musical_hypernym_results.txt")
            self.results_concept.set("../SemEval2018-Task9/test/data/2B.musical.test.data.txt")


    def concept_set(self):
        self.concept_filename.set(filedialog.askopenfilename(initialdir="/", title="Select file",
                                                        filetypes=(("all files", "*.*"), ("all files", "*.*"))))

    def gold_set(self):
        self.gold_filename.set(filedialog.askopenfilename(initialdir="/", title="Select file",
                                                            filetypes=(("all files", "*.*"), ("all files", "*.*"))))

    def corpus_set(self):
        try:
            value = float(self.fscore.get())
            self.spearman.set((0.3048 * value * 10000.0 + 0.5) / 10000.0)
        except ValueError:
            pass
        self.corpus_filename.set(filedialog.askopenfilename(initialdir="/", title="Select file",
                                                        filetypes=(("all files", "*.*"), ("all files", "*.*"))))

    def pattern_set(self):
        self.pattern_filename.set(filedialog.askopenfilename(initialdir="/", title="Select file",
                                                        filetypes=(("all files", "*.*"), ("all files", "*.*"))))

    def score(self):
        self.fscore.set(0)
        self.spearman.set(0)

    def download_data(self):
        self.download_status.set('Download in progress...')

        datasetName = self.default_option.get()

        if downloadData.download(datasetName):
            self.download_status.set('Done!')


    def run(self):

        frequency = 0

        self.hyp = HypernymMining()

        self.hyp.load(self.concept_filename.get(), self.pattern_filename.get(), 1000)

        self.hyp.load_test(self.concept_filename.get(), self.gold_filename.get())

        self.hyp.write_hypernyms(self.concept_filename.get(), self.results_file.get())

        self.hyp.write_percentages(self.concept_filename.get(), self.percents_file.get())

        total = float(self.total_files)

        self.total_files = 10 # For debugging purposes, uncomment when done

        threshold = 0  # only collect hypernyms with frequency above threshold

        greediness = 20

        def callback():
            for i in range(0, self.total_files+1):
                # self.percent.set("{0:.2f}% complete...".format(float(i)/total) * 100)
                self.percent.set('{0:.2f}% complete...'.format((float(i)/total) * 100))
                filename = '{0}_{1}.txt'.format(self.corpus_filename.get(), i)
                self.hyp.codiscover(filename, threshold)
                print("Now serving file number: {0}".format(i))

                self.hyp.discover(filename, greediness)

            with open(self.test_concept_filename.get(), 'r') as concept_file:
                for concept_line in concept_file:
                    concept = concept_line.split("\t")

                    test_concepts.append(concept[0])

            self.percent.set('100.00% now writing this can take a while...')
            # self.hyp.write_results(test_concepts, self.write_file.get())
            # self.hyp.write_model()
            self.percent.set('100.00% Finished!')

            scores = scorer.get_scores(self.gold_filename.get())
            self.fscore.set(scores['fscore'])
            self.recall.set(scores['recall'])
            self.precision.set(scores['precision'])

        t = threading.Thread(target=callback)
        t.start()
        test_concepts = list()

def main():

    dialog = Dialog()


if __name__ == '__main__':
    main()
