if __name__ == '__main__':
    corpus = '../Data/2B_music_bioreviews_tokenized.txt'
    # corpus = '../Data/2A_med_pubmed_tokenized.txt'
    # corpus = '../Data/musc/2B_music_bioreviews_2.txt'
    # corpus = '2A_med_pubmed_tokenized.txt'#sys.argv[1]

    f=open(corpus,'rU')
    lines = f.readlines()

    print(len(lines))

    n = 40
    chunkSize = len(lines) / n

    #3,239,945
    # chunkSize = 40000

    print('Processing file...')
    data = ''
    chunkData = list()
    for l, line in enumerate(lines):

        data += line

        if l % chunkSize == 0 and l != 0:
            chunkData.append(data)
            data = ''
    chunkData.append(data)
    print('Done Processing file!')
    # raw=f.read()


    for counter, data in enumerate(chunkData):

        # tag_file(data, '../Data/2A_med_pubmed_POITagged{0}.txt'.format(counter))

        # filename = '../Data/2A_med_pubmed_2/2A_med_pubmed_2_{0}.txt'.format(counter)
        filename = '../Data/musc/2B_music_bioreviews_2/2B_music_bioreviews_2_{0}.txt'.format(counter)
        print('Writing to file...')

        with open(filename, 'w') as file:
            file.write(data)