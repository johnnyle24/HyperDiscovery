from tkinter import *
from tkinter import ttk
from tkinter import filedialog
# from HypernymMining import HypernymMining
# from patternMining import PatternMining
# import sys

class Dialog:

    def __init__(self):
        self.root = Tk()
        self.root.title("Hypernym Discovery")

        mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        self.fscore = StringVar()
        self.spearman = StringVar()
        self.recall = StringVar()
        self.precision = StringVar()

        self.pattern_filename = StringVar()
        self.concept_filename = StringVar()
        self.gold_filename = StringVar()
        self.corpus_filename = StringVar()

        self.hypernym_order = StringVar()
        self.hypernym_order.set("<Hyper>:<Hypo>")

        self.hypernym_query = StringVar()
        self.hypernym_query.set("")

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

        ttk.Label(mainframe, textvariable=self.fscore).grid(column=2, row=7, sticky=(W, E))
        ttk.Label(mainframe, textvariable=self.spearman).grid(column=2, row=8, sticky=(W, E))
        ttk.Label(mainframe, textvariable=self.recall).grid(column=2, row=9, sticky=(W, E))
        ttk.Label(mainframe, textvariable=self.precision).grid(column=2, row=10, sticky=(W, E))

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

        ttk.Button(mainframe, text="Check Hypernym", command=self.run).grid(column=4, row=2, sticky=W)

        for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

        pattern_entry.focus()
        # root.bind('<Return>', calculate)

        self.root.mainloop()

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

    def run(self):

        file_name = self.corpus_filename

        # print("Pattern mining...")
        # # pattern_mining = PatternMining()
        #
        # print("...")
        # # pattern_mining.GetPairs()
        #
        # print("Hypernym hashing...")
        # hyp = HypernymMining()
        # print("...")
        # hyp.hash_patterns(self.pattern_filename)
        # print("...")
        # hyp.hash_hypernyms(self.concept_filename)
        #
        # print("Hypernym extraction...")
        # hyp.extract_hypernyms(file_name)
        #
        # print("Extraction Complete.")


def main():

    dialog = Dialog()


if __name__ == '__main__':
    main()
