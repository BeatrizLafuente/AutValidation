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
        # Match until the end of the sentence
        section = re.search('(See Section)(([^\\)]*[)][^.]*[.])|([^\\)]*[)][^\\)]*[\\)][.])|'
                            '([^\\)]*[))])|([^\\)]*[)][^.]*$))', description, re.IGNORECASE)
        if section:
            s = description.replace(section.group(), '')
        return s

    def clean_section(self):
        self.description = self.get_section(self.description)

    @staticmethod
    def get_may_be_present(description):
        m = description
        may = re.search('((May be present).*\\.)', description, re.IGNORECASE)
        req = re.search('(Required)', description, re.IGNORECASE)
        if req:
            if may:
                m = description.replace(may.group(), '')
        return m

    def clean_may_be_present(self):
        self.description = self.get_may_be_present(self.description)

    @staticmethod
    def get_num_items_present(description):
        p = description
        num = re.search('(One|zero)( or )(one|more)( items shall be)[^.*]*[.]', description, re.IGNORECASE)
        if num:
            p = description.replace(num.group(), '')
        return p

    def clean_num_items_present(self):
        self.description = self.get_num_items_present(self.description)

    @staticmethod
    def get_rule_class(description):
        r = description
        # Search for Required/shall until enumerated values or until the end of the sentence
        req = re.search('((Required)((.*(Enumerated Values).*$)|[^.]*[.]\\s|[^.]*$|.*[.]$))', description)
        if_req = re.search('(if required).*(shall)[^.]*[.]', description, re.IGNORECASE)
        shall = re.search('((Shall)((.*(Enumerated values).*$)|[^.]*[.]\\s|[^.]*$|.*[.]$))', description, re.IGNORECASE)
        if req:
            r = req.group()
        elif if_req:
            r = if_req.group()
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
