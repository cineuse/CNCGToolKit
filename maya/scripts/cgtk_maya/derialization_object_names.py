# =============================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Wed, 25 Jun 2014 14:43:02
# =============================================
import re, string
import maya.cmds as mc
# --+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+


def derialization_object_names(object_list, name_format='Temp*', start=0, padding=3):
    """
    object_list must is a list or a tuple
    name_format mutst have one " * "
    Exp:
            [pCulbe,  pCulbe1, pCulbe2, pCulbe3, pCulbe4] -> temp*
        ->  [temp000, temp001, temp002, temp003, temp004] 
    
            [pCulbe,  pCulbe1, pCulbe2, pCulbe3, pCulbe4] -> C_temp*_geo_0
        ->  [C_temp000_geo_0, C_temp001_geo_0, C_temp002_geo_0, C_temp003_geo_0, C_temp004_geo_0] 
    """
    if not isinstance(object_list, (list, tuple)):
        return
    
    if name_format.count('*') != 1:
        return
    
    new_name_list = []
    for i, obj in enumerate(object_list):
        new_name = derialization_object_names(name_format.replace('*', string.zfill(i + start, padding)))
        new_name_list.append(new_name)
    return new_name_list
