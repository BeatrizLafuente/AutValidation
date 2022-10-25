import regex as re


class Attribute:
    # TODO refine init class
    def __init__(self, description, tag, type):
        self.description = description
        self.tag = tag
        self.type = type

    @staticmethod
    def find_req(attribute_dict):
        required_att=[]
        for a in attribute_dict:
            if re.search(r'Required', a.description):
                required_att.append(a)
        return required_att
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
    def clean_note(attribute_dict):
        attributes_no_note = attribute_dict
        for i in range(len(attribute_dict)):
            txt = attribute_dict[i].description
            note = re.search(r'(Note:.*)+(.+?(?=Required))|(.+?(?=Shall))|(.+?(?=\n))', txt)
            if note:
                attributes_no_note[i].description = txt.replace(note.group(), '')
        return attributes_no_note
