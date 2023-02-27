import math
import random
from link import *
from joint import *
import constants as c
import copy
import utils

class RandomCreature():
    def __init__(self, uid=0, dimension=3, numLinks=8, linkTypes=['rectangle'], scale=[0.3,0.3]):
        self.uid = uid
        self.dimension = dimension
        self.numLinks = numLinks
        self.linkTypes = linkTypes
        self.scale = scale
        self.buffer = self.scale[1] / 2 + 0.1*self.scale[1]
        
        self.generate_links()
        self.generate_joints()
        self.original_links = copy.deepcopy(self.links)
        self.original_joints = copy.deepcopy(self.joints)
        self.create_body_plan()
        #self.set_diameter() #list
    
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
        # if self.numSensors == 0:
        #     print('numSensors is zero, adding one')
        #     self.links[0].set_sensor(1)
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
        self.links_with_positions = []
        self.joint_groups = []
        self.master_plan = []
        if self.dimension == 1:
            self.links[0].position = [c.x,c.y,self.startZ]
            for i in range(1,len(self.links)):
                self.links[i].position = [0,self.links[i].dims[1]/2,0]
            self.joints[0].position = [c.x, c.y + self.links[0].dims[1]/2, self.startZ]
            #for i in range(1, len())

            ### finish ###

        else:
            # startZ is the max height the creature could end up being
            self.links[0].abs_pos = [c.x,c.y,self.startZ]
            self.add_link_position(None, self.links[0], [c.x,c.y,self.startZ], [0,0,0])
            

            for i in range(1,len(self.links)):
                # do while loop structure
                #self.links[i].dims[2] += i*0.01
                attempts = 0
                total_attempts = 0
                open_list = []
                while True:
                    if attempts > 20 or (not open_list and attempts > 0):
                        self.links[i] = RectangleLink(name=f'Link{i}',random=1, s=self.links[i].sensor)
                        attempts = 0
                    
                    rand_link = self.links_with_positions[random.randint(0,len(self.links_with_positions)-1)]
                    #open_list = rand_link.open_faces
                    if attempts == 0:
                        open_list = rand_link.open_faces[:]
                    while not open_list:
                        rand_link = self.links_with_positions[random.randint(0,len(self.links_with_positions)-1)]
                        open_list = rand_link.open_faces[:]
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
                        try: # do not halt if these fail
                            rand_link.open_faces.remove(rand_dir)
                            self.links[i].open_faces.remove([-x for x in rand_dir])
                        except Exception:
                            pass
                        break
                    else:
                        open_list.remove(rand_dir)
                # will be called len(links)-1 times, as desired
                # compute position for joint 
                # refactor this
                    attempts += 1
                    total_attempts += 1
                self.add_joint(i-1,rand_link,self.links[i], jp)
    
    def remove_joints(self, joints):
        for je in joints:
            if type(je) == list:
                for j in je:
                    self.joints.remove(j)
                self.joint_groups.remove(je)
            else:
                self.joints.remove(je)

    def add_joint(self,jointIndex,from_link, to_link, position):
        if from_link.prev_direction == [0,0,0]:
            # absolute positions
            position = [position[0] + c.x, position[1] + c.y, position[2] + self.startZ]
        if len(self.jointAxesList[jointIndex]) == 1:
            new_joint = RevoluteJoint(from_link,to_link, self.jointAxesList[jointIndex][0], position=position)
            self.joints.append(new_joint)
            self.joint_groups.append([new_joint])
            self.master_plan.append(new_joint)
           # to_link.received_joints.append(new_joint)
        else:
            new_cubes = []
            for i in range(len(self.jointAxesList[jointIndex])-1):
                new_cubes.append(RectangleLink(f'Cube{i}{jointIndex}', position=[0,0,0], random=0, width=0, height=0, length=0, sensor=0))
            all_links = [from_link]
            all_links.extend(new_cubes)
            all_links.append(to_link)
            ls = self.jointAxesList[jointIndex]
            curr_joints = []
            for i in range(0,len(ls)):
                pos = position
                if i != 0:
                    pos = [0,0,0]
                new_joint = RevoluteJoint(all_links[i],all_links[i+1],ls[i], position=pos)
                self.joints.append(new_joint)
                curr_joints.append(new_joint)
                self.master_plan.append(new_joint)
               # to_link.received_joints.append(curr_joints)
            self.joint_groups.append(curr_joints)
        

    def add_link_position(self,from_link,link,pos,dir, i=0):
        # if this is the root link of the body
        if not from_link: 
            link.prev_direction = dir
            link.position = pos
            link.from_link = link
            self.links_with_positions.append(link)
            return
        # otherwise, we have a from_link
       
        abs_pos = [from_link.abs_pos[i] + dir[i]*from_link.dims[i]/2 + pos[i] for i in range(len(pos))]
        # print(f"\n ======= \n From link abs pos: {from_link.abs_pos}\n New link abs pos: {abs_pos}\n ======= \n")
        # print(f"from_link dims: {from_link.dims}")
        # print(f"new_link dims: {link.dims}")
        if not self.intersection(link,abs_pos):
            link.abs_pos = abs_pos
            link.prev_direction = dir
            link.position = pos
            link.from_link  = from_link
            self.links_with_positions.append(link)
            return True
        else:
            return False

    def intersection(self,link,abs_pos):
        td = link.dims
        proximity_count = 0
        distances = []

       
        for other_link in self.links_with_positions:
            cp = other_link.abs_pos
            for i in range(3):  
                curr = utils.euclidean_distance(cp, abs_pos)
                if curr < max(td):
                    return True
                
                # dim_distances = [abs(cp[i]-abs_pos[i]) for i in range(3)]

                # if min(dim_distances) < 0.1:
                #     return True
                distances.append(curr)
        
        print(f"adding link, euclidean distance: {min(distances)}")
        return False


    # minor tweaks for later in evolution
    def small_mutate(self, extreme=0):
        #randomly remove some number of links, and/or change some of the joints.
        # depending on which joints/links are added/removed, make sure to update num_sensors and num_joints 
        
       #self.child = copy.deepcopy(self)

        # type of mutation 
        
        tm = random.randint(0,10)
        if extreme==1:
            tm = 10
        if tm <= 0 and tm <= 9:
            # change random number of links (only end links)
            links = []
            nl = random.randint(1,min(len(self.links)-1,3))
            while len(links) < nl:
                proposed_link = self.links[random.randint(0,len(self.links)-1)]
                if len(proposed_link.open_faces) == 5:
                    links.append(proposed_link)

            for link in links:
                self.mutate_link(link)
            
        # if two joints STACK, this becomes a problem
        # elif tm == 1:
        #     # change random number of joints
        #     joints = random.sample(self.joints, k=random.randint(1,max(len(self.joints),5)))
        #     for joint in joints:
        #         jointAxes = ['1 0 0', '0 1 0', '0 0 1']
        #         jointAxes.remove(joint.axis)
        #         joint.axis = jointAxes[random.randint(0,1)]
        # elif tm == 1:
        #     # randomly remove an (end) link
        #     to_remove = self.links[random.randint(0,len(self.links)-1)]
        #     while len(to_remove.open_faces) != 5:
        #         to_remove = self.links[random.randint(0,len(self.links)-1)]
        #     if to_remove.sensor == 1:
        #         self.numSensors -= 1
        #         self.numLinks -= 1
        #    # self.remove_joints(to_remove.received_joints)
        #     self.links.remove(to_remove)
        #     # also need to remove the corresponding joint


        # regen the entire thing
        elif tm == 10:
            print('new body plan')
            self.links = self.original_links
            self.joints = []
            self.create_body_plan()

    def mutate_link(self, link):
        # will only ever be called once abbs_pos is defined
        if not link.abs_pos:
            raise Exception('Link absolute position is not defined but mutate is called')
        attempts = 0
        while True:
            if attempts > 3000:
                print("attempts 3000. giving up")
                return
            former_dims = link.dims[:]
            for i in range(3):
                link.dims[i] = max(0.2,random.gauss(mu=link.dims[i], sigma=0.3))

            new_pos = [link.prev_direction[j] * link.dims[j]/2 for j in range(3)]
            from_link = link.from_link
            abs_pos = [from_link.abs_pos[i] + link.prev_direction[i]*from_link.dims[i]/2 + new_pos[i] for i in range(len(new_pos))]
            if not self.intersection(link, abs_pos):
               # print('Successfully mutated link')
                link.position = new_pos
                link.abs_pos = abs_pos
                break
            else:
                link.dims = former_dims
            attempts += 1

    def num_sensors(self):
        return self.numSensors

    def num_joints(self):
        return self.numJoints




