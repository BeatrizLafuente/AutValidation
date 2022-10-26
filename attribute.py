import regex as re


class Attribute:
    # TODO refine init class
    def __init__(self, description, tag, type):
        self.description = description
        self.tag = tag
        self.type = type

    @staticmethod
    def get_note(description):
        n = description
        note = re.search('(Note.*?)(?:(?=Required)|(?:(?=Shall))|(\n)|($))', description)
        if note:
            n = description.replace(note.group(), '')
        return n

    def clean_note(self):
        self.description = self.get_note(self.description)

    @staticmethod
    def get_section(description):
        s = description
        section = re.search('(See Section.*)((for further explanation\\.)|(\\)\\.))', description, re.IGNORECASE)
        if section:
            s = description.replace(section.group(), '')
        return s

    def clean_section(self):
        self.description = self.get_section(self.description)

    @staticmethod
    def get_may_be_present(description):
        m = description
        may = re.search('(May be present otherwise\\.)', description, re.IGNORECASE)
        if may:
            m = description.replace(may.group(), '')
        return m

    def clean_may_be_present(self):
        self.description = self.get_may_be_present(self.description)

    @staticmethod
    def get_rule_class(description):
        r = description
        req = re.search('(Required.*)((\\.)|($))', description)
        shall = re.search('(Shall.*)((\\.)|($))', description)
        if req:
            r = req.group()
        elif shall:
            r = shall.group()
        return r

    def set_only_rule_def(self):
        self.description = self.get_rule_class(self.description)

    # @staticmethod
    # def find_req(attribute_dict):
    #     required_att = []
    #     for a in attribute_dict:
    #         if re.search(r'Required', a.description):
    #             required_att.append(a)
    #     return required_att

    # @staticmethod
    # def remove_required(a, b):
    #     new_list = [i for i in a if i not in b]
    #     return new_list
    #
    # # TODO: investigate if it's  better to do one single
    # # method with an if loop, or a dictionary with keywords or different methods for each
    #
    # @staticmethod
    # def find_shall(cond_shall, cond_req):
    #     rules_shall = []
    #     for i in cond_shall:
    #         text = re.findall(r'Shall.*$', i.description)
    #         if text:
    #             if i not in cond_req:
    #                 rules_shall.append(i)
    #     return rules_shall
