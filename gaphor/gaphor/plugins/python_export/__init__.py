import logging
import gi
import os


import xml.etree.ElementTree as ET
import xmi

from gaphor.abc import ActionProvider, Service
from gaphor.core import action, gettext
from gaphor.plugins.xmiexport import exportmodel
from gaphor.ui.filedialog import save_file_dialog
try:
    from gaphor.core import gettext
except ImportError:
    def gettext(s): return s


gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

log = logging.getLogger(__name__)





def python_action(caminho):
    #print("testes", caminho)

    cam = ''
    for c in caminho:
        if c == '\\':
            cam += '/'
        else:
            cam += c

    #print("cam", cam)
    cc = cam[2:]
    #print("cc", cc)
    '''cam = caminho[2:]
    cam.replace("\\", "/")
    print("cammm", cam)'''
    '''tree = ET.parse('teste.xmi')
    root = tree.getroot()'''
    #xmi_obj = xmi.open_file(caminho)
    #xmi_obj.print_details()
    '''xmi_obj = xmi.XMIT(filename=caminho,loglevel=logging.DEBUG)
    xmi_obj.open()'''
    '''f = open("C:/Users/Kellen Moura/Desktop/teste.xmi.txt", "r")
    f.close()
    print("oiiiiiii")'''
    '''f = open(cc, "r")
    print ("abriu")
    print(f.read())
    f.close()
    print("fechou")'''
    l = []
    l2 = []

    with open(caminho, "r") as arquivo:
        lines = arquivo.readlines()
        for line in lines:
            if(line.find("<UML:Package") != -1):
                package_id = ''
                name = ''
                visibility = ''

                i = line.find("id=\"") + 4
                while (line[i] != '\"'):
                    package_id += line[i]
                    i += 1

                i = line.find("name=\"") + 6
                while (line[i] != '\"'):
                    name += line[i]
                    i += 1

                i = line.find("visibility=\"") + 12
                while (line[i] != '\"'):
                    visibility += line[i]
                    i += 1

                dic = {}
                dic['id'] = package_id
                dic['name'] = name
                dic['visibility'] = visibility
                dic['class'] = []

                has_package_id = False
                for dic_pkg in l:
                    if dic_pkg['id'] == package_id:
                        has_package_id = True
                if not has_package_id:
                    l.append(dic)

                
            if (line.find("<UML:Class XMI:id=") != -1):
                class_id = ''
                class_name = ''
                class_abstract = ''
                
                i = line.find("\"") + 1
                while (line[i] != '\"'):
                    class_id += line[i]
                    i += 1

                i = line.find("name=\"") + 6
                while (line[i] != '\"'):
                    class_name += line[i]
                    i += 1

                i = line.find("isAbstract=\"") + 12
                while (line[i] != '\"'):
                    class_abstract += line[i]
                    i += 1

                classes = {}
                classes['id'] = class_id
                classes['name'] = class_name
                classes['abstract'] = class_abstract
                classes['property'] = []
                dic['class'].append(classes)
            
            if (line.find("<UML:Property") != -1):
                property_id = ''
                property_isStatic = ''
                property_isOrdered = ''
                property_isUnique = ''
                property_isDerived = ''
                property_isDerivedUnion = ''
                property_isReadOnly = ''
                property_name = ''

                i = line.find("id=\"") + 4
                while (line[i] != '\"'):
                    property_id += line[i]
                    i += 1

                i = line.find("name=\"") + 6
                while (line[i] != '\"'):
                    property_name += line[i]
                    i += 1


                i = line.find("isStatic=\"") + 10
                while (line[i] != '\"'):
                    property_isStatic += line[i]
                    i += 1          

                i = line.find("isOrdered=\"") + 11
                while (line[i] != '\"'):
                    property_isOrdered += line[i]
                    i += 1

                i = line.find("isUnique=\"") + 10
                while (line[i] != '\"'):
                    property_isUnique += line[i]
                    i += 1

                i = line.find("isDerived=\"") + 11
                while (line[i] != '\"'):
                    property_isDerived += line[i]
                    i += 1

                i = line.find("isDerivedUnion=\"") + 16
                while (line[i] != '\"'):
                    property_isDerivedUnion += line[i]
                    i += 1

                i = line.find("isReadOnly=\"") + 12
                while (line[i] != '\"'):
                    property_isReadOnly += line[i]
                    i += 1

                properties = {}
                properties['id'] = property_id
                if property_name == "Property XMI:id=":
                    properties['name'] = ""
                else:
                    properties['name'] = property_name
                #properties['name'] = property_name
                properties['isStatic'] = property_isStatic
                properties['isOrdered'] = property_isOrdered
                properties['isUnique'] = property_isUnique
                properties['isDerived'] = property_isDerived
                properties['isDerivedUnion'] = property_isDerivedUnion
                properties['isReadOnly'] = property_isReadOnly
                classes['property'].append(properties)

            if (line.find("<UML:Generalization XMI:id=") != -1):
                relacao_id = ''
                
                i = line.find("\"") + 1
                while (line[i] != '\"'):
                    relacao_id += line[i]
                    i += 1
            
                relacoes = {}
                relacoes['id'] = relacao_id
                relacoes['obj'] = []
                l2.append(relacoes)

            if (line.find("<UML:Class XMI:idref=") != -1):
                obj_relacionados = ''
                i = line.find("\"") + 1
                while (line[i] != '\"'):
                    obj_relacionados += line[i]
                    i += 1
                if l2:
                    relacoes['obj'].append(obj_relacionados)
                
    '''print("\n", l)
    print()
    print("L222", l2)
    print()'''

    
    dic_id_name = {}
    dic_id_property = {}
    for dic_package in l:
        for dic_class in dic_package['class']:
            dic_id_name[dic_class['id']] = dic_class['name']
            i = 0
            dic_id_property[dic_class['id']] = []
            while i < len(dic_class['property']): #talvez fazer um if dicpropert diferente de lista
                if dic_class['property'] != '':
                    dic_id_property[dic_class['id']].append(dic_class['property'][i]['name'])
                i += 1
    #print()


    dic_heranca = {}
    for dic_l2 in l2:
        if dic_l2['obj'][1] in dic_heranca:
            dic_heranca[dic_l2['obj'][1]].append(dic_l2['obj'][0])
        else:
            dic_heranca[dic_l2['obj'][1]] = []
            dic_heranca[dic_l2['obj'][1]].append(dic_l2['obj'][0])

    '''print()
    print("Loiii", dic_id_property)
    print()
    print("liieeee", dic_heranca)'''

    dic_property_all = {}
    for dic_key_heranca in dic_heranca:
        dic_property_all[dic_key_heranca] = dic_id_property[dic_key_heranca]
        for herancas in dic_heranca[dic_key_heranca]:           
            dic_property_all[dic_key_heranca] += dic_id_property[herancas]

    #print()
    #print("aaaaaa", dic_property_all)   


    aux2 = False
    print("CA1", caminho)
    caminhoc = caminho[0:-3] + 'py'
    print("CA2", caminhoc)

    with open(caminhoc, "w") as arquivo_py:
        for dic_package in l:
            for dic_class in dic_package['class']:

                i = 0
                aux = False
                if aux2 == True:
                    arquivo_py.writelines("\n")
                aux2 = True
                lcon = []
                while i < len(l2):
                    if dic_class['id'] == l2[i]['obj'][1] and dic_class['id'] not in lcon:
                        lcon.append(dic_class['id'])
                        aux = True
                        aux_heranca = ''
                        for heranca in dic_heranca[l2[i]['obj'][1]]:
                            aux_heranca += dic_id_name[heranca] + ', '
                        arquivo_py.writelines("class " + dic_class['name'] + "(" + aux_heranca[0:-2] + "):\n")
                        aux_parametros = ''
                        for parametro in dic_property_all[dic_class['id']]:
                            #print("para ", parametro)
                            if parametro != '':
                                aux_parametros += parametro + ', '
                        #print("oii", aux_parametros, "fim")
                        if (aux_parametros != ''):
                            arquivo_py.writelines("\tdef __init__(self, " + aux_parametros[0:-2]  + "):\n")
                            arquivo_py.writelines("\t\tsuper().__init__(" + aux_parametros[0:-2]  + ")\n")
                        else:
                            arquivo_py.writelines("\tdef __init__(self): \n \t\tpass")

                        '''for dic_property in dic_class['property']:
                            arquivo_py.writelines(", " + dic_property['name'])
                            cont = 0
                            
                            if len(dic_id_property[l2[i]['obj'][0]]) == 1:
                                arquivo_py.writelines(", ")
                                while cont < len(dic_id_property[l2[i]['obj'][0]]):
                                    arquivo_py.writelines(dic_id_property[l2[i]['obj'][0]][cont])
                                    cont += 1
                            if len(dic_id_property[l2[i]['obj'][0]]) >= 2:
                                arquivo_py.writelines(", ")

                                x = 1
                                while cont < len(dic_id_property[l2[i]['obj'][0]]):
                                    arquivo_py.writelines(dic_id_property[l2[i]['obj'][0]][cont])
                                    if x < len(dic_id_property[l2[i]['obj'][0]]):
                                        arquivo_py.writelines(", ")
                                    x += 1
                                    cont += 1
                        arquivo_py.writelines("):\n")
                        cont = 0'''

                        
                        #arquivo_py.writelines("\t\tsuper().__init__(" + aux_parametros[0:-2]  + ")\n")

                        '''if len(dic_id_property[l2[i]['obj'][0]]) == 1:
                            while cont < len(dic_id_property[l2[i]['obj'][0]]):
                                arquivo_py.writelines(dic_id_property[l2[i]['obj'][0]][cont])
                                cont += 1
                        if len(dic_id_property[l2[i]['obj'][0]]) >= 2:
                            x = 1
                            while cont < len(dic_id_property[l2[i]['obj'][0]]):
                                arquivo_py.writelines(dic_id_property[l2[i]['obj'][0]][cont])
                                if x < len(dic_id_property[l2[i]['obj'][0]]):
                                    arquivo_py.writelines(", ")
                                x += 1
                                cont += 1
                        arquivo_py.writelines("):\n")'''

                    i += 1

                if aux == False:
                    arquivo_py.writelines("class " + dic_class['name'] + ":\n")

                    arquivo_py.writelines("\tdef __init__(self")
                    #print("aq ", dic_class['property'])
                    if len(dic_class['property']) > 0:
                        for dic_property in dic_class['property']:
                            if dic_property['name'] != '':
                                arquivo_py.writelines(", " + dic_property['name'])
                        arquivo_py.writelines("):\n")
                    else:
                        arquivo_py.writelines("):\n")
                        arquivo_py.writelines("\t\tpass")



                for dic_property in dic_class['property']:
                    if dic_property['name'] != '':
                        arquivo_py.writelines("\t\tself." + dic_property['name'] + " = ''\n")

                for dic_property in dic_class['property']:
                    arquivo_py.writelines("\n")
                    if dic_property['isReadOnly'] == "False" and dic_property['name'] != '':
                        arquivo_py.writelines("\tdef set" + dic_property['name'] + "(self, " + dic_property['name'] + "): \n")
                        arquivo_py.writelines("\t\tself." + dic_property['name'] + " = ''\n")
                    
                    if dic_property['isStatic'] == "True":
                        arquivo_py.writelines("\tdef get" + dic_property['name'] + "(self, " + dic_property['name'] + "): \n")
                        arquivo_py.writelines("\t\treturn self." + dic_property['name'] + " = ''\n")


                '''if dic_property['name']:
                    arquivo_py.writelines("\t" + dic_property['name'] + " = \'\'\n")
                if dic_property['isReadOnly'] == "False":
                    #ReadOnly false = criar método set
                    #arquivo_py.writelines("\t" + dic_property['isReadOnly'] + " = \'\'\n")
                else:
                    #ReadOnly true = não criar método set
                if dic_property['isStatic'] == "False":
                    #isStatic false = não criar método get
                else:
                    #isStatic true = criar método get'''
    #deletar arquivo aqui
    
    os.remove(caminho)
    #with open(caminhoc, "r") as arquivo_py:
    #    print(arquivo_py.readlines())








class PyExport(Service, ActionProvider):

    def __init__(self, element_factory, file_manager, export_menu):
        self.element_factory = element_factory
        self.file_manager = file_manager
        export_menu.add_actions(self)

    def shutdown(self):
        pass

    @action(
        name="file-export-py",
        label=gettext("Export to python"),
        #tooltip=gettext("Every application should have a Hello world plugin!"),
        tooltip=gettext("Export model to Python"),
    )



    def execute(self):
        filename = self.file_manager.filename
        #print("fileeee", filename)
        filename = filename.replace(".gaphor", ".xmi") if filename else "model.xmi"
        filename = save_file_dialog(
            gettext("Export model to XMI file"),
            filename=filename,
            extension=".xmi",
            filters=[(gettext("All XMI Files"), ".xmi", "text/xml")],
        )
        #print("fileeee2", filename)

        if filename and len(filename) > 0:
            log.debug(f"Exporting Python model to: {filename}")
            export = exportmodel.XMIExport(self.element_factory)
            try:
                export.export(filename)
            except Exception as e:
                log.error(f"Error while saving model to file {filename}: {e}")

        python_action(filename)

 

        #print("teste1", caminho)


    '''def helloworld_action(self):
        main_window = self.main_window
        dialog = Gtk.MessageDialog(
            parent=main_window.window,
            type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            message_format="Every application should have a Hello world plugin!",
        )
        dialog.run()
        dialog.destroy()'''
