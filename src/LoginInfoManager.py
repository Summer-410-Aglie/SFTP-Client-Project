import xml.etree.ElementTree as ET
import xml.dom.minidom as dom


FILE_PATH: str = "resources/connection_profiles.xml"

class LoginInfoManager:
    def __init__(self, file_name: str = FILE_PATH) -> None:
        self.file_name = file_name

        try: # file exist
            self.tree = ET.parse(self.file_name)
            self.root = self.tree.getroot()
        except (ET.ParseError, FileNotFoundError): # file does not exist or wrong format
            self.root = ET.Element('root')
            self.tree = ET.ElementTree(self.root)
            self.tree.write(self.file_name)
        pass

    def addLoginInfo(self, user_name: str, host: str, password: str) -> None:
        login_info = {"username": user_name, "host": host, "password": password}
        for login_element in self.root.findall('login'): # checks if the login info already exist
            xml_info = {child.tag: child.text for child in login_element}
            if xml_info == login_info:
                return False
            pass
        login_element = ET.SubElement(self.root, 'login')
        for key, value in login_info.items(): # adds the login info to the xml tree
            ET.SubElement(login_element, key).text = value
            pass

        self.generateXml()
        return True
        pass

    def getAllLoginInfo(self) -> list:
        login_infos = list()

        for login_element in self.root.findall('login'):
            info = {child.tag: child.text for child in login_element}
            login_infos.append(info)
            pass
        return login_infos
        pass

    def deleteLoginInfo(self, login_info) -> bool:
        for login_element in self.root.findall('login'):
            xml_info = {child.tag: child.text for child in login_element}
            if xml_info == login_info: # checks if they both match
                self.root.remove(login_element)
                self.generateXml()
                return True # found and deleted
            pass
        return False # not found
        pass

    def generateXml(self) -> None:
        xml_string = ET.tostring(self.root)
        parsed_xml = dom.parseString(xml_string)
        pretty_xml = parsed_xml.toprettyxml(indent='\t')
        pretty_xml = '\n'.join([line for line in pretty_xml.split('\n') if line.strip()])
        with open(self.file_name, 'w') as writer:
            writer.write(pretty_xml)
        pass

    pass