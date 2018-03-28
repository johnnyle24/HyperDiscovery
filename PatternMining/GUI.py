from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from time import sleep
import multiprocessing
# from HypernymMining import HypernymMining
# from patternMining import PatternMining
# import sys
from Scoring import scorer
from Misc import downloadData
from HypernymMiningPhase2 import HypernymMining


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

        self.test_concept_filename = StringVar()
        self.test_gold_filename = StringVar()

        self.write_file = StringVar()

        self.pattern_filename.set("../MinedData/medical_patterns.json")
        self.concept_filename.set("../SemEval2018-Task9/training/data/2A.medical.training.data.txt")
        self.gold_filename.set("../SemEval2018-Task9/training/gold/2A.medical.training.gold.txt")
        self.corpus_filename.set("../Data/2A_med_pubmed_tokenized/2A_med_pubmed_tokenized")

        self.test_concept_filename.set("../SemEval2018-Task9/test/data/2A.medical.test.data.txt")
        self.test_gold_filename.set("../SemEval2018-Task9/test/gold/2A.medical.test.gold.txt")

        self.write_file.set("../MinedData/medical_results.txt")

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

        ttk.Label(mainframe, text="Enter a hypernym below").grid(column=3, row=1, sticky=(W, E))
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

        ttk.Label(mainframe, textvariable=self.hypernym_order).grid(column=3, row=3, sticky=(W, E))

        ttk.Label(mainframe, text="VISUALIZATION").grid(column=3, row=4, sticky=(W, E))

        ttk.Button(mainframe, text="Check Hypernym", command=self.check_hypernym).grid(column=4, row=2, sticky=W)

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

        concept_filename = "../Data/Model/concepts.txt"
        gold_filename = "../Data/Model/hypernyms.txt"

        self.hyp.load(concept_filename, gold_filename)

    def check_hypernym(self):
        order = self.hyp.get_order(self.hypernym_query.get())

        if len(order) > 0:
            ordered_hypernyms = order[0]

            for index in range(1, len(order)):
                ordered_hypernyms += ":" + order[index]

            self.hypernym_order.set(ordered_hypernyms)

    def set_data(self, choice):
        print(choice)
        if choice == 'Medical':
            self.pattern_filename.set("../MinedData/medical_patterns.json")
            self.concept_filename.set("../SemEval2018-Task9/training/data/2A.medical.training.data.txt")
            self.gold_filename.set("../SemEval2018-Task9/training/gold/2A.medical.training.gold.txt")
            self.corpus_filename.set("../Data/2A_med_pubmed_tokenized/2A_med_pubmed_tokenized")
            self.total_files = 368

            self.test_concept_filename.set("../SemEval2018-Task9/test/data/2A.medical.test.data.txt")
            self.test_gold_filename.set("../SemEval2018-Task9/test/gold/2A.medical.test.gold.txt")

            self.write_file.set("../MinedData/medical_results.txt")
        if choice == 'Music':
            self.pattern_filename.set("../MinedData/music_patterns.json")
            self.concept_filename.set("../SemEval2018-Task9/training/data/2B.music.training.data.txt")
            self.gold_filename.set("../SemEval2018-Task9/training/gold/2B.music.training.gold.txt")
            self.corpus_filename.set("../Data/2B_music_bioreviews_tokenized/2B_music_bioreviews_tokenized")
            self.total_files = 468

            self.test_concept_filename.set("../SemEval2018-Task9/test/data/2B.music.test.data.txt")
            self.test_gold_filename.set("../SemEval2018-Task9/test/gold/2B.music.test.gold.txt")

            self.write_file.set("../MinedData/music_results.txt")


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

        self.fscore.set("0")

        self.hyp = HypernymMining()

        frequency = 0

        self.hyp.parse(self.concept_filename.get(), self.gold_filename.get())

        self.hyp.parse_patterns(self.pattern_filename.get(), frequency)

        total = float(self.total_files)

        # self.total_files = 10 # For debugging purposes, uncomment when done

        for i in range(0, self.total_files+1):
            self.percent.set('{0}% complete...'.format(float(i)/total))
            filename = '{0}_{1}.txt'.format(self.corpus_filename.get(), i)
            self.hyp.discover(filename)
            print("Now serving file number: {0}".format(i))

        test_concepts = list()

        with open(self.test_concept_filename.get(), 'r') as concept_file:
            for concept_line in concept_file:
                concept = concept_line.split("\t")

                test_concepts.append(concept[0])

        self.hyp.write_results(test_concepts, self.write_file.get())
        self.hyp.write_model()


def main():

    dialog = Dialog()


if __name__ == '__main__':
    main()
