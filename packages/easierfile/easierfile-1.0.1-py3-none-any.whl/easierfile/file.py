import os

class File:
    def __init__(self, filePath):
        self.__m_filePath = filePath
        self.__m_dirPath = os.path.dirname(self.__m_filePath)
        if os.path.exists(self.__m_dirPath) == False:  # If the directory of the file path does not exist, it will be created.
            os.mkdir(self.__m_dirPath)
        try:  # If the file does not exist, it will be created.
            self.__m_file = open(self.__m_filePath, "x")
        except:
            pass
        else:
            self.__m_file.close()

    @property
    def content(self):
        self.__m_file = open(self.__m_filePath, "r")
        self.__m_content = self.__m_file.read()
        self.__m_file.close()
        return self.__m_content

    def Rewrite(self,content):
        self.__m_file = open(self.__m_filePath, "w")
        self.__m_file.write(content)
        self.__m_file.close()

    def Append(self,content):
        self.__m_file = open(self.__m_filePath, "a")
        self.__m_file.write(content)
        self.__m_file.close()

    def Delete(self):
        if os.path.exists(self.__m_filePath):
            os.remove(self.__m_filePath)