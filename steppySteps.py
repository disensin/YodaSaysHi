import maya.cmds as mc


"""
ISAI CALDERON
February 2, 2017
Assignment 02 - Step Master?
Instructor: Geordie Martinez
Class: Learn Python Inside Maya
School: CG Society
"""



# Settings for my stairs

settings = {
            'degrees':1,
            'spread':.6,
            'stepHeight':0.5,
            'stepLength':5,
            'stepName':'pasito',
            'steps':300,
            'columnWidth':200,
            'railHeight':5
            }

# Shorten the names of all the variables
grados = float(settings['degrees'])
largo = float(settings['stepLength'])
alto = float(settings['stepHeight'])
profundo = int(settings['spread'])
gradas = settings['steps']
grueso = float(settings['columnWidth'])
rielAltura = float(settings['railHeight'])
curves = []

# Create parent group
allSteps = mc.group(em=1,name='steppySteps'+str(01))



# Math for railing and column heights and thickness
gruesoAjustado=((largo + (grueso/(1 + (1/grueso))))*2-(largo/5))
altoAjustado = (alto* 1.15 * (360/grados))

# RAIL BASE
# Make the helix for the railing system
helixMake = mc.polyHelix(
                        c=1,
                        h=altoAjustado,
                        w= gruesoAjustado,
                        radius = 1,
                        sa = 3,
                        sco = 3*360/grados,
                        sc = 0,
                        d=1
                        )[0]

# Move railing up
mc.xform(t=(0,altoAjustado/2,0))

# Select edges to create the first rail.
mc.select(helixMake + '.e[' + (str(int((3*360/grados)*3+5))) + ']')
mc.select(helixMake + '.e[' + (str(int((3*360/grados)*3+8))) + ']', add=True)
mc.select(helixMake + '.e[' + (str(int((3*360/grados)*3+11))) + ']', add=True)

# Convert edges into curve and save it into the variable "curve"
curve = mc.polyToCurve(form = 0, degree =1)[0]



# CREATE THE STAIRS
# Loop through each step: 1) Step, 2) Rail bars, 3) Rail ends, 4) Move 'em all together
for i in range(0,gradas):
    # Set the stair's name
    nombre = settings['stepName'] + str(i)
    
    # Create the rotation and translation group for the step
    stepGRP = mc.group(name = nombre + '_GRP',em = 1)
    
    
    
    # Create the step
    stepGEO = mc.polyCube(
                          name = nombre + '_GEO',
                          width = largo,
                          height = alto,
                          depth = profundo,
                          sx = 1,
                          sy = 1,
                          sz = 1,
                          )[0]
    # Move it over. It will stay along the edge of the column.
    mc.setAttr( stepGEO + '.translateX', ((largo/2) + (grueso/(1 + (1/grueso)))))
    
    # Create the rail's bars
    railBar = mc.polyCylinder(
                              name = nombre + '_column_GEO',
                              radius = .1,
                              height = rielAltura,
                              sa=grueso*5.4
                              )[0]
    
    # Create ends for the rails
    if i == 0 or i == gradas-1:
        # Make the sphere
        railEnd = mc.polySphere(name = 'rail'+str(i),r=.5)[0]
        # Move it up
        mc.setAttr( railEnd + '.translateY', rielAltura/2)
        # Parent it beneath the rail bar
        mc.parent(railEnd,railBar)
    
    # Move the rail bar over in X and Y
    mc.setAttr( railBar + '.translateX', (((largo/2) + (grueso/(1 + (1/grueso))))+(largo/2.5)))
    mc.setAttr( railBar + '.translateY', rielAltura/2)
    
    # Parent the rail bar to the step's group
    mc.parent(railBar,stepGRP)
    
    # Ignore the curve creation for the last step. There will be a sphere here instead.
    if i != gradas-1:
        
        # Duplicate the individual curve
        curvy = mc.duplicate(curve,name='railCurve'+str(i))[0]
        
        # Move the curve up
        mc.setAttr( curvy + '.translateY', rielAltura)
        
        # Place the new curve into the curves list
        curves += [curvy]
        
        # Parent the curve to the step group
        mc.parent(curvy,stepGRP)
    
    # Parent the step into the step's group
    mc.parent(stepGEO, stepGRP)

    # Rotate the group by the set amount of degrees
    mc.setAttr( stepGRP + '.rotateY', (i * grados))
    
    # Move the group up
    mc.setAttr(stepGRP + '.translateY', (i * alto * 1.15))
    
    # Place everything inside the top-most group (or the STAIR-MASTER!!)
    mc.parent(stepGRP,allSteps)
    
    


# CREATE SINGLE COLUMN
# If column width is less than 5, default is 20. If over 200, default is 1000.
if grueso <= 5:
    column = mc.polyCylinder(
                            name = nombre + '_column_GEO',
                            radius = grueso,
                            height = alto*gradas*1.15,
                            sa=(20)
                            )[0]
elif grueso > 5 or grueso < 200:
    column = mc.polyCylinder(
                            name = nombre + '_column_GEO',
                            radius = grueso,
                            height = alto*gradas*1.15,
                            sa=(grueso*5)
                            )[0]
elif grueso > 200:
    column = mc.polyCylinder(
                            name = nombre + '_column_GEO',
                            radius = grueso,
                            height = alto*gradas*1.15,
                            sa=(1000)
                            )[0]
# Shift column up to match stair height
mc.setAttr(column + '.translateY', (alto*gradas*1.15/2)-alto/1.85)
# Parent column beneath pappy!
mc.parent(column,allSteps)


# RAIL PROCESS FINISHES HERE
# Make the completed rail curve from the previously created curves
railCurve = mc.attachCurve(curves,
                           ch = 0,
                           rpo = 0,
                           kmk = 0,
                           m=1,
                           bb = .5,
                           bki = 0,
                           p = .1
                           )[0]

# Create the rail's thickness
railThickness = mc.circle(r=.2)[0]

# Extrude the rail!!
riel = mc.extrude(railThickness, railCurve,
                  ch=0,
                  rn=False,
                  po=0,
                  et=2,
                  ucp=1,fpt=1,
                  upn=1,
                  rotation=0,
                  scale=1,
                  rsp=1
                  )
# Parent rail to the main group
mc.parent(riel,allSteps)

# Delete excess items
mc.delete(helixMake,curves,curve,railThickness,railCurve)

# Select the top group, ready for manipulation!
mc.select(allSteps)
