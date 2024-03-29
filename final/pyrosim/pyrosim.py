import pybullet as p

from pyrosim.nndf import NNDF

from pyrosim.linksdf  import LINK_SDF

from pyrosim.linkurdf import LINK_URDF

from pyrosim.model import MODEL

from pyrosim.sdf   import SDF

from pyrosim.urdf  import URDF

from pyrosim.joint import JOINT

SDF_FILETYPE  = 0

URDF_FILETYPE = 1

NNDF_FILETYPE   = 2

# global availableLinkIndex

# global linkNamesToIndices

def End():

    if filetype == SDF_FILETYPE:

        sdf.Save_End_Tag(f)

    elif filetype == NNDF_FILETYPE:

        nndf.Save_End_Tag(f)
    else:
        urdf.Save_End_Tag(f)

    f.close()

def End_Model():

    model.Save_End_Tag(f)

def Get_Touch_Sensor_Value_For_Link(linkName):

    touchValue = -1.0

    desiredLinkIndex = linkNamesToIndices[linkName]

    pts = p.getContactPoints()

    for pt in pts:

        linkIndex = pt[4]

        if ( linkIndex == desiredLinkIndex ):

            touchValue = 1.0

    return touchValue

def Prepare_Link_Dictionary(bodyID):

    global linkNamesToIndices

    linkNamesToIndices = {}

    for jointIndex in range( 0 , p.getNumJoints(bodyID) ):

        jointInfo = p.getJointInfo( bodyID , jointIndex )

        jointName = jointInfo[1]

        jointName = jointName.decode("utf-8")

        jointName = jointName.split("_")

        linkName = jointName[1]

        linkNamesToIndices[linkName] = jointIndex

        if jointIndex==0:

           rootLinkName = jointName[0]

           linkNamesToIndices[rootLinkName] = -1 

def Prepare_Joint_Dictionary(bodyID):

    global jointNamesToIndices

    global jointNamesToType

    jointNamesToIndices = {}

    jointNamesToType = {}

    for jointIndex in range( 0 , p.getNumJoints(bodyID) ):

        jointInfo = p.getJointInfo( bodyID , jointIndex )

        jointName = jointInfo[1].decode('UTF-8')

        jointType = jointInfo[2]

        jointNamesToIndices[jointName] = jointIndex

        jointNamesToType[jointName] = jointType

def Prepare_To_Simulate(bodyID):

    Prepare_Link_Dictionary(bodyID)

    Prepare_Joint_Dictionary(bodyID)

def Send_Cube(name="default",pos=[0,0,0],size=[1,1,1],mass=1.0,color="0 1.0 1.0 1.0",color_name="Cyan",geometry_type="box"):

    global availableLinkIndex

    global links

    if filetype == SDF_FILETYPE:

        Start_Model(name,pos)

        link = LINK_SDF(name,pos,size,mass)

        links.append(link)
    else:
        link = LINK_URDF(name,pos,size,color,color_name,geometry_type)

        links.append(link)

    link.Save(f)

    if filetype == SDF_FILETYPE:

        End_Model()

    linkNamesToIndices[name] = availableLinkIndex

    availableLinkIndex = availableLinkIndex + 1

def Send_Joint(name,parent,child,type,position,jointAxis):

    joint = JOINT(name,parent,child,type,position)

    joint.Save(f,jointAxis)

def Send_Motor_Neuron(name,jointName):

    f.write('    <neuron name = "' + str(name) + '" type = "motor"  jointName = "' + jointName + '" />\n')

def Send_Sensor_Neuron(name,linkName):

    f.write('    <neuron name = "' + str(name) + '" type = "sensor" linkName = "' + linkName + '" />\n')

def Send_Synapse( sourceNeuronName , targetNeuronName , weight ):

    f.write('    <synapse sourceNeuronName = "' + str(sourceNeuronName) + '" targetNeuronName = "' + str(targetNeuronName) + '" weight = "' + str(weight) + '" />\n')

 
def Set_Motor_For_Joint(bodyIndex,jointName,controlMode,targetPosition,maxForce):

    if jointNamesToType[jointName]  == p.JOINT_REVOLUTE:
        p.setJointMotorControl2(
            bodyIndex      = bodyIndex,
            jointIndex     = jointNamesToIndices[jointName],
            controlMode    = controlMode,
            targetPosition = targetPosition,
            force          = maxForce)
    elif jointNamesToType[jointName]  == p.JOINT_SPHERICAL:
        abs_limit = 0.78 #hard limit
        cliped_position = max(min(targetPosition, abs_limit), -abs_limit)
        target_orientation = p.getQuaternionFromEuler([cliped_position, cliped_position, cliped_position]) 
        p.setJointMotorControlMultiDof(
            bodyIndex, jointNamesToIndices[jointName], controlMode, targetPosition=target_orientation, force=[maxForce,maxForce,maxForce])
    else:
        p.setJointMotorControl2(
            bodyIndex      = bodyIndex,
            jointIndex     = jointNamesToIndices[jointName],
            controlMode    = controlMode,
            targetPosition = targetPosition,
            force          = maxForce)

def Start_NeuralNetwork(filename):

    global filetype

    filetype = NNDF_FILETYPE

    global f

    f = open(filename,"w")

    global nndf

    nndf = NNDF()

    nndf.Save_Start_Tag(f)

def Start_SDF(filename):

    global availableLinkIndex

    availableLinkIndex = -1

    global linkNamesToIndices

    linkNamesToIndices = {}

    global filetype

    filetype = SDF_FILETYPE

    global f
 
    f = open(filename,"w")

    global sdf

    sdf = SDF()

    sdf.Save_Start_Tag(f)

    global links

    links = []

def Start_URDF(filename):

    global availableLinkIndex

    availableLinkIndex = -1

    global linkNamesToIndices

    linkNamesToIndices = {}

    global filetype

    filetype = URDF_FILETYPE

    global f

    f = open(filename,"w")

    global urdf 

    urdf = URDF()

    urdf.Save_Start_Tag(f)

    global links

    links = []

def Start_Model(modelName,pos):

    global model 

    model = MODEL(modelName,pos)

    model.Save_Start_Tag(f)
