def open_file(path):
    reading_file = open(path, 'r')
    return reading_file.read().split()

class two_song_report():
    def __init__(self, list_report, phrases_dict, longest_phrases):
        self.list_report = list_report
        self.phrases_dict = phrases_dict
        self.longest_phrases = longest_phrases

# compares two songs in their entirety, returning all the matching phrases in common, the longest
# should probably be reworked in order to only log a phrase once, at the longest
def compare_two_file(file_1_path, file_2_path):
    file_1 = open_file(file_1_path)
    file_2 = open_file(file_2_path)
    reporting_list = []
    matching_phrases = {}
    for i, iword in enumerate(file_1[:len(file_1):]):
        for j, jword in enumerate(file_2[:(len(file_2)):]):
            current_combo = 0
            current_phrase = ''
            while jword == iword:
                current_phrase += iword
                current_combo += 1
                if (j + current_combo) >= len(file_2) or (i + current_combo) >= len(file_1):
                    break
                else:
                    jword = file_2[(j + current_combo)]
                    iword = file_1[(i + current_combo)]
                    current_phrase += ' '
            if current_combo != 0:
                try:
                    reporting_list[((current_combo) - 1)] += 1
                    matching_phrases[str(current_combo)].append(current_phrase)
                except IndexError:
                    while len(reporting_list) < (current_combo - 1):
                        reporting_list.append(0)
                    reporting_list.append(1)
                    matching_phrases[str(current_combo)] = [current_phrase]
            iword = file_1[i]
    longest_phrase = matching_phrases[str(len(reporting_list))]
    return two_song_report(reporting_list, matching_phrases, longest_phrase)



