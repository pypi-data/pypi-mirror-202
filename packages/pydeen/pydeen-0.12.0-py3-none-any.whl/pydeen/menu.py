"""
    Menu and user input utils
"""

from getpass import getpass

class UserInput:
    def __init__(self, label:str, default:str=None):
        self.label   = label
        self.default = default

    def get_input(self, empty_allowed:bool=False):
        # label
        label = self.label
        if self.default != None:
            label += f" ({self.default}): "
        else:
            label += ": "    
        
        # input loop
        answer = ""
        valid = False
        while valid == False:
            answer = input(label)
            if self.default != None and ( answer == "" or answer == None ):
                answer = self.default
            if answer == "" and empty_allowed == True:
                valid = True
            elif len(answer) > 0:
                valid = True        

        return answer     

    def get_label(self) -> str:
        label = self.label
        if self.default != None:
            label += f" ({self.default}): "
        else:
            label += ": "    
        return label

    def get_password(self, empty_allowed:bool=False):
        # label
        label = self.get_label()    
        
        # input loop
        answer = ""
        valid = False
        while valid == False:
            answer = getpass(prompt=label)
            if self.default != None and ( answer == "" or answer == None ):
                answer = self.default
            if answer == "" and empty_allowed == True:
                valid = True
            elif len(answer) > 0:
                valid = True        

        return answer     

    def get_selection_from_list(self, title:str, entries:list):
        if entries == None or len(entries) == 0:
            return None

        list_entries = {}
        for entry in entries:
            list_entries[entry] = entry

        action = MenuSelection(title, list_entries, False, True).show_menu()  
        if action.is_cancel_entered() == True:
            return None
        else:
            return action.get_selection()          


    def get_input_int(self, min:int=None, max:int=None):
        label = self.label
        if self.default != None:
            label += f" ({self.default}): "
        else:
            label += ": "    
        
        result = None
        answer = None
        while answer == None or answer == "":
            answer = input(label)
            if self.default != None and ( answer == "" or answer == None ):
                answer = self.default

            if answer.isdigit():
                result = int(answer)
                if min != None and min > result:
                    answer = None
                if max != None and max < result:
                    answer = None
            else:
                answer = None    
        return result     

    def get_input_yes_no(self, default_yes:bool=True) -> bool:
        label = self.label
        if default_yes:
            label += f"(Yes/no): "
        else:
            label += f"(yes/No): "

        answer = None
        while answer == None or answer == "":
            answer = input(label)
            if answer == "" or answer == None:
                if default_yes:
                    return True
                else:
                    return False    
            if answer == "Y" or answer == "y":
                return True
            elif answer == "N" or "n":
                return False
            else: 
                answer = None    


class MenuAction:
    def __init__(self, menu, selected, cancel_entered:bool=False, quit_entered:bool=False):
        self.menu = menu
        self.selected = selected
        self.selected_multi = None
        self.cancel_entered = cancel_entered
        self.quit_entered = quit_entered
    
    def is_quit_entered(self) -> bool:
        return self.quit_entered

    def is_cancel_entered(self) -> bool:
        return self.cancel_entered

    def is_selected(self) -> bool:
        if self.selected != None and self.quit_entered == False and self.cancel_entered == False:
            return True
        else: 
            return False

    def get_selection(self):
        return self.selected            

    def set_multi_selection(self, selected:list):
        self.selected_multi = selected

    def is_multi_selection_available(self) -> bool:
        if self.selected_multi != None and len(self.selected_multi) > 0:
            return True
        else:
            return False    

    def get_multi_selection(self) -> list:
        return self.selected_multi

class Menu:

    @staticmethod
    def dict_keys_as_entries(entries:dict) -> dict:
        result = {}
        for key in entries.keys():
            result[key] = key
        return result

    def __init__(self, title:str, subtitle:str=None, quit:bool=False, cancel:bool=True):
        self.title = title
        self.subtitle = subtitle
        self.exit_text = "Quit"
        self.exit_code = "Q"
        self.exit_allowed = quit
        self.cancel_text = "Cancel"
        self.cancel_code = "C"
        self.cancel_allowed = cancel
        self.select_all_code = "A"
        self.select_all_text = "Select all"
        self.unselect_all_code = "D"
        self.unselect_all_text = "Delete all selections"
        self.invert_selection_code = "I"
        self.invert_selection_text = "Invert selection"
        self.confirm_code = "N"
        self.confirm_text = "Confirm current selection and process next step"

    def show_build_separator(self, title:str, separator:str="=", print_it:bool=True) -> str:
        sep = ""
        for _ in range(len(self.title)):
            sep += separator
        if print_it:
            print(sep)
        return sep


    def show_menu(self) -> MenuAction:
        print()
        print(self.title)
        self.show_build_separator(self.title, separator="=")
        if self.subtitle != None and type(self.subtitle) == str and len(self.subtitle) > 0:
            print(self.subtitle)
            self.show_build_separator(self.title, separator="-")
        return None


class MenuSelection(Menu):

    def __init__(self, title:str, entries:dict, subtitle:str=None, quit:bool=False, cancel:bool=True, lower_case:bool=True):
        super().__init__(title=title, subtitle=subtitle, quit=quit, cancel=cancel)
        self.entries = entries
        self.lower_case = lower_case

    def show_menu(self) -> MenuAction:        
        # build menu from given    
        code = []
        text = []
        for key in self.entries.keys():
            entry_text = self.entries[key]
            if len(entry_text) > 0:
                code.append(key)
                text.append(entry_text)

        # menu loop       
        valid = False
        filter = None
        result = None

        while valid == False:
            # print menu
            super().show_menu()
            for index in range(len(text)):
                if filter == None:
                    print(f"{index+1} - {text[index]}")
                else:
                    if text[index].find(filter) >= 0:
                        print(f"{index+1} - {text[index]}")

            if self.cancel_allowed == True:
                print(f"{self.cancel_code} - {self.cancel_text}")

            if self.exit_allowed == True:
                print(f"{self.exit_code} - {self.exit_text}")

            # get user input
            answer = UserInput("\nEnter your selection").get_input()
            if answer.isdigit():
                int_answer = int(answer)
            else:
                int_answer = 0    
                if self.lower_case:
                    answer = answer.upper()

            # check answer
            if answer == self.exit_code:
                result = MenuAction(self, None, False, True)
            elif answer == self.cancel_code:
                result = MenuAction(self, None, True, False)
            elif int_answer > 0 and int_answer <= len(text):
                selected_code = code[int_answer-1]
                result = MenuAction(self, selected_code, False, False)
            elif len(answer) > 2 and answer[0] == "*" and answer[-1] == "*":
                filter = answer[1:-1]
                print("Filter: ", filter)

            if result != None:
                valid = True               
        
        print()
        return result

    def confirm(self, msg:str=None):
        prompt = msg
        if prompt == None:
            prompt = self.title
        
        print()    
        input(f"{prompt} - Please confirm (with Enter)")

class MenuMultiSelection(Menu):

    def __init__(self, title:str, entries:dict, selected:list=[], subtitle:str=None, quit:bool=False, cancel:bool=True, required_selections:int=1, lower_case:bool=True):
        super().__init__(title=title, subtitle=subtitle, quit=quit, cancel=cancel)
        self.entries = entries
        self.selected = selected
        self.lower_case = lower_case
        self.required_selections = required_selections

    def is_selected(self, key) -> bool:
        if key in self.selected:
            return True
        else:
            return False

    def is_valid_key(self, key) -> bool:
        if key in self.entries.keys():
            return True
        else:
            return False


    def selection_toggle(self, key) -> bool:
        if not self.is_valid_key(key):
            return False
        else:
            if self.is_selected(key):
                self.selected.remove(key)
                return False
            else:
                self.selected.append(key)  
                return True  

    def get_valid_index(self, input:str) -> int:
        try:
            int_result = int(input.strip()) - 1
            if int_result > len(self.entries):
                return None
            else:
                return int_result
        except:
            return None    

    def get_multi_index_from_input(self, input:str) -> list:
        # check valid input
        if input == None or len(input) < 2:
            return None

        if input.find("-") < 0 and input.find(",") < 0:
            return 

        # sub strings to check
        checks = []    
        if input.find(",") > 0:
            checks = input.split(",")
        else:
            checks.append(input)

        # build result
        result = []
        for check_input in checks:
            check_input = check_input.strip()
            if check_input.find("-") < 0 and check_input.isdigit():
                int_value = self.get_valid_index(check_input)
                if int_value != None:
                    result.append(int_value)
            elif check_input.find("-") > 0:
                range_bounds = check_input.split("-")
                range_from   = self.get_valid_index(range_bounds[0])
                range_to     = self.get_valid_index(range_bounds[1])
                if range_from != None and range_to != None and range_from < range_to and range_from >= 0:
                    for add_index in range(range_from, range_to+1):
                        result.append(add_index)

        result = list(set(result))
        return result

    def show_menu(self) -> MenuAction:        
        # build menu from given    
        code = []
        text = []
        for key in self.entries.keys():
            entry_text = self.entries[key]
            if len(entry_text) > 0:
                code.append(key)
                text.append(entry_text)

        # check selected
        preselected = self.selected
        self.selected = []
        if preselected != None and len(preselected) > 0:
            for presel_key in preselected:
                if self.is_valid_key(presel_key):
                    self.selected.append(presel_key)

        # menu loop       
        valid = False
        filter = None
        result = None
        lines_max = len(code)

        while valid == False:
            # print menu
            super().show_menu()
            lines_selected = len(self.selected)
            # entry option
            for index in range(len(text)):
                selection_code = code[index]
                if self.is_selected(selection_code):
                    selected_char = '*'
                else:
                    selected_char = ' '
                
                if filter == None:
                    print(f"{selected_char}{index+1} - {text[index]}")
                else:
                    if text[index].find(filter) >= 0:
                        print(f"{selected_char}{index+1} - {text[index]}")

            # multi select options
            print("-------------")
            print(f"{self.select_all_code} - {self.select_all_text}")
            print(f"{self.unselect_all_code} - {self.unselect_all_text}")
            print(f"{self.invert_selection_code} - {self.invert_selection_text} ({lines_selected}/{lines_max})")

            if lines_selected >= self.required_selections:
                print(f"{self.confirm_code} - {self.confirm_text}")

            # print exit options
            if self.cancel_allowed == True:
                print(f"{self.cancel_code} - {self.cancel_text}")

            if self.exit_allowed == True:
                print(f"{self.exit_code} - {self.exit_text}")

            # get user input
            answer = UserInput("\nEnter your selection").get_input()
            if answer.isdigit():
                int_answer = int(answer)
            else:
                int_answer = 0    
                if self.lower_case:
                    answer = answer.upper()

            # check answer
            if answer == self.exit_code:
                result = MenuAction(self, None, False, True)
            elif answer == self.cancel_code:
                result = MenuAction(self, None, True, False)
            elif answer == self.confirm_code and lines_selected >= self.required_selections:
                result = MenuAction(self, None, False, False)
                result.set_multi_selection(self.selected)
            elif answer == self.select_all_code:
                self.selected = code
            elif answer == self.unselect_all_code: 
                self.selected = []
            elif answer == self.invert_selection_code:
                for invert_code in code:
                    self.selection_toggle(invert_code)
            elif int_answer > 0 and int_answer <= len(text):
                selected_code = code[int_answer-1]
                self.selection_toggle(selected_code)
            elif len(answer) > 2 and answer[0] == "*" and answer[-1] == "*":
                filter = answer[1:-1]
                print("Filter: ", filter)
            elif answer.find(",") > 0 or answer.find("-") > 0:
                multi_index = self.get_multi_index_from_input(answer)
                if multi_index != None and len(multi_index) > 0:
                    for index in multi_index:
                        self.selection_toggle(code[index])

            if result != None:
                valid = True               
        
        print()
        return result

    def confirm(self, msg:str=None):
        prompt = msg
        if prompt == None:
            prompt = self.title
        
        print()    
        input(f"{prompt} - Please confirm (with Enter)")



if __name__ == "__main__":
    entries = {
        "selection1" : "selection1",
        "selection2" : "selection2",
        "selection3" : "selection3",
        "selection4" : "selection4",
        "selection5" : "selection5",
    }
    menu = MenuSelection("Testmenue", entries, quit=True)
    action = menu.show_menu()
    if action != None and action.is_selected():
        print("Selected:", action.get_selection())
    else:
        print("Nothing selected. Cancel or Exit.")    