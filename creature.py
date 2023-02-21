import math
import random
from link import *
from joint import *
import constants as c

class RandomCreature():
    def __init__(self, dimension=3, numLinks=5, linkTypes=['rectangle'], scale=[0.3,0.3]):
        self.dimension = dimension
        self.numLinks = numLinks
        self.linkTypes = linkTypes
        self.scale = scale
        self.buffer = self.scale[1] / 2 + 0.1*self.scale[1]
        self.links_with_positions = []
        self.generate_links()
        self.generate_joints()
        self.create_body_plan()

    def generate_links(self):
        self.links = []
        self.maxZ = 0
        self.startZ = 0
        self.numSensors = 0
        for i in range(self.numLinks):
            currType = random.choice(self.linkTypes)
            if currType == 'rectangle':
                curr = RectangleLink(f'Link{i}',random=1)
                
                self.maxZ = curr.height if curr.height > self.maxZ else self.maxZ
                self.startZ += curr.height
                self.links.append(curr)
                if curr.sensor == 1:
                    self.numSensors += 1

        self.startZ *= 0.5

    def generate_joints(self):
        # randomly choose # of axes of rotation, and then:
        # choose random axis for each revolute joint
        self.numJoints = 0
        jointAxes = ['1 0 0', '0 1 0', '0 0 1']
        self.joints = []
        if self.dimension == 1:
            for i in range(self.numLinks-1):
                df = random.randint(1,3)
                self.numJoints += df
                randAxes = random.sample(jointAxes,k=df)
                self.joints.append(RevoluteJoint(parent=self.links[i], child=self.links[i+1], axes=randAxes))
        else:
            self.jointAxesList = []
            for i in range(self.numLinks-1):
                df = random.randint(1,3)
                self.numJoints += df
                randAxes = random.sample(jointAxes,k=df)
                self.jointAxesList.append(randAxes)

    def create_body_plan(self):
        dirs = [[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]]
        self.master_plan = []
        if self.dimension == 1:
            self.links[0].position = [c.x,c.y,self.startZ]
            for i in range(1,len(self.links)):
                self.links[i].position = [0,self.links[i].dims[1]/2,0]
            self.joints[0].position = [c.x, c.y + self.links[0].dims[1]/2, self.startZ]
            #for i in range(1, len())

            ### finish ###

        else:
            self.links[0].abs_pos = [c.x,c.y,self.startZ]
            self.add_link_position(None, self.links[0], [c.x,c.y,self.startZ], [0,0,0])
            
            
            # def get_volume(link):
            #     return link.dims[0] * link.dims[1] * link.dims[2]
            # self.links.sort(key=get_volume)
            # print([x.name for x in self.links])
            for i in range(1,len(self.links)):
                # do while loop structure
                #self.links[i].dims[2] += i*0.01
                attempts = 0
                while True:
                    if attempts > 20:
                        self.links[i] = RectangleLink(name=f'Link{i}',random=1)
                    

                    rand_link = self.links_with_positions[random.randint(0,len(self.links_with_positions)-1)]
                    open_list = rand_link.open_faces
                    rand_dir = open_list[random.randint(0,len(open_list)-1)]
                    
                    rd = rand_link.dims
                    pd = rand_link.prev_direction
                    d = rand_dir
                    jp = [(pd[0]+d[0])*rd[0]/2,
                                  (pd[1]+d[1])*rd[1]/2,
                                  (pd[2]+d[2])*rd[2]/2]
                    ld = self.links[i].dims
                    link_position = [d[0]*ld[0]/2,
                                     d[1]*ld[1]/2,
                                     d[2]*ld[2]/2]
                    if self.add_link_position(rand_link,self.links[i], link_position, rand_dir,i):
                        print('Adding link at abs pos: ', self.links[i].abs_pos)
                        rand_link.open_faces.remove(rand_dir)
                        self.links[i].open_faces.remove([-x for x in rand_dir])
                        break
                # will be called len(links)-1 times, as desired
                # compute position for joint 
                # refactor this
                    attempts += 1
                self.add_joint(i-1,rand_link,self.links[i], jp)
               # self.master_plan.append(self.links[i])
           # print([x.abs_pos for x in self.links_with_positions])
    def add_joint(self,jointIndex,from_link, to_link, position):
        if from_link.prev_direction == [0,0,0]:
            # absolute positions
            position = [position[0] + c.x, position[1] + c.y, position[2] + self.startZ]
        if len(self.jointAxesList[jointIndex]) == 1:
            new_joint = RevoluteJoint(from_link,to_link, self.jointAxesList[jointIndex][0], position=position)
            self.joints.append(new_joint)
            self.master_plan.append(new_joint)
        else:
            new_cubes = []
            for i in range(len(self.jointAxesList[jointIndex])-1):
                new_cubes.append(RectangleLink(f'Cube{i}{jointIndex}', position=[0,0,0], random=0, width=0, height=0, length=0, sensor=0))
            all_links = [from_link]
            all_links.extend(new_cubes)
            all_links.append(to_link)
            ls = self.jointAxesList[jointIndex]
            for i in range(0,len(ls)):
                pos = position
                if i != 0:
                    pos = [0,0,0]
                new_joint = RevoluteJoint(all_links[i],all_links[i+1],ls[i], position=pos)
                self.joints.append(new_joint)
                self.master_plan.append(new_joint)
        

    def add_link_position(self,from_link,link,pos,dir, i=0):
        if not from_link:
            link.prev_direction = dir
            link.position = pos
            self.links_with_positions.append(link)
            return
        abs_pos = [from_link.abs_pos[i] + from_link.dims[i]/2 + pos[i] for i in range(len(pos))]
        if not self.intersection(link,abs_pos,i):
            link.abs_pos = abs_pos
            link.prev_direction = dir
            link.position = pos
            self.links_with_positions.append(link)
            return True
        else:
            return False

    def intersection(self,link,abs_pos,i):
        td = link.dims
        proximity_count = 0
        distances = []
        def euclidean_distance(p,q):
             
            return math.pow((p[0]-q[0])**2 + (p[1] - q[1]) ** 2 + (p[2] - q[2]) ** 2,
                                            1/3)
        for other_link in self.links_with_positions:
            cp = other_link.abs_pos
            for i in range(3):
                curr = euclidean_distance(cp, abs_pos)
                if curr < max(td):
                    return True
                
                # dim_distances = [abs(cp[i]-abs_pos[i]) for i in range(3)]

                # if min(dim_distances) < 0.1:
                #     return True
                distances.append(curr)
        
        print(f"adding link, euclidean distance: {min(distances)}")
        return False


    def mutate(self):
        #randomly remove some number of links, and/or change some of the joints. If joints
        pass

    def num_sensors(self):
        return self.numSensors

    def num_joints(self):
        return self.numJoints




