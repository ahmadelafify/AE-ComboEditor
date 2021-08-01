# Made in ~2018-2019

import os
import random
import re
import sys
import win32api

try:
    program_path = sys.argv[0]
    program_temp = os.path.dirname(program_path) + r'\\TEMP'
    txt_path = sys.argv[1]
    arg = sys.argv[2]
except Exception:
    program_path = None
    program_temp = None
    txt_path = None
    arg = None


def do_all(path):
    try:
        normalTmp, normalizeCount = normalize(path)
        cleanTmp, dupeCount = removedupes(normalTmp)
        randomTmp, randomizeCount = randomize(cleanTmp)
        os.remove(normalTmp)
        os.remove(cleanTmp)
        win32api.MessageBox(0, f'Normalized {normalizeCount} combos.\nRemoved {dupeCount} duplicate combos.\nRandomized {randomizeCount} combos.', 'Combo Editor')
    except Exception:
        pass


def normalize(path):
    normalizeCount = 0
    with open(path, 'r') as file:
        RACC = '([^\s]+):([^\s]+)'
        newPath = f'{os.path.splitext(path)[0]}_normalized.txt'
        if arg != '-all':
            with open(newPath, 'w+') as normalFile:
                for line in file:
                    r = re.search(RACC, line)
                    if r:
                        if '@' in r.group(1):
                            acc = f'{r.group(0)}\n'
                            normalizeCount += 1
                            normalFile.write(acc)
        else:
            randomNum1 = random.randint(1, 999999)
            randomNum2 = random.randint(1, 999999)
            newPath = program_temp + '\\' + str(randomNum1) + str(randomNum2) + "_tmp.txt"
            with open(newPath, 'w+') as normalFile:
                for line in file:
                    r = re.search(RACC, line)
                    if r:
                        if '@' in r.group(1):
                            acc = f'{r.group(0)}\n'
                            normalizeCount += 1
                            normalFile.write(acc)
                return newPath, normalizeCount

    win32api.MessageBox(0, f'Normalized {normalizeCount} combos.', 'Combo Editor')


def randomize(path):
    with open(path, 'r') as file:
        randomString = ''
        newPath = f'{os.path.splitext(path)[0]}_randomized.txt'
        fileList = file.readlines()
        randomList = random.sample(fileList, len(fileList))
        for i, line in enumerate(randomList):
            line = line.replace('\n', '')
            randomString += f'{line}\n'
        if arg != '-all':
            with open(newPath, 'w+') as randomFile:
                randomFile.write(randomString)
        else:
            newPath = f'{os.path.splitext(txt_path)[0]}_all.txt'
            with open(newPath, 'w+') as randomFile:
                randomFile.write(randomString)
            return newPath, len(fileList)

    win32api.MessageBox(0, f'Randomized {len(fileList)} combos.', 'Combo Editor')


def removedupes(path):
    dupeCount = 0
    with open(path, 'r') as file:
        newPath = f'{os.path.splitext(path)[0]}_removedupes.txt'
        lines_seen = set()  # holds lines already seen
        if arg != '-all':
            with open(newPath, 'w+') as cleanFile:
                for line in file:
                    if line not in lines_seen:  # not a duplicate
                        cleanFile.write(line)
                        lines_seen.add(line)
                    else:
                        dupeCount += 1
        else:
            randomNum1 = random.randint(1, 999999)
            randomNum2 = random.randint(1, 999999)
            newPath = f"{program_temp}\\{randomNum1}_{randomNum2}_tmp.txt"
            with open(newPath, 'w+') as cleanFile:
                for line in file:
                    if line not in lines_seen:  # not a duplicate
                        cleanFile.write(line)
                        lines_seen.add(line)
                    else:
                        dupeCount += 1
                return newPath, dupeCount

    win32api.MessageBox(0, f'Removed {dupeCount} duplicate combos.', 'Combo Editor')


def main():
    if '.txt' not in txt_path:
        win32api.MessageBox(0, 'Not a txt file.', 'Combo Editor')
    elif arg == "-all":
        do_all(txt_path)
    elif arg == "-normalize":
        normalize(txt_path)
    elif arg == "-randomize":
        randomize(txt_path)
    elif arg == "-removedupes":
        removedupes(txt_path)
    else:
        win32api.MessageBox(0, 'Invalid Arguement.', 'Combo Editor')


main()
