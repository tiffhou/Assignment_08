#------------------------------------------#
# Title: CD_Inventory.py
# Desc: Assignnment 08 - Working with classes to create CD Inventory script
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, created file
# DBiesinger, 2030-Jan-01, added pseudocode to complete assignment 08
# THou, 2020-Mar-13: updated header
# THou, 2020-Mar-13: added to CD class; added save and load functions;
#   added DataProcessor class and functions; added IO functions;
#   updated main body of script
# THou, 2020-Mar-14: added error handling & formatting
# THou, 2020-Mar-15: added formatting, doc strings, tweaked error handling
# THou, 2020-Mar-16: added additional error handling; updated docstrings
#------------------------------------------#

# -- DATA -- #
strFileName = 'CDInventory.txt'
lstInv = [] #list of CD objects comprising the inventory
strChoice = '' #user menu choice
strInput = '' #user input
intID = ''
strTitle = ''
strArtist = ''


class CD:
    """Stores data about a CD:
    
    properties:
        cd_id (int): the ID of the CD; private
        cd_title (str): the title of the CD; private
        cd_artist (str): the artist of the CD; private
    """

    #--- Constructor ---#
    def __init__(self, cdid, cdtitle, cdartist): 
        """ Constructor for a CD instance
        
        Args:
            self
            cdid (int): CD ID
            cdtitle (str): CD title
            cdartist (str): CD artist
        
        Return:
            None
        """
        self.__id = cdid
        self.__title = cdtitle
        self.__artist = cdartist

    #--- Properties ---#
    @property
    def id(self):
        """ Getter for CD ID
        
        Args:
            self
        
        Return:
            __id (str): the private CD ID attribute
        """
        return self.__id
    
    @id.setter
    def id(self, value):
        """ Setter for the CD ID; enforces the integer type  
        
        Args:
            self
            
        Raises:
            ValueError: if ID is not an integer
            
        Return:
            None
        """
        try:
            value = int(value)
            self.__id = value
        except ValueError:
            raise ValueError('ID must be an integer') # raise ValueError to provide more context

    @property
    def title(self):
        """ Getter for CD title
        
        Args:
            self
            
        Return:
            __title (str): the private CD title attribute
        """
        return self.__title

    @title.setter
    def title(self):
        """ Setter for CD title; currently empty"""
        # add enforcement and validation here in future
        pass

    @property
    def artist(self):
        """ Getter for CD artist
        
        Args:
            Self
        
        Return:
            __artist (str): the private CD artist attribute
        """
        return self.__artist
    
    @artist.setter
    def artist(self):
        """ Setter for CD artist; currently empty"""
        # add enforcement and validation here in future
        pass



# -- PROCESSING -- #
class FileIO:
    """Processes data to and from file:
    
    properties:
        None
    
    Functions:
        load_inventory(file_name): -> (a list of CD objects)
        save_inventory(file_name, lst_Inventory): -> None
    """

    # Code to process data from a file
    @staticmethod
    def load_inventory(file_name):
        """overwrite the current inventory
        
        Args:
            file_name (str): name of the file to be loaded from
        
        Exceptions:
            FileNotFoundError: if the file cannot be found
            
        Return:
            table (list): the current inventory table loaded with data from the file
        """
        print('Loading data from {}\n.\n.\n.\n'.format(strFileName))
        try:
            with open(file_name, 'r') as fileObj:
                table = []
                for line in fileObj:
                    data = line.strip().split(',')
                    newCD = CD(int(data[0]), data[1], data[2])
                    table.append(newCD)
            if len(table) > 0:
                print('Inventory loaded from {}'.format(file_name))
            else:
                print('No data in {} to be loaded.'.format(file_name))
            return table
        except FileNotFoundError:
            print('{} not found. No data loaded.'.format(file_name))

    # Code to process data to a file
    @staticmethod
    def save_inventory(file_name, inventory):
        """write the current inventory to the save file
        
        Args:
            file_name (str): the name of the file to save to
            inventory (list): the current inventory to be written to file
        
        Return:
        """
        lstValues = []
        with open(file_name, 'w') as fileObj:
            for cd in inventory:
                lstValues = [cd.id, cd.title, cd.artist]
                lstValues[0] = str(lstValues[0])
                fileObj.write(','.join(lstValues) + '\n')
        print('Inventory saved to {}'.format(file_name))



class DataProcessor:
    """Processes data in memory
    
    Properties:
        None
    
    Methods:
        get_int(strVal): -> intVal
        delete_entry(strID, lstInv): -> table
        generate_cd_id(lstInv): -> cd_id
    """

    @staticmethod
    def get_int(strVal):
        """Casts the user input as an integer
        
        Args:
            strVal (str): the value inputted by the user
        
        Exceptions:
            ValueError: if the user input cannot be cast as an integer
        
        Returns:
            intVal (int): the value cast as an integer
        """
        try:
            intVal = int(strVal)
            return intVal
        except ValueError:
            print('Input must be an integer')
            return None

    @staticmethod
    def delete_entry(delID, table):
        """Deletes a CD entry based on inputted ID (delID).
        
        Args:
            delID (int): the ID inputted by the user for the entry to be deleted
            table (list): the current inventory list
        
        Raises:
            TypeError: if the list has not been populated before and is a NoneType
            
        Return:
            table (list): the updated inventory list
        """
        intRowNr = -1
        blnCDRemoved = False
        try:
            for cd in table:
                intRowNr += 1
                if cd.id == delID:
                    del cd
                    del table[intRowNr]
                    blnCDRemoved = True
                    break
            if blnCDRemoved:
                print('The CD was removed.\n')
            else:
                print('Could not find this CD!\n')
        except TypeError:
            print('No entries in table to delete.')
        return table

    @staticmethod
    def generate_cd_id(table):
        """generates a CD ID, for uniqueness in current inventory
        
        Args:
            table (list): the current inventory table
        
        Return:
            cd_id (int): the auto-generated CD ID
        """
        cd_id = 1
        if table is not None:
            for cd in table:
                if cd.id == cd_id:
                    cd_id += 1
        return cd_id



# -- PRESENTATION (Input/Output) -- #
class IO:
    """Presenting outputs and collecting inputs to and from the user
    
    Properties:
        
    Methods:
        show_menu()
        menu_choice()
        show_inventory(lstInv)
        add_cd(intID, lstInv) --> table
    """

    # Code to show menu to user
    @staticmethod
    def show_menu():
        """show the menu choices to the user
        
        Args:
            None
        
        Return:
            None
        """
        print('\n\n[[  CD Inventory Menu  ]]\n')
        print('[i]\tShow current inventory\n[a]\tAdd CD to inventory\n[d]\tDelete CD from inventory\n[s]\tSave inventory to file\n[l]\tLoad inventory from file\n[x]\tExit CD Inventory')

    # Code to captures user's choice
    @staticmethod
    def menu_choice():
        """get the menu choice from user & checks for valid choi
        
        Args:
            None
        
        Return:
            choice (str): the validated choice
        """
        choice = None
        while choice not in ['i', 'a', 'd', 's', 'l', 'x']:
            choice = input('Select your option: ').strip().lower()
        print()
        return choice

    # Code to display the current data on screen
    @staticmethod
    def show_inventory(table):
        """Displays current inventory table.
        
        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.
        
        Raises:
            TypeError: if the list has not been populated before and is a NoneType
        
        Returns:
            None.
        """
        try:
            if len(table) > 0:
                print('======= The Current Inventory: =======')
                print('ID\tCD Title (by: Artist)\n')
                for cd in table:
                    print('{}\t{} (by: {})'.format(cd.id, cd.title, cd.artist))
                print('======================================')
            else:
                print('No entries in inventory table to show.\n')
        except TypeError:
            print('No entries in inventory table to show.\n')


    # Code to get CD data from user and add to inventory table
    @staticmethod
    def add_cd(cd_id, table):
        """get the CD fields from the user
        
        Args:
            cd_id (int): the auto-generated CD ID
        
        Exceptions:
            AttributeError: if the list is a NoneType and cannot be appended to
        
        Returns:
            table (list): the updated inventory list
        """
        newCD = ''
        print('CD ID: ', cd_id)
        cd_title = input('CD\'s title: ').strip()
        cd_artist = input('CD Artist\'s name: ').strip()
        newCD = CD(int(cd_id), cd_title, cd_artist)
        print(newCD.id)
        try:
            table.append(newCD)
        except AttributeError: #can't append if list is None
            table = [newCD]
        print('\nCD added to inventory.\n')
        return table



# -- Main Body of Script -- #

# Load data from file into a list of CD objects on script start
lstInv = FileIO.load_inventory(strFileName)
if lstInv is not None:
    IO.show_inventory(lstInv)


while True:
    IO.show_menu()
    strChoice = IO.menu_choice()


# Display menu to user
    # show user current inventory
    if strChoice == 'i':
        IO.show_inventory(lstInv)
        continue


    # let user add data to the inventory
    elif strChoice == 'a':
        #get unique CD ID
        intID = DataProcessor.generate_cd_id(lstInv)
        
        #pass CD ID into add_cd()
        lstInv = IO.add_cd(intID, lstInv)
        IO.show_inventory(lstInv)
        continue


    # let user delete a CD
    elif strChoice == 'd':
        IO.show_inventory(lstInv)
        #get int ID of entry to delete
        strInput = input('Which ID would you like to delete? ')
        intID = DataProcessor.get_int(strInput)
        
        #pass ID of entry into delete_entry()
        if intID is not None:
            lstInv = DataProcessor.delete_entry(intID, lstInv)
            IO.show_inventory(lstInv)
        continue  # start loop back at top.


    # let user save inventory to file
    elif strChoice == 's':
        strInput = input('Overwrite the data in {}? (\'yes\' to continue)\n'.format(strFileName)).strip().lower()
        if strInput == 'yes':
            FileIO.save_inventory(strFileName, lstInv)
        continue


    # let user load inventory from file
    elif strChoice == 'l':
        #check if there is data to be overwritten, then load inventory
        try:
            if len(lstInv) > 0:
                IO.show_inventory(lstInv)
                strInput = input('Are you sure you want to overwrite the existing inventory? (enter \'yes\' to continue)\n').strip().lower()
                if strInput == 'yes':
                    lstInv = FileIO.load_inventory(strFileName)
                    IO.show_inventory(lstInv)
            else:
                lstInv = FileIO.load_inventory(strFileName)
                IO.show_inventory(lstInv)
        except TypeError: #if lstInv is NoneType
            lstInv = FileIO.load_inventory(strFileName)
            IO.show_inventory(lstInv)
        continue


    # let user exit program
    elif strChoice == 'x':
        print('Thanks for using the CD inventory.')
        break
    
    # restarts menu in case of input error
    else:
        print('Invalid selection. Please try again.')
        continue