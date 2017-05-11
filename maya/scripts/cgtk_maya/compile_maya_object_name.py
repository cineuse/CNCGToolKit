# =============================================
# author: changlong.zang
#   mail: zclongpop@163.com
#   date: Wed, 25 Jun 2014 14:43:02
# =============================================
import re, string
import maya.cmds as mc
# --+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+


def compile_maya_object_name(object_name):
    """
    build a not exists maya object name...
    Exp: 
        pCube  -> pCube1  -> pCube2  -> pCube3  -> pCube4 ...  pCuben+1
        pSphere -> pSphere1 -> pSphere2 -> pSphere3 -> pSphere4 ... pSpheren+1
    """
    if not mc.objExists(object_name):
        return object_name
    
    res = re.search('\d+$', object_name)
    if res:
        index = string.zfill(int(res.group()) + 1, len(res.group()))
        result = re.sub('\d+$', index, object_name)
    else:
        result = '%s1' % object_name
    
    return compile_maya_object_name(result)
