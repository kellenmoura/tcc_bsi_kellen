import logging
import gi
import os


import xml.etree.ElementTree as ET
import xmi
import xml

from gaphor.abc import ActionProvider, Service
from gaphor.core import action, gettext
from gaphor.plugins.xmiexport import exportmodel
from gaphor.ui.filedialog import save_file_dialog
from gaphor.ui.filemanager import FileManager
from gaphor.storage.xmlwriter import XMLWriter
from gaphor.storage import storage, verify
from gaphor.ui.gidlethread import GIdleThread, Queue



#print("GETTTT", FileManager.get_filename)


try:
    from gaphor.core import gettext
except ImportError:
    def gettext(s): return s


gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

log = logging.getLogger(__name__)


def alloy_action(caminho):
    print("cmainho", caminho)
    cam = ''
    for c in caminho:
        if c == '\\':
            cam += '/'
        else:
            cam += c

    cc = cam[2:]
    caminhoc = caminho[0:-3] + 'txt'

    
    tree = ET.parse(caminho)
    root = tree.getroot()
    root.tag
    root.attrib
   
    l = []

    dic = {}
    dic2 = {}
    dic3 = {}
    dic4 = {}
    dic5 = {}
    dic6 = {}
    dic7 = {}
    dic8 = {}
    dicprop2 = {}
    #print("NOME DO ARQUIVO:")
    for module_name in root.findall("./{http://gaphor.sourceforge.net/model}Package/{http://gaphor.sourceforge.net/model}name/{http://gaphor.sourceforge.net/model}val"):
        #print("Modulo", module_name.text )
        dic['module'] = module_name.text
    l.append(dic)
    #print("\n")
    #print("PROPRIEDADES:")
    i = 0
    for property_id in root.findall("./{http://gaphor.sourceforge.net/model}Property"):
        #print("Property", property_id.attrib)
        propertylst = []
        dic2['property'  + str(i)] = []
        properties = {}
        properties['property_id'] = property_id.attrib
        prop2id = property_id.attrib['id']

        for class_id in property_id.findall("./{http://gaphor.sourceforge.net/model}type/{http://gaphor.sourceforge.net/model}ref"):
            #print("class_id", class_id.attrib)
            properties['class_id'] = class_id.attrib


        for lowerval in property_id.findall("./{http://gaphor.sourceforge.net/model}lowerValue/{http://gaphor.sourceforge.net/model}val"):
            #print("lowerval", lowerval.text)
            properties['lowerval'] = lowerval.text


        for upperval in property_id.findall("./{http://gaphor.sourceforge.net/model}upperValue/{http://gaphor.sourceforge.net/model}val"):
            #print("upperval", upperval.text)
            properties['upperval'] = upperval.text


        for atributos_clas in property_id.findall("./{http://gaphor.sourceforge.net/model}name/{http://gaphor.sourceforge.net/model}val"):
            #print("atributos_clas", atributos_clas.text)
            properties['atributos_clas'] = atributos_clas.text

        for cid_atributo in property_id.findall("./{http://gaphor.sourceforge.net/model}class_/{http://gaphor.sourceforge.net/model}ref"):
            #print("cid_atributo", cid_atributo.attrib)
            properties['cid_atributo'] = cid_atributo.attrib

        for typevalue in property_id.findall("./{http://gaphor.sourceforge.net/model}typeValue/{http://gaphor.sourceforge.net/model}val"):
            #print("typevalue", typevalue.text)
            properties['typevalue'] = typevalue.text

        for assoc_id in property_id.findall("./{http://gaphor.sourceforge.net/model}association/{http://gaphor.sourceforge.net/model}ref"):
            #print("assoc_id", assoc_id.attrib)
            properties['assoc_id'] = assoc_id.attrib

        #para OntoUML
        for type_n in property_id.findall("./{http://gaphor.sourceforge.net/model}type/{http://gaphor.sourceforge.net/model}ref"):
            dicprop2[prop2id] = type_n.attrib['refid']

        dic2['property' + str(i)].append(properties)
        propertylst.append(dic2)
        i += 1
        #print("\n")



    l.append(propertylst)


    i = 0
    #print("ASSOCIAÇÕES:")
    auxassoc = False
    for id_assoc in root.findall("./{http://gaphor.sourceforge.net/model}Association"):
        #print("id_assoc", id_assoc.attrib)
        auxassoc = True
        associationlst = []
        dic3['association'  + str(i)] = []
        associations = {}
        associations['association_id'] = id_assoc.attrib
        
        for id_prop in id_assoc.findall("./{http://gaphor.sourceforge.net/model}memberEnd/{http://gaphor.sourceforge.net/model}reflist/{http://gaphor.sourceforge.net/model}ref"):
            #print("id_prop", id_prop.attrib)
            associations['id_prop'] = id_prop.attrib
        dic3['association' + str(i)].append(associations)
        associationlst.append(dic3)
        i += 1
        #print("\n")

    if auxassoc == True:
        l.append(associationlst)
    else:
        associationlst = []
        l.append(associationlst)

    i = 0
    #print("CLASSES:")
    auxclasses = False
    for class_id in root.findall("./{http://gaphor.sourceforge.net/model}Class"):
        auxclasses = True
        classelst = []

        #print("class_id", class_id.attrib)
        dic4['classes'  + str(i)] = []
        classes = {}
        classes['class_id'] = class_id.attrib

        for class_name in class_id.findall("./{http://gaphor.sourceforge.net/model}name/./{http://gaphor.sourceforge.net/model}val"):
            #print("class_name", class_name.text)
            classes['class_name'] = class_name.text
        dic4['classes' + str(i)].append(classes)
        classelst.append(dic4)
        i += 1
        
    if auxclasses == True:
        l.append(classelst)
    else:
        classelst = []
        l.append(classelst)

    #print("\n")

    i = 0
    #print("OPERAÇÕES:")
    auxop = False
    for id_operation in root.findall("./{http://gaphor.sourceforge.net/model}Operation"):
        #print("id_operation", id_operation.attrib)
        auxop = True
        operationlst = []
        dic5['operation'  + str(i)] = []
        operations = {}
        operations['operation_id'] = id_operation.attrib
        
        for id_prop in id_operation.findall("./{http://gaphor.sourceforge.net/model}class_/{http://gaphor.sourceforge.net/model}ref"):
            #print("id_prop", id_prop.attrib)
            operations['id_prop'] = id_prop.attrib

        for id_prop in id_operation.findall("./{http://gaphor.sourceforge.net/model}name/{http://gaphor.sourceforge.net/model}val"):
            #print("id_prop", id_prop.text)
            operations['id_prop'] = id_prop.text

        dic5['operation' + str(i)].append(operations)
        operationlst.append(dic5)
        i += 1
        #print("\n")
    if auxop == True:
        l.append(operationlst)
    else:
        operationlst = []
        l.append(operationlst)


    #print("GENERALIZAÇÃO")
    auxgen = False
    i = 0
    for id_generalization in root.findall("./{http://gaphor.sourceforge.net/model}Generalization"):
        auxgen = True
        generalizationlst = []
        dic6['generalization'  + str(i)] = []
        generalizations = {}
        generalizations['generalization_id'] = id_generalization.attrib
        #print("id_generalization", id_generalization.attrib)
        for id_general in id_generalization.findall("./{http://gaphor.sourceforge.net/model}general/{http://gaphor.sourceforge.net/model}ref"):
            #print("id_general", id_general.attrib)
            generalizations['id_general'] = id_general.attrib
        for id_specific in id_generalization.findall("./{http://gaphor.sourceforge.net/model}specific/{http://gaphor.sourceforge.net/model}ref"):
            #print("id_specific", id_specific.attrib)
            generalizations['id_specific'] = id_specific.attrib
        dic6['generalization' + str(i)].append(generalizations)
        generalizationlst.append(dic6)

        i +=1 

    if auxgen == True:
        l.append(generalizationlst)
    else:
        generalizationlst = []
        l.append(generalizationlst)

    #general é passado como parametro no specific
    relacoes_gener = []

    for herancas in l[5]:
        i = len(herancas)
        x = 0
        while x < i:
            gener = herancas['generalization' + str(x)][0]
            relacoes_gener.append([gener['generalization_id']['id'], gener['id_general']['refid'], gener['id_specific']['refid']])
            x += 1

    #ONTOUML
    auxverificaonto = False

    dicheritage = {}
    dicheritage2 = {} #chave id, primeira posicao pai e segunda posicao filho
    dicheritage3 = {}
    for id_heritage in root.findall("./{http://gaphor.sourceforge.net/model}Heritage"):
        idHeritage = id_heritage.attrib['id']
        #print("ENTROU")

        for id_heritage2 in id_heritage.findall("./{http://gaphor.sourceforge.net/model}navigableOwnedEnd/{http://gaphor.sourceforge.net/model}reflist/{http://gaphor.sourceforge.net/model}ref"):
            dicheritage[idHeritage] = id_heritage2.attrib['refid']
            dicheritage2[idHeritage] = []

        for id_heritage2 in id_heritage.findall("./{http://gaphor.sourceforge.net/model}memberEnd/{http://gaphor.sourceforge.net/model}reflist/{http://gaphor.sourceforge.net/model}ref"):
            dicheritage2[idHeritage].append(id_heritage2.attrib['refid'])

        for id_heritage2 in id_heritage.findall("./{http://gaphor.sourceforge.net/model}name/{http://gaphor.sourceforge.net/model}val"):
            dicheritage2[idHeritage].append(id_heritage2.text)
            #if id_heritage2.text not in dicheritage3:
            #   dicheritage2[id_heritage2.text] = []
    #print("h2", dicheritage2)
    dicgeralonto = {}
    #print("AQUI", dicheritage)
    

    #print("\n1 ", dicprop2)
    #dicionario com todas relacoes exceto heranca
    dicrelacoes = {}
    #para relacao de mediation (fazer para outras relacoes)
    for id_mediation in root.findall("./{http://gaphor.sourceforge.net/model}Mediation"):
        idMediation = id_mediation.attrib['id']
        lstrelacoes = []
        for id_mediation2 in id_mediation.findall("./{http://gaphor.sourceforge.net/model}memberEnd/{http://gaphor.sourceforge.net/model}reflist/{http://gaphor.sourceforge.net/model}ref"):
            lstrelacoes.append(id_mediation2.attrib['refid'])
            dicrelacoes[idMediation] = lstrelacoes

    dicmaterial = {}
    for id_material in root.findall("./{http://gaphor.sourceforge.net/model}Material"):
        idMaterial = id_material.attrib['id']
        lstrelacoes = []
        for id_material2 in id_material.findall("./{http://gaphor.sourceforge.net/model}memberEnd/{http://gaphor.sourceforge.net/model}reflist/{http://gaphor.sourceforge.net/model}ref"):
            lstrelacoes.append(id_material2.attrib['refid'])
            dicrelacoes[idMaterial] = lstrelacoes
            dicmaterial[idMaterial] = lstrelacoes
        for id_material2 in id_material.findall("./{http://gaphor.sourceforge.net/model}name/{http://gaphor.sourceforge.net/model}val"):
            lstrelacoes.append(id_material2.text)
            dicmaterial[idMaterial] = lstrelacoes
    #print("DICRELACOES", dicrelacoes)

    dickind = {}
    lstkind = []
    for id_kind in root.findall("./{http://gaphor.sourceforge.net/model}StereotypeKind"):
        auxverificaonto = True
        idOnto = id_kind.attrib['id']
        #print("id_kind", id_kind.attrib)

        for id_kind2 in id_kind.findall("./{http://gaphor.sourceforge.net/model}name/{http://gaphor.sourceforge.net/model}val"):
            dickind[idOnto] = id_kind2.text
            dicgeralonto[idOnto] = [id_kind2.text, "kind"]
            #print("id_kind2", id_kind2.text)
            #print("dic", dickind)
    if len(dickind) >= 1:
        lstkind = dickind.values()
        lstkind = list(lstkind)
    #print("aaaaa", (lstkind))

    dicrelator = {}
    lstrelator = []
    for id_relator in root.findall("./{http://gaphor.sourceforge.net/model}StereotypeRelator"):
        auxverificaonto = True
        idOnto = id_relator.attrib['id']
        #print("id_relator", id_relator.attrib)
        for id_relator2 in id_relator.findall("./{http://gaphor.sourceforge.net/model}name/{http://gaphor.sourceforge.net/model}val"):
            dicrelator[idOnto] = id_relator2.text
            dicgeralonto[idOnto] = [id_relator2.text, "relator"]
            #print("id_relator2", id_relator2.text)
            #print("dic2", dicrelator)
    if len(dicrelator) >= 1:
        lstrelator = dicrelator.values()
        lstrelator = list(lstrelator)


    dicphase = {}
    lstphase = []
    for id_phase in root.findall("./{http://gaphor.sourceforge.net/model}StereotypePhase"):
        auxverificaonto = True
        idOnto = id_phase.attrib['id']
        #print("id_phase", id_phase.attrib)
        for id_phase2 in id_phase.findall("./{http://gaphor.sourceforge.net/model}name/{http://gaphor.sourceforge.net/model}val"):
            dicphase[idOnto] = id_phase2.text
            dicgeralonto[idOnto] = [id_phase2.text, "phase"]
            #print("id_phase2", id_phase2.text)
            #print("dic2", dicphase)
    if len(dicphase) >= 1:
        lstphase = dicphase.values()


    dicsubkind = {}
    lstsubkind = []
    for id_subkind in root.findall("./{http://gaphor.sourceforge.net/model}StereotypeSubkind"):
        auxverificaonto = True
        idOnto = id_subkind.attrib['id']
        #print("id_subkind", id_subkind.attrib)
        for id_subkind2 in id_subkind.findall("./{http://gaphor.sourceforge.net/model}name/{http://gaphor.sourceforge.net/model}val"):
            dicsubkind[idOnto] = id_subkind2.text
            dicgeralonto[idOnto] = [id_subkind2.text, "subkind"]
            #print("id_subkind2", id_subkind2.text)
            #print("dic2", dicsubkind)
    if len(dicsubkind) >= 1:
        lstsubkind = dicsubkind.values()

    dicrole = {}
    lstrole = []
    for id_role in root.findall("./{http://gaphor.sourceforge.net/model}StereotypeRole"):
        auxverificaonto = True
        idOnto = id_role.attrib['id']
        #print("id_role", id_role.attrib)
        for id_role2 in id_role.findall("./{http://gaphor.sourceforge.net/model}name/{http://gaphor.sourceforge.net/model}val"):
            dicrole[idOnto] = id_role2.text
            dicgeralonto[idOnto] = [id_role2.text, "role"]
            #print("id_role2", id_role2.text)
            #print("dic2", dicrole)
    if len(dicrole) >= 1:
        lstrole = dicrole.values()

    diccollective = {}
    lstcollective = []
    for id_collective in root.findall("./{http://gaphor.sourceforge.net/model}StereotypeCollective"):
        auxverificaonto = True
        idOnto = id_collective.attrib['id']
        #print("id_collective", id_collective.attrib)
        for id_collective2 in id_collective.findall("./{http://gaphor.sourceforge.net/model}name/{http://gaphor.sourceforge.net/model}val"):
            diccollective[idOnto] = id_collective2.text
            dicgeralonto[idOnto] = [id_collective2.text, "collective"]
            #print("id_collective2", id_collective2.text)
            #print("dic2", diccollective)
    if len(diccollective) >= 1:
        lstcollective = diccollective.values()

    dicquantity = {}
    lstquantity = []
    for id_quantity in root.findall("./{http://gaphor.sourceforge.net/model}StereotypeQuantity"):
        auxverificaonto = True
        idOnto = id_quantity.attrib['id']
        #print("id_quantity", id_quantity.attrib)
        for id_quantity2 in id_quantity.findall("./{http://gaphor.sourceforge.net/model}name/{http://gaphor.sourceforge.net/model}val"):
            dicquantity[idOnto] = id_quantity2.text
            dicgeralonto[idOnto] = [id_quantity2.text, "quantity"]
            #print("id_quantity2", id_quantity2.text)
            #print("dic2", dicquantity)
    if len(dicquantity) >= 1:
        lstquantity = dicquantity.values()

    diccategory = {}
    lstcategory = []
    for id_category in root.findall("./{http://gaphor.sourceforge.net/model}StereotypeCategory"):
        auxverificaonto = True
        idOnto = id_category.attrib['id']
        #print("id_category", id_category.attrib)
        for id_category2 in id_category.findall("./{http://gaphor.sourceforge.net/model}name/{http://gaphor.sourceforge.net/model}val"):
            diccategory[idOnto] = id_category2.text
            dicgeralonto[idOnto] = [id_category2.text, "category"]
            #print("id_category2", id_category2.text)
            #print("dic2", diccategory)
    if len(diccategory) >= 1:
        lstcategory = diccategory.values()

    dicphasemixin = {}
    lstphasemixin = []
    for id_phasemixin in root.findall("./{http://gaphor.sourceforge.net/model}StereotypePhasemixin"):
        auxverificaonto = True
        idOnto = id_phasemixin.attrib['id']
        #print("id_phasemixin", id_phasemixin.attrib)
        for id_phasemixin2 in id_phasemixin.findall("./{http://gaphor.sourceforge.net/model}name/{http://gaphor.sourceforge.net/model}val"):
            dicphasemixin[idOnto] = id_phasemixin2.text
            dicgeralonto[idOnto] = [id_phasemixin2.text, "phasemixin"]
            #print("id_phasemixin2", id_phasemixin2.text)
            #print("dic2", dicphasemixin)
    if len(dicphasemixin) >= 1:
        lstphasemixin = dicphasemixin.values()

    dicrolemixin = {}
    lstrolemixin = []
    for id_rolemixin in root.findall("./{http://gaphor.sourceforge.net/model}StereotypeRolemixin"):
        auxverificaonto = True
        idOnto = id_rolemixin.attrib['id']
        #print("id_rolemixin", id_rolemixin.attrib)
        for id_rolemixin2 in id_rolemixin.findall("./{http://gaphor.sourceforge.net/model}name/{http://gaphor.sourceforge.net/model}val"):
            dicrolemixin[idOnto] = id_rolemixin2.text
            dicgeralonto[idOnto] = [id_rolemixin2.text, "rolemixin"]
            #print("id_rolemixin2", id_rolemixin2.text)
            #print("dic2", dicrolemixin)
    if len(dicrolemixin) >= 1:
        lstrolemixin = dicrolemixin.values()

    dicmixin = {}
    lstmixin = []
    for id_mixin in root.findall("./{http://gaphor.sourceforge.net/model}StereotypeMixin"):
        auxverificaonto = True
        idOnto = id_mixin.attrib['id']
        #print("id_mixin", id_mixin.attrib)
        for id_mixin2 in id_mixin.findall("./{http://gaphor.sourceforge.net/model}name/{http://gaphor.sourceforge.net/model}val"):
            dicmixin[idOnto] = id_mixin2.text
            dicgeralonto[idOnto] = [id_mixin2.text, "mixin"]
            #print("id_mixin2", id_mixin2.text)
            #print("dic2", dicmixin)
    if len(dicmixin) >= 1:
        lstmixin = dicmixin.values()

    dicmode = {}
    lstmode = []
    for id_mode in root.findall("./{http://gaphor.sourceforge.net/model}StereotypeMode"):
        auxverificaonto = True
        idOnto = id_mode.attrib['id']
        #print("id_mode", id_mode.attrib)
        for id_mode2 in id_mode.findall("./{http://gaphor.sourceforge.net/model}name/{http://gaphor.sourceforge.net/model}val"):
            dicmode[idOnto] = id_mode2.text
            dicgeralonto[idOnto] = [id_mode2.text, "mode"]
            #print("id_mode2", id_mode2.text)
            #print("dic2", dicmode)
    if len(dicmode) >= 1:
        lstmode = dicmode.values()

    dicquality = {}
    lstquality = []
    for id_quality in root.findall("./{http://gaphor.sourceforge.net/model}StereotypeQuality"):
        auxverificaonto = True
        idOnto = id_quality.attrib['id']
        #print("id_quality", id_quality.attrib)
        for id_quality2 in id_quality.findall("./{http://gaphor.sourceforge.net/model}name/{http://gaphor.sourceforge.net/model}val"):
            dicquality[idOnto] = id_quality2.text
            dicgeralonto[idOnto] = [id_quality2.text, "quality"]
            #print("id_quality2", id_quality2.text)
            #print("dic2", dicquality)
    if len(dicquality) >= 1:
        lstquality = dicquality.values()



    '''print("DEPENDENCIA")
    auxdep = False
    i = 0
    for id_dependency in root.findall("./{http://gaphor.sourceforge.net/model}Dependency"):
        auxdep = True
        dependencylst = []
        dic8['dependency'  + str(i)] = []
        dependencies = {}
        dependencies['dependency_id'] = id_dependency.attrib
        print("id_dependency", id_dependency.attrib)
        for id_client in id_dependency.findall("./{http://gaphor.sourceforge.net/model}client/{http://gaphor.sourceforge.net/model}ref"):
            print("id_client", id_client.attrib)
            dependencies['id_client'] = id_client.attrib
        for id_supplier in id_dependency.findall("./{http://gaphor.sourceforge.net/model}supplier/{http://gaphor.sourceforge.net/model}ref"):
            print("id_supplier", id_supplier.attrib)
            dependencies['id_supplier'] = id_supplier.attrib
        dic8['dependency' + str(i)].append(dependencies)
        dependencylst.append(dic8)

        i +=1 

    if auxdep == True:
        l.append(dependencylst)
    else:
        dependencylst = []
        l.append(dependencylst)

    relacoes_depen = []
    for depend in l[6]:
        i = len(depend)
        x = 0
        while x < i:
            dep = depend['dependency' + str(x)][0]
            relacoes_depen.append([dep['dependency_id']['id'], dep['id_client']['refid'], dep['id_supplier']['refid']])
            x += 1

    print("reldep", relacoes_depen)
    #suplier passa como parametro no client'''



    #print("lst", l)
    '''print("\nlst 0", l[0])
    print("\nlst 1", l[1])
    print("\nlst 2", l[2])
    print("\nlst 3", l[3])
    print("\nlst 4", l[4])'''

    for classes_name in l[3]:
        i2 = len(classes_name)
        x2 = 0
        while x2 < i2:
            cl = classes_name['classes' + str(x2)][0]['class_id']['id']
            dic7[cl] = classes_name['classes' + str(x2)][0]['class_name']
            x2 += 1

    print("\n")

    relacoes = []
    for propriedades in l[1]:
        #propriedades['property' + len(propriedades)]
        i = len(propriedades)
        x = 0
        while x < i:
            prop = propriedades['property' + str(x)][0]
            #prop2 = propriedades['property' + str(x)][0]
            if 'assoc_id' in prop:

                for classesp in l[3]:
                    i2 = len(classesp)
                    x2 = 0
                    while x2 < i2:
                        #print("ENTROU", prop)
                        #print("AQUIIII", classesp['classes' + str(x2)][0]['class_id']['id'])
                        if classesp['classes' + str(x2)][0]['class_id']['id']:
                            cl = classesp['classes' + str(x2)][0]['class_id']['id']
                            if 'class_id' in prop:
                                if (cl == prop['class_id']['refid']):
                                    mult = 'one'
                                    if 'upperval' in prop:
                                        if prop['upperval'] == '1':
                                            if 'lowerval' in prop and prop['lowerval'] == '0':
                                                mult = 'lone'
                                        elif 'lowerval' in prop and prop['upperval'] == '*' and prop['lowerval'] == '*':
                                            mult = 'some'
                                        elif 'lowerval' in prop and prop['upperval'] == '*' and prop['lowerval'] == '0':
                                            mult = 'lone'
                                        elif prop['upperval'] == '*':
                                            mult = 'some'
                                        elif 'lowerval' in prop and prop['upperval'] == '*' and prop['lowerval'] == '1':
                                            mult = 'some'

                                    relacoes.append([classesp['classes' + str(x2)][0]['class_name'], prop['assoc_id']['refid'], cl, mult])
                        x2 += 1
                    
            x += 1
    #print("classesps", relacoes)
    #acrescentar em "relacoes" as relações de generalization e dependency
    #l[0] package
    #l[1] property
    #l[2] association
    #l[3] classes
    #l[4] operation
    #l[5] generalization
    #l[6] dependency
    with open(caminhoc, "w") as arquivo:
        arquivo.writelines("module " + dic['module'].replace(" ", ""))

        if auxverificaonto == True:
            arquivo.writelines("\nopen util/ordering[State] as state")
            arquivo.writelines("\nopen util/relation\n")

            #criando assinatura kind
            if len(lstkind) > 0:
                #print(len(lstkind))
                for i in lstkind:
                    arquivo.writelines("\nsig " + i + "{}")


            #criando assinatura relator
            '''if len(lstrelator) > 0:
                for i in lstrelator:
                    arquivo.writelines("\nsig " + i + "{}")'''

            #for i in dicrelacoes:
            #   print(i)
            #print(l[1])
            dicrelatorassoc = {}
            for propriedades in l[1]:
                #propriedades['property' + len(propriedades)]
                i = len(propriedades)
                x = 0
                while x < i:
                    prop = propriedades['property' + str(x)][0]
                    #print(prop)
                    for x3 in dicheritage2:
                        if 'class_id' in prop:
                            if  dicheritage2[x3][0] == prop['property_id']['id']:
                                dicheritage2[x3][0] = prop['class_id']['refid']
                            if  dicheritage2[x3][1] == prop['property_id']['id']:
                                dicheritage2[x3][1] = prop['class_id']['refid']

                    if 'assoc_id' in prop:
                        for j in dicrelator:
                            if j == prop['class_id']['refid']:
                                #print("chave relator", j)
                                if j not in dicrelatorassoc:
                                    dicrelatorassoc[j] = []
                                #print("chave associacao", prop['assoc_id']['refid'])
                                
                                for j1 in dicrelacoes:
                                    
                                    if prop['assoc_id']['refid'] == j1:
                                        #print("propriedades da associacao", dicrelacoes[j1])
                                        
                                        for propriedades2 in l[1]:
                                            i2 = len(propriedades2)
                                            x2 = 0
                                            
                                            while x2 < i2:
                                                prop2 = propriedades2['property' + str(x2)][0]
                                                if dicrelacoes[j1][0] == prop2['property_id']['id']:
                                                    auxrel1 = prop2['class_id']['refid']
                                                    if auxrel1 != j:
                                                        auxrel0 = auxrel1
                                                if dicrelacoes[j1][1] == prop2['property_id']['id']:
                                                    auxrel2 = prop2['class_id']['refid']
                                                    if auxrel2 != j:
                                                        auxrel0 = auxrel2

                                                mult = 'one'
                                                if 'upperval' in prop2:
                                                    if prop2['upperval'] == '1':
                                                        if 'lowerval' in prop2 and prop2['lowerval'] == '0':
                                                            mult = 'lone'
                                                    elif 'lowerval' in prop2 and prop2['upperval'] == '*' and prop2['lowerval'] == '*':
                                                        mult = 'some'
                                                    elif 'lowerval' in prop2 and prop2['upperval'] == '*' and prop2['lowerval'] == '0':
                                                        mult = 'lone'
                                                    elif prop2['upperval'] == '*':
                                                        mult = 'some'
                                                    elif 'lowerval' in prop2 and prop2['upperval'] == '*' and prop2['lowerval'] == '1':
                                                        mult = 'some'

                                                x2 += 1
                                        
                                        dicrelatorassoc[j].append((auxrel0, mult))
                                        #print("auxrel", dicrelatorassoc)

                        #continuar - fazer um dicionario relator q tenha a chave o id relator
                        #e uma lista de tuplas que contenha o id do objeto e a multiplicade 
                        #lista pronta (dicrelatorassoc) -------- Escrever no arquivo externo

                    x += 1
            '''print("h1", dicrelatorassoc)
            print("h2", dicheritage2)
            print("h3", dicgeralonto)'''

            dicrelatorkind = {}
            for x in dicrelatorassoc:
                for x2 in range(len(dicrelatorassoc[x])):
                    #print("aqui", dicrelatorassoc[x][x2][0])
                    for x3 in dicheritage2:
                        if dicheritage2[x3][1] == dicrelatorassoc[x][x2][0]:
                            if dicgeralonto[dicheritage2[x3][0]][1] == "kind":
                                dicrelatorkind[dicheritage2[x3][1]] = dicheritage2[x3][0]
            #print("\n h4", dicrelatorkind)

            #criando assinatura relator (configurar para quando tem conexao com outro objeto) - ok
            #print("dic material", dicmaterial)
            #print("pro", dicprop2)
            for x in dicmaterial:
                for i in range(len(dicmaterial[x])):
                    if dicmaterial[x][i] in dicprop2:
                        dicmaterial[x][i] = dicprop2[dicmaterial[x][i]]
            #print("dic relator", dicrelatorassoc)
            #print("dic material", dicmaterial)
            #print("\ndicg", dicgeralonto)
            #print("\ndic relacao2", dicheritage2)
            #print("he", dicrelacoes)


            #FAZER: Comparar dicrelator com dicmaterial e quando os dois possuirem os mesmos objetos 
            #escrever "derived_material_relationX: " + obj1 multiplicdade + "->" + obj2 + ","
            
            #fazer um dic (dicrelmat) com chave derived_material_relationX e dentro  uma lista
            #1a posi: id do relator
            #2a posi: nome da relacao material (fica na ultima posi do dic material)
            #Verificar qual obj sao herdeiro de kind com mais phase - o que possuir mais phase do kind eh obj1
            #3a posi: obj1
            #4a posi: mult do obj1
            #5a posi: obj2
            #eh preciso verificar se os dois sao role??

            dicrelmat = {}
            contrelmat = 0
            for i in dicrelatorassoc:
                auxdicrelmat = "derived_material_relation" + str(contrelmat)
                #print("ax", auxdicrelmat)
                contrelmat += 1
                #print("i", dicrelatorassoc[i][0][1], dicrelatorassoc[i][1][0])
                for x in dicmaterial:
                    #print("x", dicmaterial[x][0], dicmaterial[x][1])
                    if (dicmaterial[x][0] == dicrelatorassoc[i][0][0]) or (dicmaterial[x][0] == dicrelatorassoc[i][1][0]):
                        auxrelmat = True
                    else:
                        auxrelmat = False
                    if (dicmaterial[x][1] == dicrelatorassoc[i][0][0] or dicmaterial[x][1] == dicrelatorassoc[i][1][0]):
                        auxrelmat1 = True
                    else:
                        auxrelmat1 = False
                    #fazer um aux que contenha o q possui mais phase
                    #ignorar --- fazer um if para comparar com o aux o obj e escrever a lista de acordo com oq for
                    #colocar na pose anterior oq possui mais phase
                    aux0 = 0
                    aux1 = 0
                    auxx0 = ''
                    auxx1 = ''
                    for h2 in dicheritage2:
                        #print("teste", dicheritage2[h2])
                        if dicheritage2[h2][1] == dicrelatorassoc[i][0][0]:
                            auxx0 = dicheritage2[h2][0]
                        elif dicheritage2[h2][1] == dicrelatorassoc[i][1][0]:
                            auxx1 = dicheritage2[h2][0]
                    for h2 in dicheritage2:
                        if dicheritage2[h2][0] == auxx0:
                            if dicgeralonto[dicheritage2[h2][1]][1] == "phase":
                                aux0 += 1
                        elif dicheritage2[h2][0] == auxx1:
                            if dicgeralonto[dicheritage2[h2][1]][1] == "phase":
                                aux1 += 1
                    #print("aux0", aux0)
                    #print("aux1", aux1)
                    if (auxrelmat == True and auxrelmat1 == True):
                        if aux0 > aux1:
                            dicrelmat[auxdicrelmat] = [i, dicmaterial[x][2], dicrelatorassoc[i][0][0], dicrelatorassoc[i][0][1], dicrelatorassoc[i][1][0]]
                        else:
                            dicrelmat[auxdicrelmat] = [i, dicmaterial[x][2], dicrelatorassoc[i][1][0], dicrelatorassoc[i][1][1], dicrelatorassoc[i][0][0]]
            #print("\nrelmat", dicrelmat)



            #fazer: Quando o i for igual a chave do dicrelmat escrever: "derived_material_relationX: " + obj1 multiplicdade + "->" + obj2 + ","
            if len(lstrelator) > 0:
                for i in dicrelatorassoc:
                    if len(dicrelatorassoc[i]) < 1:
                        arquivo.writelines("\nsig " + dicgeralonto[i][0] + "{}")
                        #print(dicrelatorassoc[i])
                    else:
                        arquivo.writelines("\nsig " + dicgeralonto[i][0] + "{")
                        for j in range (len(dicrelatorassoc[i])):
                            #print(dicgeralonto[dicrelatorassoc[i][j][0]][0])
                            #print(dicrelatorassoc[i][j])
                            #fazer um dicionario com a chave sendo objeto principal e o pai dele quando kind - ok
                            arquivo.writelines("\n\t" + dicgeralonto[dicrelatorassoc[i][j][0]][0] + ": " + dicrelatorassoc[i][j][1] + " " + dicgeralonto[dicrelatorkind[dicrelatorassoc[i][j][0]]][0] + ",")
                            #colocar virgula quando nao for o ultimo
                            if j == (len(dicrelatorassoc[i])-1):
                                for x in dicrelmat:
                                    if dicrelmat[x][0] == i:
                                        arquivo.writelines("\n\t" + x + ": " + dicgeralonto[dicrelmat[x][2]][0] + " " + dicrelmat[x][3] + " -> " + dicgeralonto[dicrelmat[x][4]][0] + ",")
                                    #print("aaaa", dicrelmat[x][0])
                                arquivo.writelines("\n}")
                            #elif j != (len(dicrelatorassoc[i])-1):
                            #   arquivo.writelines(", ")


            #criando assinaturas de subkind quando classe pai for kind
            dicherancasubkind = {}
            for propriedadesx in l[1]:
                #propriedades['property' + len(propriedades)]
                i = len(propriedadesx)
                x = 0
                while x < i:
                    prop = propriedadesx['property' + str(x)][0]
                    #print("\n", prop)
                    if prop['assoc_id']['refid'] in dicheritage:
                        #print("\n propriedade pai", dicheritage[prop['assoc_id']['refid']])
                        for clasprop in l[1]:
                            i2 = len(propriedadesx)
                            x2 = 0
                            while x2 < i2:
                                prop2 = clasprop['property' + str(x2)][0]
                                if prop2['property_id']['id'] == dicheritage[prop['assoc_id']['refid']]:
                                    #print("classsss pai", prop2['class_id']['refid'])
                                    auxpai = prop2['class_id']['refid']
                                x2 += 1

                        auxfilho = prop['class_id']['refid']
                        #print("auxpai", auxpai)
                        #print("auxfilho", auxfilho)

                        if auxpai != auxfilho:
                            if dicgeralonto[auxfilho][1] == "subkind":
                                if auxpai not in dicherancasubkind:
                                    dicherancasubkind[auxpai] = []
                                #print("pooioioioi9", dicgeralonto[auxfilho])                       
                                dicherancasubkind[auxpai].append(dicgeralonto[auxfilho][0])

                        #print("llssst", dicherancasubkind[auxpai])
                    x += 1

            #arquivo.writelines("sig ")
            auxpais = list(dicherancasubkind.keys())
            for i in range (len(auxpais)):
                arquivo.writelines("\nsig ")
                for j in range (len(dicherancasubkind[auxpais[i]])):
                    arquivo.writelines(dicherancasubkind[auxpais[i]][j])
                    if j == (len(dicherancasubkind[auxpais[i]])-1):
                        arquivo.writelines(" in " + dicgeralonto[auxpais[i]][0] + "{}")
                    elif j != (len(dicherancasubkind[auxpais[i]][j])-1):
                        arquivo.writelines(", ")
                
                #print("j", dicherancasubkind[auxpais[i]][j])
            for i in range (len(auxpais)):
                lstaux = []
                arquivo.writelines("\nfact generalization_set{\n\tdisj[")
                for j in range (len(dicherancasubkind[auxpais[i]])):
                    arquivo.writelines(dicherancasubkind[auxpais[i]][j])
                    lstaux.append(dicherancasubkind[auxpais[i]][j])
                    if j == (len(dicherancasubkind[auxpais[i]])-1):
                        arquivo.writelines("]\n\t")
                        arquivo.writelines(dicgeralonto[auxpais[i]][0] + " = ")
                        #print("oiiiiii", lstaux)
                        for i2 in range (len(lstaux)):
                            arquivo.writelines(lstaux[i2])
                            if i2 == (len(lstaux)-1):
                                arquivo.writelines("\n}")
                            else:
                                arquivo.writelines("+")

                    elif j != (len(dicherancasubkind[auxpais[i]][j])-1):
                        arquivo.writelines(",")
            #print("\nherança", dicherancasubkind)
            #print("AQUI", dicgeralonto)

            #pegar categorias e passar para codigo
            if len(lstcategory) > 0:
                for j in diccategory:
                    #print(j)
                    for propriedadeso in l[1]:
                        i = len(propriedadeso)
                        x = 0
                        lteste = []
                        while x < i:
                            prop = propriedadeso['property' + str(x)][0]
                            #prop2 = propriedades['property' + str(x)][0]
                            #print(prop)
                            if prop['class_id']['refid'] == j:
                                lteste.append(prop['assoc_id']['refid'])
                                #print(lteste)

                            x += 1

                        x2 = 0
                        lteste2 = []
                        while x2 < i:
                            prop = propriedadeso['property' + str(x2)][0]
                            #prop2 = propriedades['property' + str(x)][0]
                            #print(prop)
                            for x3 in range(len(lteste)):
                                if prop['assoc_id']['refid'] == lteste[x3] and prop['class_id']['refid'] != j:
                                    lteste2.append(prop['class_id']['refid'])

                            x2 += 1
                        
                        #Escreve 'fun' - category
                        arquivo.writelines("\nfun " + diccategory[j] + ":(")
                        for xi in range (len(lteste2)):
                            arquivo.writelines(dicgeralonto[lteste2[xi]][0])
                            if xi != (len(lteste2)-1):
                                arquivo.writelines("+")
                            if xi == (len(lteste2)-1):
                                arquivo.writelines("){\n\t")
                        for xi2 in range (len(lteste2)):
                            arquivo.writelines(dicgeralonto[lteste2[xi2]][0])
                            if xi2 != (len(lteste2)-1):
                                arquivo.writelines("+")
                            if xi2 == (len(lteste2)-1):
                                arquivo.writelines("\n}")
            #Criar sig State

            #Criar um dicionario, colocar a chave "rel2" (criar uma chave para cada) e dentro das chaves colocar uma lista com todos que possuem esse valor na relacao
            #Obs.: O nome utilizado "rel2" nao podera ser reutilizado em outras relacoes de outros objetos
            for groupheritage in dicheritage2:
                #print("a\n", dicheritage2[groupheritage])
                if (len(dicheritage2[groupheritage])) == 3:
                    #print("oi")
                    if dicheritage2[groupheritage][2] not in dicheritage3:
                        dicheritage3[dicheritage2[groupheritage][2]] = []
                    
                    if dicheritage2[groupheritage][0] not in dicheritage3[dicheritage2[groupheritage][2]]:
                        if dicgeralonto[dicheritage2[groupheritage][0]][1] != "subkind":
                            dicheritage3[dicheritage2[groupheritage][2]].append(dicheritage2[groupheritage][0])
                    if dicgeralonto[dicheritage2[groupheritage][1]][1] != "subkind":
                        dicheritage3[dicheritage2[groupheritage][2]].append(dicheritage2[groupheritage][1])
            #print("aq", dicheritage3)
            for names in dicheritage3:
                #configurando para ser apenas kind
                if dicgeralonto[dicheritage3[names][0]][1] == "kind":
                    dicheritage3[names][0] = dicgeralonto[dicheritage3[names][0]][0]
                #print("\naq2", dicgeralonto[dicheritage3[names][0]][0])
            #print("aq", dicheritage3)

            #criando Sig State
            arquivo.writelines("\nsig State{\n")
            if ((len(lstkind))+(len(lstrelator))) > 0:
                arquivo.writelines("\texists: set (")
                if (len(lstkind)) > 0:
                    for x in range (len(lstkind)):
                        arquivo.writelines(lstkind[x])
                        if x != (len(lstkind)-1):
                            arquivo.writelines("+")
                    if (len(lstrelator)) > 0:
                        arquivo.writelines("+")

                if (len(lstrelator)) > 0:
                    for x in range (len(lstrelator)):
                        arquivo.writelines(lstrelator[x])
                        if x != (len(lstrelator)-1):
                            arquivo.writelines("+")
                arquivo.writelines("),")
            #conferir se soh existe 'disjont' com heranca em kind
            for i in dicheritage3:
                if (len(dicheritage3[i])) > 2:
                    arquivo.writelines("\n\tdisj ")
                    x = 1
                    while x < (len(dicheritage3[i])):
                        #print("x", x)
                        #print("dc", dicheritage3[i][x])
                        arquivo.writelines(dicgeralonto[dicheritage3[i][x]][0])
                        if x != (len(dicheritage3[i])-1):
                            arquivo.writelines(", ")
                        x += 1
                    arquivo.writelines(": set " + dicheritage3[i][0] + ":>exists,")
            for i in dicheritage3:
                if (len(dicheritage3[i])) == 2:
                    #print("k", dicgeralonto[dicheritage3[i][1]][0])
                    arquivo.writelines("\n\t" + dicgeralonto[dicheritage3[i][1]][0] + ": set " + dicheritage3[i][0] + ":>exists,")
            for i in dicheritage2:
                if (len(dicheritage2[i])) < 3:
                    if dicgeralonto[dicheritage2[i][0]][1] == "kind":
                        if dicgeralonto[dicheritage2[i][1]][1] == "phase" or dicgeralonto[dicheritage2[i][1]][1] == "role":
                            arquivo.writelines("\n\t" + dicgeralonto[dicheritage2[i][1]][0] + ": set " + dicgeralonto[dicheritage2[i][0]][0] + ":>exists,")

            #Se o Phase herda de um mixin e o mixin possui um filho kind -> Mixin: set Kind:>exists+Phase,
            dicmixinstate = {}
            for i in dicheritage2:
                if (len(dicheritage2[i])) < 3:
                    if dicgeralonto[dicheritage2[i][0]][1] == "mixin":
                        #print("criar dicionario de mixin com chave id_mixin", dicgeralonto[dicheritage2[i][0]])
                        if dicheritage2[i][0] not in dicmixinstate:
                            dicmixinstate[dicheritage2[i][0]] = []
                        if (dicgeralonto[dicheritage2[i][1]][1] == "kind" or dicgeralonto[dicheritage2[i][1]][1] == "phase"):
                            dicmixinstate[dicheritage2[i][0]].append(dicheritage2[i][1])
                        #print("anexar", dicmixinstate)
            for i in dicmixinstate:
                #print('i', dicgeralonto[dicmixinstate[i][1]][0])
                if (len(dicmixinstate[i]) >= 2):
                    arquivo.writelines("\n\t" + dicgeralonto[i][0] + ": set ")
                    if dicgeralonto[dicmixinstate[i][1]][1] == "kind":
                        #print("aq", dicgeralonto[dicmixinstate[i][0]][0])
                        arquivo.writelines(dicgeralonto[dicmixinstate[i][1]][0] + ":>exists+" + dicgeralonto[dicmixinstate[i][0]][0] + ",")
                    elif dicgeralonto[dicmixinstate[i][1]][1] == "phase":
                        arquivo.writelines(dicgeralonto[dicmixinstate[i][0]][0] + ":>exists+" + dicgeralonto[dicmixinstate[i][1]][0] + ",")
                    
            #Se o Role tem relacao com outro Role -> Relacao: set Role multiplicidade -> multiplicidade Role,
            for i in dicrelmat:
                arquivo.writelines("\n\t" + dicrelmat[i][1] + ": set " + dicgeralonto[dicrelmat[i][2]][0] + " -> " + dicgeralonto[dicrelmat[i][4]][0] + ",")




            arquivo.writelines("\n}")

            
            #comecar segunda parte do State aqui
            arquivo.writelines(" {\n\tall x:exists|x not in this.next.@exists implies x not in this.^next.@exists")
            #print("d3", dicheritage3)
            for i in dicheritage3:
                if (len(dicheritage3[i])) > 2:
                    #arquivo.writelines("\n\tdisj ")
                    x = 1
                    arquivo.writelines("\n\t" + dicheritage3[i][0] + ":>exists = ")
                    while x < (len(dicheritage3[i])):
                        #print("x", x)
                        #print("dc", dicheritage3[i][x])
                        arquivo.writelines(dicgeralonto[dicheritage3[i][x]][0])
                        if x != (len(dicheritage3[i])-1):
                            arquivo.writelines("+")
                        x += 1
            for i in dicheritage3:
                if (len(dicheritage3[i])) == 2:
                    #print("k", dicgeralonto[dicheritage3[i][1]][0])
                    arquivo.writelines("\n\t" + dicheritage3[i][0] + ":>exists = " + dicgeralonto[dicheritage3[i][1]][0])
            '''for i in dicheritage2:
                if (len(dicheritage2[i])) < 3:
                    if dicgeralonto[dicheritage2[i][0]][1] == "kind":
                        if dicgeralonto[dicheritage2[i][1]][1] == "phase":
                            arquivo.writelines("\n" + dicgeralonto[dicheritage2[i][1]][0] + ": set " + dicgeralonto[dicheritage2[i][0]][0] + ":>exists,")'''
            #print("re", dicrelator)
            if len(lstrelator) > 0:
                for i in dicrelatorassoc:
                    if len(dicrelatorassoc[i]) > 0:
                        arquivo.writelines("\n\tall x:" + dicgeralonto[i][0] + ":>exists |")
                        for j in range (len(dicrelatorassoc[i])):
                            #print(dicgeralonto[dicrelatorassoc[i][j][0]][0])
                            #print(dicrelatorassoc[i][j])
                            #fazer um dicionario com a chave sendo objeto principal e o pai dele quando kind - ok
                            arquivo.writelines(" x." + dicgeralonto[dicrelatorassoc[i][j][0]][0] + " in " + dicgeralonto[dicrelatorkind[dicrelatorassoc[i][j][0]]][0] + ":>exists")
                            #colocar virgula quando nao for o ultimo
                            '''if j == (len(dicrelatorassoc[i])-1):
                                arquivo.writelines("}")'''
                            if j != (len(dicrelatorassoc[i])-1):
                                arquivo.writelines(" and ")
            


            #tirar duvida com Max e escrever School e Student
            for i in dicrelmat:
                #print("dicrelm", dicrelmat)
                arquivo.writelines("\n\t" + dicgeralonto[dicrelmat[i][2]][0] + " = (" + dicgeralonto[dicrelmat[i][0]][0] + ":>exists)." + dicgeralonto[dicrelmat[i][2]][0])
                arquivo.writelines("\n\t(" + dicgeralonto[dicrelmat[i][0]][0] + ":>exists)." + dicgeralonto[dicrelmat[i][4]][0] + " in " + dicgeralonto[dicrelmat[i][4]][0])
                arquivo.writelines("\n\tall x: " + dicgeralonto[dicrelmat[i][4]][0] + " | " + dicrelmat[i][3] + " " + dicgeralonto[dicrelmat[i][0]][0] + ":>exists:>" + dicgeralonto[dicrelmat[i][4]][0] + ".x")

            for i in dicmixinstate:
                #print('i', dicgeralonto[dicmixinstate[i][1]][0])
                if (len(dicmixinstate[i]) >= 2):
                    arquivo.writelines("\n\t" + dicgeralonto[i][0] + " = ")
                    if dicgeralonto[dicmixinstate[i][1]][1] == "kind":
                        #print("aq", dicgeralonto[dicmixinstate[i][0]][0])
                        arquivo.writelines(dicgeralonto[dicmixinstate[i][1]][0] + ":>exists+" + dicgeralonto[dicmixinstate[i][0]][0])
                    elif dicgeralonto[dicmixinstate[i][1]][1] == "phase":
                        arquivo.writelines(dicgeralonto[dicmixinstate[i][0]][0] + ":>exists+" + dicgeralonto[dicmixinstate[i][1]][0])
            
            for i in dicrelmat:
                arquivo.writelines("\n\t" + dicrelmat[i][1] + " in exists." + i)


            arquivo.writelines("\n}")


        '''for propriedades in l[1]:
            #propriedades['property' + len(propriedades)]
            i = len(propriedades)
            x = 0
            while x < i:
                print("\n", propriedades['property' + str(x)])
                x += 1'''

        '''for classes in l[3]:
            i = len(classes)
            x = 0
            while x < i:
                #arquivo.writelines("\n\nsig " + classes['classes' + str(x)][0]['class_name'] + " {")
                auxverifica = False
                #Relações de associação
                for y in range(0,len(relacoes)):
                    if (classes['classes' + str(x)][0]['class_id']['id'] == relacoes[y][2]):
                        aux = relacoes[y][1]
                        mult = relacoes[y][3]

                        for yi in range(0,len(relacoes)):
                            if relacoes[yi][1] == aux:
                                aux2 = relacoes[yi][0]
                                if aux2 != classes['classes' + str(x)][0]['class_name']:

                                    arquivo.writelines("\n\nsig " + classes['classes' + str(x)][0]['class_name'].capitalize() + " {\n" + aux2 + ": " + relacoes[yi][3] + " " + aux2.capitalize())
                                    #arquivo.writelines()
                                    for propriedades in l[1]:
                                    #propriedades['property' + len(propriedades)]
                                        i5 = len(propriedades)
                                        x5 = 0
                                        while x5 < i5:
                                            if 'cid_atributo' and 'atributos_clas' and 'typevalue' in propriedades['property' + str(x5)][0]:
                                                #print("\n", propriedades['property' + str(x5)][0]['cid_atributo']['refid'])
                                                if (propriedades['property' + str(x5)][0]['cid_atributo']['refid'] == classes['classes' + str(x)][0]['class_id']['id']):
                                                    #print("clas", classes['classes' + str(x)][0]['class_id']['id'])
                                                    arquivo.writelines("\n" + propriedades['property' + str(x5)][0]['atributos_clas'] + ': set ' +  propriedades['property' + str(x5)][0]['typevalue'].capitalize())
                                            x5 += 1
                                    arquivo.writelines("}")'''
        #AQUI COMECA UML
        relacoes2 = {}
        cr_verifica = []
        for i in relacoes:
            #print(i[0])
            if i[0] not in relacoes2:
                relacoes2[i[0]] = []
                #print(i[1])
                relacoes2[i[0]].append([i[1], i[3]])
            elif i[0] in relacoes2:
                relacoes2[i[0]].append([i[1], i[3]])
        #print("rel", relacoes2)
        for classes in l[3]:
            i = len(classes)
            x = 0
            #print("\ncl", classes)
            while x < i:
                #arquivo.writelines("\n\nsig " + classes['classes' + str(x)][0]['class_name'] + " {")
                auxverifica = False
                #Relações de associação
                lescrita = []
                auxverificaassoc = False
                for y in range(0,len(relacoes)):
                    if (classes['classes' + str(x)][0]['class_id']['id'] == relacoes[y][2]):
                        aux = relacoes[y][1]
                        mult = relacoes[y][3]
                        
                        for yi in range(0,len(relacoes)):
                            if relacoes[yi][1] == aux:
                                aux2 = relacoes[yi][0]
                                if aux2 != classes['classes' + str(x)][0]['class_name']:
                                    if classes['classes' + str(x)][0]['class_name'] not in lescrita:
                                        auxverificaassoc = True
                                        lescrita.append(classes['classes' + str(x)][0]['class_name'])
                                        #-
                                        #print("re ", relacoes_gener)
                                        if len(relacoes_gener) > 0:
                                            for i2 in range(0,len(relacoes_gener)):
                                                if(classes['classes' + str(x)][0]['class_id']['id'] == relacoes_gener[i2][2]):
                                                    arquivo.writelines("\n\nsig " + classes['classes' + str(x)][0]['class_name'].capitalize() + " extends " + dic7[relacoes_gener[i2][1]].capitalize() + " {\n" + aux2 + ": " + relacoes[yi][3] + " " + aux2.capitalize())
                                                    cr_verifica.append(classes['classes' + str(x)][0]['class_name'])
                                                    for propriedades in l[1]:
                                                        i5 = len(propriedades)
                                                        x5 = 0
                                                        while x5 < i5:
                                                            if 'cid_atributo' and 'atributos_clas' and 'typevalue' in propriedades['property' + str(x5)][0]:
                                                                #print("\n", propriedades['property' + str(x5)][0]['cid_atributo']['refid'])
                                                                if (propriedades['property' + str(x5)][0]['cid_atributo']['refid'] == classes['classes' + str(x)][0]['class_id']['id']):
                                                                    #print("clas", classes['classes' + str(x)][0]['class_id']['id'])
                                                                    arquivo.writelines("\n" + propriedades['property' + str(x5)][0]['atributos_clas'] + ': set ' +  propriedades['property' + str(x5)][0]['typevalue'].capitalize())
                                                            x5 += 1
                                                    #auxverificagen = True
                                        #-
                                        if classes['classes' + str(x)][0]['class_name'] not in cr_verifica:
                                            arquivo.writelines("\n\nsig " + classes['classes' + str(x)][0]['class_name'].capitalize() + " {\n" + aux2 + ": " + relacoes[yi][3] + " " + aux2.capitalize())
                                            cr_verifica.append(classes['classes' + str(x)][0]['class_name'])
                                            for propriedades in l[1]:
                                                i5 = len(propriedades)
                                                x5 = 0
                                                while x5 < i5:
                                                    if 'cid_atributo' and 'atributos_clas' and 'typevalue' in propriedades['property' + str(x5)][0]:
                                                        #print("\n", propriedades['property' + str(x5)][0]['cid_atributo']['refid'])
                                                        if (propriedades['property' + str(x5)][0]['cid_atributo']['refid'] == classes['classes' + str(x)][0]['class_id']['id']):
                                                            #print("clas", classes['classes' + str(x)][0]['class_id']['id'])
                                                            arquivo.writelines("\n" + propriedades['property' + str(x5)][0]['atributos_clas'] + ': set ' +  propriedades['property' + str(x5)][0]['typevalue'].capitalize())
                                                    x5 += 1
                                    elif classes['classes' + str(x)][0]['class_name'] in lescrita:
                                        #auxverificaassoc = True
                                        arquivo.writelines(",\n" + aux2 + ": " + relacoes[yi][3] + " " + aux2.capitalize())
                                        for propriedades in l[1]:
                                            i5 = len(propriedades)
                                            x5 = 0
                                            while x5 < i5:
                                                if 'cid_atributo' and 'atributos_clas' and 'typevalue' in propriedades['property' + str(x5)][0]:
                                                    #print("\n", propriedades['property' + str(x5)][0]['cid_atributo']['refid'])
                                                    if (propriedades['property' + str(x5)][0]['cid_atributo']['refid'] == classes['classes' + str(x)][0]['class_id']['id']):
                                                        #print("clas", classes['classes' + str(x)][0]['class_id']['id'])
                                                        arquivo.writelines("\n" + propriedades['property' + str(x5)][0]['atributos_clas'] + ': set ' +  propriedades['property' + str(x5)][0]['typevalue'].capitalize())
                                                x5 += 1
                classesrel = []
                #print('cr1 ', cr_verifica)
                if auxverificaassoc == True:
                    arquivo.writelines("}")
                if auxverifica == False:
                    auxverificagen = False
                    #Relações de herança
                    for i2 in range(0,len(relacoes_gener)):
                        #print("1", classes['classes' + str(x)][0]['class_id']['id'])
                        #print("2", relacoes_gener[i2][0])
                        if(classes['classes' + str(x)][0]['class_id']['id'] == relacoes_gener[i2][2]):
                            if classes['classes' + str(x)][0]['class_name'] not in cr_verifica: 
                                arquivo.writelines("\n\nsig " + classes['classes' + str(x)][0]['class_name'].capitalize() + " extends " + dic7[relacoes_gener[i2][1]].capitalize() + " {")
                                cr_verifica.append(classes['classes' + str(x)][0]['class_name'])
                                for propriedades in l[1]:
                                        #propriedades['property' + len(propriedades)]
                                    i5 = len(propriedades)
                                    x5 = 0
                                    while x5 < i5:
                                        if 'cid_atributo' and 'atributos_clas' and 'typevalue' in propriedades['property' + str(x5)][0]:
                                                    #print("\n", propriedades['property' + str(x5)][0]['cid_atributo']['refid'])
                                                    if (propriedades['property' + str(x5)][0]['cid_atributo']['refid'] == classes['classes' + str(x)][0]['class_id']['id']):
                                                        #print("clas", classes['classes' + str(x)][0]['class_id']['id'])
                                                        arquivo.writelines("\n" + propriedades['property' + str(x5)][0]['atributos_clas'] + ': set ' +  propriedades['property' + str(x5)][0]['typevalue'].capitalize())
                                        x5 += 1
                                    arquivo.writelines("}")
                                auxverificagen = True
                        elif (classes['classes' + str(x)][0]['class_id']['id'] == relacoes_gener[i2][1]):
                            #print("cl ", classes['classes' + str(x)][0]['class_name'])
                            #print('cr ', cr_verifica)
                            if (classes['classes' + str(x)][0]['class_name'] not in classesrel) and (classes['classes' + str(x)][0]['class_name'] not in cr_verifica):
                                arquivo.writelines("\n\nsig " + classes['classes' + str(x)][0]['class_name'].capitalize() + " {")#Fazer condição atributos class
                                classesrel.append(classes['classes' + str(x)][0]['class_name'])
                                cr_verifica.append(classes['classes' + str(x)][0]['class_name'])

                                for propriedades in l[1]:
                                        #propriedades['property' + len(propriedades)]
                                    i5 = len(propriedades)
                                    x5 = 0
                                    while x5 < i5:
                                        if 'cid_atributo' and 'atributos_clas' and 'typevalue' in propriedades['property' + str(x5)][0]:
                                                    #print("\n", propriedades['property' + str(x5)][0]['cid_atributo']['refid'])
                                                    if (propriedades['property' + str(x5)][0]['cid_atributo']['refid'] == classes['classes' + str(x)][0]['class_id']['id']):
                                                        #print("clas", classes['classes' + str(x)][0]['class_id']['id'])
                                                        arquivo.writelines("\n" + propriedades['property' + str(x5)][0]['atributos_clas'] + ': set ' +  propriedades['property' + str(x5)][0]['typevalue'].capitalize())
                                        x5 += 1
                                arquivo.writelines("}")
                                auxverificagen = True
                    '''if auxverificagen == False:
                        #Relações de dependencia
                        for i3 in range(0,len(relacoes_depen)):
                        #print("1", classes['classes' + str(x)][0]['class_id']['id'])
                        #print("2", relacoes_depen[i3][0])
                            if (classes['classes' + str(x)][0]['class_id']['id'] == relacoes_depen[i3][2]):
                                arquivo.writelines("\n\nsig " + classes['classes' + str(x)][0]['class_name'].capitalize() + " {")#Fazer condição atributos class
                                for propriedades in l[1]:
                                    #propriedades['property' + len(propriedades)]
                                    i5 = len(propriedades)
                                    x5 = 0
                                    while x5 < i5:
                                        if 'cid_atributo' and 'atributos_clas' and 'typevalue' in propriedades['property' + str(x5)][0]:
                                                #print("\n", propriedades['property' + str(x5)][0]['cid_atributo']['refid'])
                                                if (propriedades['property' + str(x5)][0]['cid_atributo']['refid'] == classes['classes' + str(x)][0]['class_id']['id']):
                                                    #print("clas", classes['classes' + str(x)][0]['class_id']['id'])
                                                    arquivo.writelines("\n" + propriedades['property' + str(x5)][0]['atributos_clas'] + ': set ' +  propriedades['property' + str(x5)][0]['typevalue'])
                                        x5 += 1
                                arquivo.writelines("}")
                        
                            elif(classes['classes' + str(x)][0]['class_id']['id'] == relacoes_depen[i3][1]):
                                arquivo.writelines("\n\nsig " + classes['classes' + str(x)][0]['class_name'].capitalize() + " {\n" + dic7[relacoes_depen[i3][2]].capitalize())
                                for propriedades in l[1]:
                                    #propriedades['property' + len(propriedades)]
                                    i5 = len(propriedades)
                                    x5 = 0
                                    while x5 < i5:
                                        if 'cid_atributo' and 'atributos_clas' and 'typevalue' in propriedades['property' + str(x5)][0]:
                                                #print("\n", propriedades['property' + str(x5)][0]['cid_atributo']['refid'])
                                                if (propriedades['property' + str(x5)][0]['cid_atributo']['refid'] == classes['classes' + str(x)][0]['class_id']['id']):
                                                    #print("clas", classes['classes' + str(x)][0]['class_id']['id'])
                                                    arquivo.writelines("\n" + propriedades['property' + str(x5)][0]['atributos_clas'] + ': set ' +  propriedades['property' + str(x5)][0]['typevalue'])
                                        x5 += 1

                                arquivo.writelines("}")'''
                x += 1

        arquivo.writelines("\n\npred show[] {} \nrun show")

    '''with open("/Users/Kellen Moura/Desktop/aaalloy.txt", "w") as arquivo_py:
        arquivo_py.writelines(i)'''


    '''with open(caminho, "r") as arquivo:
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
                    i += 1'''

    
    


    '''with open(caminhoc, "w") as arquivo_py:
        arquivo_py.writelines("testeoiiiii")'''

    os.remove(caminho)


class AlloyExport(Service, ActionProvider):

    def __init__(self, element_factory, file_manager, export_menu):
        self.element_factory = element_factory
        self.file_manager = file_manager
        export_menu.add_actions(self)

    def shutdown(self):
        pass

    @action(
        name="file-export-txt",
        label=gettext("Export to alloy"),
        #tooltip=gettext("Every application should have a Hello world plugin!"),
        tooltip=gettext("Export model to alloy"),
    )



    def execute(self):
        filename = self.file_manager.filename
        filename = filename.replace(".gaphor", ".xmi") if filename else "model.xmi"
        filename = save_file_dialog(
            gettext("Export model to XMI file"),
            filename=filename,
            extension=".xmi",
            filters=[(gettext("All XMI Files"), ".xmi", "text/xml")],
        )
        #print("fileeee2", filename)
        queue = Queue()

        if filename and len(filename) > 0:
            log.debug(f"Exporting alloy model to: {filename}")
            #export = exportmodel.XMIExport(self.element_factory)
            try:
                with open(filename.encode("utf-8"), "w") as out:
                    saver = storage.save_generator(XMLWriter(out), self.element_factory)
                    worker = GIdleThread(saver, queue)
                    worker.start()
                    worker.wait()
                    #export = storage.save_generator(XMLWriter(out), self.element_factory)

                    #try:
                    #export.export(filename)
            except Exception as e:
                log.error(f"Error while saving model to file {filename}: {e}")

        alloy_action(filename)

 

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
