import re

class regex_struct_class():
    def __init__(self):
        """Initiating of regex_struct object"""
        self.regex_string = ""
        self.replace_string = ""
        self.input = ""
        self.result_list = []
        self.result = ""
        self.flags = 0
        self.function = "findAll"

    def change_flags(self, flag, switched = True):
        """calculating self.flags"""
        if switched:
            regex_struct.flags |= flag
        else:
            regex_struct.flags = regex_struct.flags & (~flag)


    def calc_result(self, tounicode, additParam = ""):
        """calculating result list of matches and string"""
        self.result = ""
        self.result_list = []
        # findall
        if self.function == "findAll":
            try:
                self.result_list = re.findall(self.regex_string, self.input, flags=self.flags)
            except:
                self.result_list = []
                self.result = "<b>Error in Regular Expression</b>"
            else:
                if tounicode:
                    tempstr = u"["
                    for i in self.result_list:
                        tempstr += "u'" + i + "', "
                    if tempstr != u"[":
                        tempstr = tempstr[:-2]
                    tempstr += u']'
                    self.result = tempstr
                else:
                    self.result = str(self.result_list)
            return

        if self.function == "search":
            try:
                self.result = re.search(self.regex_string, self.input, flags=self.flags)
            except:
                self.result_list = ()
                self.result = "<b>Error in Regular Expression</b>"
            else:
                if self.result is None:
                    self.result_list = ()
                    self.result = "String not found"
                else:
                    self.result_list = ()  # to-do: to print groups
                    self.result = "Found!"

        if self.function == "match":
            try:
                self.result = re.match(self.regex_string, self.input, flags=self.flags)
            except:
                self.result_list = ()
                self.result = "<b>Error in Regular Expression</b>"
            else:
                if self.result is None:
                    self.result_list = ()
                    self.result = "No match"
                else:
                    self.result_list = ()  # to-do: to print groups
                    self.result = "Match found!"


        if self.function == "sub":
            try:
                if additParam != "":
                    self.result = re.sub(self.regex_string, self.replace_string, self.input, int(additParam))
                else:
                    self.result = re.sub(self.regex_string, self.replace_string, self.input)
            except:
                self.result_list = []
                self.result = "<b>Error in Regular Expression</b>"
            return

        if self.function == "split":
            try:
                if additParam != "":
                    self.result_list = re.split(self.regex_string, self.input, int(additParam), flags=self.flags)
                else:
                    self.result_list = re.split(self.regex_string, self.input, flags=self.flags)
            except:
                self.result_list = []
                self.result = "<b>Error in Regular Expression</b>"
            else:
                if tounicode:
                    tempstr = u"["
                    for i in self.result_list:
                        tempstr += "u'" + i + "', "
                    if tempstr != u"[":
                        tempstr = tempstr[:-2]
                    tempstr += u']'
                    self.result = tempstr
                else:
                    self.result = str(self.result_list)
            return


regex_struct = regex_struct_class()