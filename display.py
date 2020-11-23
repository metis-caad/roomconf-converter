def get_triples(path_or_connmap):
    """
        Fetches the triples for a Text Connection Map

        Parameter:
        ----------
        path_or_connmap: The path or the text connection map itself

        Returns:
        --------
        A list of triples for each room in the Connection Map

    """
    triples = []
    lines = []
    if str(path_or_connmap).startswith('['):
        lines.append(path_or_connmap)
    else:
        lines = open(path_or_connmap, 'r', encoding='utf-8').readlines()
    for line in lines:
        line = line[1:len(line) - 1]
        splitted_1 = line.split(']], [[')
        t1 = []
        for s1 in splitted_1:
            splitted_2 = s1.split('], [')
            t2 = []
            for s2 in splitted_2:
                splitted_3 = s2.strip('[[').strip(']]]').split(', ')
                t3 = []
                for s3 in splitted_3:
                    s4 = s3.strip('\'')
                    if s4 == 'None':
                        s4 = None
                    t3.append(s4)
                t2.append(t3)
            t1.append(t2)
        triples.append(t1)
    return triples


def get_guids(path_or_connmap):
    """
        Fetches the GUIDS for a Text Connection Map based on the number of unique edge sources

        Parameter:
        ----------
        path_or_connmap: The path or the text connection map itself

        Returns:
        --------
        A list of GUIDS for each unique source in the Connection Map

    """
    guids = []
    lines = []
    if str(path_or_connmap).startswith('['):
        lines.append(path_or_connmap)
    else:
        lines = open(path_or_connmap, 'r', encoding='utf-8').readlines()
        for line in lines:
            line = line[1:len(line) - 1]
            splitted_1 = line.split(']], [')
            t1 = []
            for s1 in splitted_1:
                t2 = []
                splitted_2 = s1.split('], [')
                count = 0
                for s2 in splitted_2:
                    count += 1
                    t3 = []
                    splitted_3 = s2.strip(', [').split(', ')
                    if count == 1:
                        source = splitted_3[0].strip('\'')
                        t2.append(source)
                    for s3 in splitted_3:
                        if s3.startswith('['):
                            s3 = s3.strip('[')
                        elif s2.endswith(']]'):
                            s3 = s3.strip(']]')
                        s4 = s3.strip('\'')
                        if source != s4:
                            t3.append(s4)
                    t2.append(t3)
                t1.append(t2)
            guids.append(t1)
        return guids
