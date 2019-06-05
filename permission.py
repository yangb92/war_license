import zipfile
import xml.etree.ElementTree as ET
from xml.dom import minidom

ET.register_namespace('', "http://java.sun.com/xml/ns/javaee")
ET.register_namespace('xsi', "http://www.w3.org/2001/XMLSchema-instance")

EFilter = ET.Element('filter')
EFilter_name = ET.SubElement(EFilter,'filter-name')
EFilter_name.text="License"
EFilter_clazz = ET.SubElement(EFilter,'filter-class')
EFilter_clazz.text="com.yangb.cer.WebLicense"

EFilter_Mapping = ET.Element('filter-mapping')
EFilter_name2 = ET.SubElement(EFilter_Mapping,'filter-name')
EFilter_name2.text="License"
EUrl_pattern = ET.SubElement(EFilter_Mapping,'url-pattern')
EUrl_pattern.text="/*"

# 发送jar包
def sendJar(warpath):
    with zipfile.ZipFile(warpath,'a') as war:
        war.write("WEB-INF/lib/cer-1.0.jar")

def writeWebXml(warpath):    
    with zipfile.ZipFile(warpath,'a') as war:
        war.write("WEB-INF/web.xml")

def makeWebXml(warpath):
    with zipfile.ZipFile(warpath, 'r') as war:
        with war.open("WEB-INF/web.xml",'r') as webxml:
            xml = ET.fromstring(webxml.read())
            xml.insert(0,EFilter_Mapping)
            xml.insert(0,EFilter)
            dom = minidom.parseString(ET.tostring(xml))
            with open("WEB-INF/web.xml",'w') as f:
                dom.writexml(f, "", "\t", '\n', 'utf-8')


def del_file(zipname,outname,filename):
    zin = zipfile.ZipFile (zipname, 'r')
    zout = zipfile.ZipFile (outname, 'w')
    for item in zin.infolist():
        buffer = zin.read(item.filename)
        if (item.filename != filename):
            zout.writestr(item, buffer)
    zout.close()
    zin.close()

if __name__ == '__main__':
    warname = 'ygzw_wsbsdt_front.war'
    newname = 'License_' + warname
    del_file(warname,newname,'WEB-INF/web.xml')
    makeWebXml(warname)
    writeWebXml(newname)
    sendJar(newname)
    