def compareFiles(path1, path2):
    with open(path1) as f1, open(path2) as f2, open('outfile.txt', 'w') as outfile:
        for line1, line2 in zip(f1, f2):
            if line1 == line2:
                print(line1.strip() + ' -> pass' , file=outfile)
            else:
                print(line1.strip() + ' ***** ' + line2.strip() + ' -> fail' , file=outfile)

compareFiles('test_data_1.txt', 'test_data_2.txt')