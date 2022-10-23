import regex as re


class Attribute:
    # TODO refine init class
    def __init__(self, description, tag, type):
        self.description = description
        self.tag = tag
        self.type = type

    @staticmethod
    def remove_required(a, b):
        new_list = [i for i in a if i not in b]
        return new_list

    # TODO: investigate if it's  better to do one single
    # method with an if loop, or a dictionary with keywords or different methods for each

    @staticmethod
    def find_shall(cond_shall):
        rules_shall = []
        for i in range(len(cond_shall)):
            text = re.findall(r'Shall.*$', cond_shall[i].description)
            if text:
                rules_shall.append(text)
        return rules_shall

    @staticmethod
    #TODO method so that the string captured is until a line break
    def clean_note(attribute_dict):
        attributes_no_note = attribute_dict
        for i in range(len(attribute_dict)):
            txt = attribute_dict[i].description
            note = re.findall(r'(Note:)+(?:Required)|(?:Shall)|(Note:.*)', txt)
            if len(note):
                attributes_no_note[i].description = txt.replace(note[0][1], '')
        return attributes_no_note