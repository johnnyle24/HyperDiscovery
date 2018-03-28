
def get_file(data_file_name, output_file):
    with open('../Data/Model/hypernyms.txt') as file:
        hypes = file.readlines()

    with open('../Data/Model/concepts.txt') as file:
        concepts = file.readlines()

    with open(data_file_name) as file:
    # with open('../SemEval2018-Task9/test/data/2A.medical.test.data.txt') as file:
        train = file.readlines()

    results = []
    for s, con in enumerate(train):
        con = con.split()[0]
        for i, c in enumerate(concepts):
            c = c.split()
            if c[0] == con:
                if i < len(hypes):
                    results.append(hypes[i])
                    break
        if len(results) <= s:
            results.append(None)

    with open(output_file, 'w') as f:

        for r in results:
            if r is None:
                f.write('None\n')
            else:
                f.write(r.replace('\n', '') + '\n')