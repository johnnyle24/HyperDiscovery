

with open('../Data/Model/hypernyms.txt') as file:
    hypes = file.readlines()

with open('../Data/Model/concepts.txt') as file:
    concepts = file.readlines()

with open('../SemEval2018-Task9/test/data/2A.medical.test.data.txt') as file:
    train = file.readlines()


results = []
for s, con in enumerate(train):
    con = con.split()[0]
    for i, c in enumerate(concepts):
        c = c.split()
        if c[0] == con:
            print(concepts[i])
            if i < len(hypes):
                results.append(hypes[i])
                break
    if len(results) <= s:
        results.append(None)

with open('train_results.txt', 'w') as f:

    for r in results:
        if r is None:
            f.write('None\n')
        else:
            f.write(r.replace('\n', '') + '\n')

