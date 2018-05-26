########################################
# Many of these started as standalone ArcPy files, have been joined into one large file
########################################


arcpy.env.workspace = "./working/dir"
# Defining paths for shapefile
shapefile = "./working/dir"

codeblock_PA=  """def Reclass(Vector_Mag,PA,P_C):
    if Vector_Mag>= 168.26 and P_C=="P":
        return "MVPA"
    elif Vector_Mag>=8.26 and Vector_Mag<=168.25 and P_C=="P":
        return "LA"
    elif Vector_Mag<=8.25 and P_C=="P":
        return "SED"
    elif Vector_Mag>=191.26 and P_C=="C":
        return "MVPA"
    elif Vector_Mag>=8.26 and Vector_Mag<=191.25 and P_C=="C":
        return "LA"
    elif Vector_Mag<= 8.33 and P_C=="C":
        return "SED"
    else:
        return "UNCLASS" """


arc.AddField_management(shapefile,"PA","STRING")
arc.CalculateField_management(shapefile, field="PA", expression="Reclass(!Vector_Mag!,!PA!,!P_C!)", expression_type="PYTHON_9.3", code_block=codeblock_PA)

# This script dictates a set of criteria to remove points due to GPS collection problems
# 0 = DO NOT use this point and 1 = point is VALID

import arcpy as arc

shapefile = "./path/to/shp"



codeblock_QC=  """def Reclass(speed,QC):
    if speed >=150:
        return 0
    else:
        return 1"""

arc.AddField_management(shapefile,"QC","INTEGER")
arc.CalculateField_management(shapefile, field="QC", expression="Reclass(!speed!,!QC!)", expression_type="PYTHON_9.3", code_block=codeblock_QC)


# Script used to classify CHILD shapefiles into commuting (as one column) or home/school (seperate column)
# 1 = HOME and 2 = SCHOOL. Note that each ID has a set of home/work-school points within the folder, should not use the master that contains all ID locations

import arcpy as arc
from arcpy import env
arcpy.env.workspace = "./working/dir"
# Defining paths for shapefile and all points for roads, home and school
shapefile = "./to/data/shp"
roads = "./tp/road/shp"
home = "./to/home/shp"
school = "./to/school/shp"
# Creating field to denote commuting. BAsed on Proximity to roads (<15m) and speed (>15 km/h)
codeblock_commute=  """def Reclass(speed,DIST_ROAD):
    if speed >=10 and DIST_ROAD<15:
        return 1
    else:
        return 0"""
# Determining distances and putting these into a new field 'NEAR_DIST', converted to DIST_ROAD and NEAR_DIST is removed
arc.Near_analysis(shapefile,roads)
arc.AddField_management(shapefile,"DIST_ROAD","FLOAT")
arc.CalculateField_management(shapefile, field="DIST_ROAD", expression="!NEAR_DIST!", expression_type="PYTHON_9.3")
arc.DeleteField_management(shapefile,"NEAR_DIST")
arc.DeleteField_management(shapefile,"NEAR_FID")
# New field that will be populated with 0/1 based on codeblock
arc.AddField_management(shapefile,"COMMUTE","FLOAT")
arc.CalculateField_management(shapefile, field="COMMUTE", expression="Reclass(!speed!,!DIST_ROAD!)", expression_type="PYTHON_9.3", code_block=codeblock_commute)
# Determining distances and putting these into a new field 'DIST_HOME', for HOME
arc.Near_analysis(shapefile,home)
arc.AddField_management(shapefile,"DIST_HOME","FLOAT")
arc.CalculateField_management(shapefile, field="DIST_HOME", expression="!NEAR_DIST!", expression_type="PYTHON_9.3")
arc.DeleteField_management(shapefile,"NEAR_DIST")
arc.DeleteField_management(shapefile,"NEAR_FID")
# Determining distances and putting these into a new field 'DIST_SCHL', for SCHOOL
arc.Near_analysis(shapefile,school)
arc.AddField_management(shapefile,"DIST_SCHL","FLOAT")
arc.CalculateField_management(shapefile, field="DIST_SCHL", expression="!NEAR_DIST!", expression_type="PYTHON_9.3")
arc.DeleteField_management(shapefile,"NEAR_DIST")
arc.DeleteField_management(shapefile,"NEAR_FID")
 # Creating field to denote School/Work/Home. Based on speed (<cond.) and within buffer 1=at home and 2=at work and 0=neither
code_space=  """def Reclass(speed,DIST_HOME,DIST_SCHL):
    if speed <10 and DIST_HOME<=50:
        return 1
    elif speed <10 and DIST_SCHL<=100:
        return 2
    else:
        return 0"""
# New field that will be populated with /1 based on codeblock
arc.AddField_management(shapefile,"hom_schl","FLOAT")
arc.CalculateField_management(shapefile, field="hom_schl", expression="Reclass(!speed!,!DIST_HOME!,!DIST_SCHL!)", expression_type="PYTHON_9.3",code_block=code_space)


## Script used to classify PARENT shapefiles into commuting (as one column) or home/work (seperate column)
# 1= HOME and 2 = WORK. Note that each ID has a set of home/work-school points within the folder, should not use the master that contains all ID locations
# can geodatabase and shapefiles be used in 'NEAR' tools

import arcpy as arc
from arcpy import env
arcpy.env.workspace = "./working/dir"

ID = 2000
# CHANGE PHASE NAME IN FILE 'shapefile'

# Defining paths for shapefile and all points for roads, home and school
shapefile = "./path/data/T%d_BL"  % ID
roads = "./path/roads"
home = "./path/home/HOME_%d.shp" % ID
work = "./path/work/WORK_%d.shp" % ID
school = "./path/school/SCHOOL_%d.shp" % ID



# Creating field to denote School/Work/Home. Based on speed (<cond.) and within buffer 1=at home and 2=at work and 0=neither
codeblock_home=  """def Reclass(speed,DIST_HOME):
    if speed<10 and DIST_HOME<=50:
        return 1
    else:
        return 0"""
# Determining distances and putting these into a new field 'DIST_HOME'
arc.Near_analysis(shapefile,home)
arc.AddField_management(shapefile,"DIST_HOME","FLOAT")
arc.CalculateField_management(shapefile, field="DIST_HOME", expression="!NEAR_DIST!", expression_type="PYTHON_9.3")
arc.DeleteField_management(shapefile,"NEAR_DIST")
arc.DeleteField_management(shapefile,"NEAR_FID")
# New field that will be populated with /1 based on codeblock
arc.AddField_management(shapefile,"HOME","FLOAT")
arc.CalculateField_management(shapefile, field="HOME", expression="Reclass(!speed!,!DIST_HOME!)", expression_type="PYTHON_9.3", code_block=codeblock_home)


# Creating field to denote School/Work/Home. Based on speed (<cond.) and within buffer 1=at home and 2=at work and 0=neither
codeblock_school=  """def Reclass(speed,DIST_SCHL,P_C):
    if speed<10 and DIST_SCHL<=50 and P_C=="C":
        return 1
    else:
        return 0"""
# Determining distances and putting these into a new field 'DIST_HOME'
arc.Near_analysis(shapefile,school)
arc.AddField_management(shapefile,"DIST_SCHL","FLOAT")
arc.CalculateField_management(shapefile, field="DIST_SCHL", expression="!NEAR_DIST!", expression_type="PYTHON_9.3")
arc.DeleteField_management(shapefile,"NEAR_DIST")
arc.DeleteField_management(shapefile,"NEAR_FID")
# New field that will be populated with /1 based on codeblock
arc.AddField_management(shapefile,"SCHL","FLOAT")
arc.CalculateField_management(shapefile, field="SCHL", expression="Reclass(!speed!,!DIST_SCHL!,!P_C!)", expression_type="PYTHON_9.3", code_block=codeblock_school)

# Creating field to denote commuting. BAsed on Proximity to roads (<15m) and speed (>15 km/h)
codeblock_work=  """def Reclass(speed,DIST_WORK,P_C):
    if speed<10 and DIST_WORK<=50 and P_C=="P":
        return 1
    else:
        return 0"""
# Determining distances and putting these into a new field 'DIST_ROAD'
arc.Near_analysis(shapefile,work) #this outputs 'NEAR_DIST'
arc.AddField_management(shapefile,"DIST_WORK","FLOAT")
arc.CalculateField_management(shapefile, field="DIST_WORK", expression="!NEAR_DIST!", expression_type="PYTHON_9.3")
arc.DeleteField_management(shapefile,"NEAR_DIST")
arc.DeleteField_management(shapefile,"NEAR_FID")
# New field that will be populated with /1 based on codeblock
arc.AddField_management(shapefile,"WORK","FLOAT")
arc.CalculateField_management(shapefile, field="WORK", expression="Reclass(!speed!,!DIST_WORK!,!P_C!)", expression_type="PYTHON_9.3", code_block=codeblock_work)

# Creating field to denote commuting. BAsed on Proximity to roads (<15m) and speed (>10 km/h)
codeblock_commute=  """def Reclass(speed,DIST_ROAD):
    if speed>4.8 and DIST_ROAD<20:
        return 1
    elif speed>10:
        return 1
    elif DIST_ROAD<15:
        return 1
    else:
        return 0"""
# Determining distances and putting these into a new field 'DIST_ROAD'
arc.Near_analysis(shapefile,roads)
arc.AddField_management(shapefile,"DIST_ROAD","FLOAT")
arc.CalculateField_management(shapefile, field="DIST_ROAD", expression="!NEAR_DIST!", expression_type="PYTHON_9.3")
arc.DeleteField_management(shapefile,"NEAR_DIST")
arc.DeleteField_management(shapefile,"NEAR_FID")
# New field that will be populated with /1 based on codeblock
arc.AddField_management(shapefile,"COMMUTE","FLOAT")
arc.CalculateField_management(shaefile, field="COMMUTE", expression="Reclass(!speed!,!DIST_ROAD!)", expression_type="PYTHON_9.3", code_block=codeblock_commute)

# Create column that denotes when no classes are defined (0)
arc.AddField_management(shapefile,"no_class","FLOAT")
arc.CalculateField_management(shapefile, field="no_class", expression="!COMMUTE! + !HOME! + !SCHL! + !WORK!", expression_type="PYTHON_9.3")



# This script dictates a set of criteria to remove points due to GPS collection problems
# 0 = DO NOT use this point and 1 = point is VALID

import arcpy as arc

shapefile = "./path/data"



codeblock_QC=  """def Reclass(speed,QC):
    if speed >=150:
        return 0
    else:
        return 1"""


arc.AddField_management(shapefile,"QC","INTEGER")
arc.CalculateField_management(shapefile, field="QC", expression="Reclass(!speed!,!QC!)", expression_type="PYTHON_9.3", code_block=codeblock_QC)



def Reclass(PA,distance):
    if PA=="MVPA" and distance==1:
        return "MT"
    elif PA=="MVPA" and distance==0:
        return "MS"
    elif PA=="LA" and distance==1:
        return "LT"
    elif PA=="LA" and distance==0:
        return "LS"
    elif PA=="SED" and distance==1:
        return "ST"
    elif PA=="SED" and distance==0:
        return "SS"


import arcpy as arc
from arcpy import env
arcpy.env.workspace = "./path/gdb"
roads = "./path/roads"

codeblock_commute=  """def Reclass(speed,DIST_ROAD):
    if speed>4.8 and DIST_ROAD<20:
        return 1
    elif speed>10:
        return 1
    elif DIST_ROAD<15:
        return 1
    else:
        return 0"""
for fc in arc.ListFeatureClasses():
    arc.Near_analysis(fc,roads)
    arc.AddField_management(fc,"DIST_ROAD","FLOAT")
    arc.CalculateField_management(fc, field="DIST_ROAD", expression="!NEAR_DIST!", expression_type="PYTHON_9.3")
    arc.DeleteField_management(fc,"NEAR_DIST")
    arc.DeleteField_management(fc,"NEAR_FID")
    arc.AddField_management(fc,"COMMUTE","FLOAT")
    arc.CalculateField_management(fc, field="COMMUTE", expression="Reclass(!speed!,!DIST_ROAD!)", expression_type="PYTHON_9.3", code_block=codeblock_commute)
