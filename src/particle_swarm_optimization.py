import random


def init_pso(data, feat_num, max_k, pop_size, threshold):
    
    particles = []
    particle_len = max_k + (max_k * feat_num)
    data_len = len(data)    
    for i in xrange(0, pop_size):
        temp_particle = []
        for j in xrange(0, max_k):
            temp_particle.append(random.random())
        counter = 0
        rand_set = set()
        for j in xrange(max_k, particle_len):
            if (counter == 0):
                rand = random.randint(0, (data_len - 1))
                while rand in rand_set:
                    rand = random.randint(0, (data_len - 1))
                center = data[rand]
                rand_set.add(rand)
            temp_particle.append(center[counter])
            counter = counter + 1
            if (counter == feat_num):
                counter = 0
        temp_particle = check_particle(temp_particle, threshold, max_k)
        particles.append(temp_particle)
    return particles

def check_particle(particle, threshold, max_k):
    k = 0
    for i in xrange(0, max_k):
        if particle[i] >= threshold:
            k += 1
    if (k < 2):
        for l in xrange(0, 2):
            rand_thresh = random.uniform(threshold, 1)
            rand_loc = random.randint(0, (max_k - 1))
            particle[rand_loc] = rand_thresh
    return particle

def find_max_min_ele(data, ele_ind):
    data_len = len(data)
    max_ele = 0
    min_ele = 99999
    for i in xrange(0, data_len):
        if data[i][ele_ind] > max_ele:
            max_ele = data[i][ele_ind]
        if data[i][ele_ind] < min_ele:
            min_ele = data[i][ele_ind]
    return {"max_ele":max_ele, "min_ele":min_ele}

def init_velocities(data, feat_num, max_k, chrom_len, pop_size):
    velocities = []

    for i in xrange(0, pop_size):
        temp_vel = []

        for j in xrange(0, max_k):
            temp_vel.append(0.5 * random.random())

        for j in xrange(0, max_k):
            for k in xrange(0, feat_num):
                plus_minus = random.random()
                elements = find_max_min_ele(data, k)
                max_ele = elements.get("max_ele")
                min_ele = elements.get("min_ele")
                if plus_minus > 0.5:
                    temp_vel.append(0.4 * random.uniform(min_ele, max_ele))
                else:
                    temp_vel.append((0.4 * random.uniform(min_ele, max_ele)) * -1)
        velocities.append(temp_vel)
    return velocities

def reinit_particle(particle, data, feat_num, max_k, threshold, debug_flag):
    if (debug_flag == True):
        print "Invalid centroid detected, reinitializing particle..."
    particle_len = len(particle)
    data_len = len(data)
    temp_particle = []
    for i in xrange(0, max_k):
        temp_particle.append(random.random())
    counter = 0
    rand_set = set()
    for i in xrange(max_k, particle_len):
        if (counter == 0):
            rand = random.randint(0, (data_len - 1))
            while rand in rand_set:
                rand = random.randint(0, (data_len - 1))
            center = data[rand]
            rand_set.add(rand)
        temp_particle.append(center[counter])
        counter = counter + 1
        if (counter == feat_num):
            counter = 0
    particle = temp_particle
    particle = check_particle(particle, threshold, max_k)
    return particle 

def get_center(particles, max_k, threshold, feat_num): 
    centers = []
    for i in xrange(0, max_k):
        temp_center = []
        if particles[i] >= threshold:
            first_element = max_k + (i * feat_num)
            last_element = first_element + feat_num
            for j in xrange(first_element, last_element):
                temp_center.append(particles[j])
            centers.append(temp_center)
    return centers

def update_position(particle, velocity, max_k, feat_num, data, debug_flag):
    if (debug_flag == True):
        print "particle before:", particle
        print "velocity:", velocity
    particle_len = len(particle)
    for i in xrange(0, particle_len):
        particle[i] = particle[i] + velocity[i]
    particle = check_position(particle, max_k, feat_num, data)
    if (debug_flag == True):
        print "particle after:", particle
    return particle
    

def check_position(particle, max_k, feat_num, data):
    for i in xrange(0, max_k):
        if (particle[i] > 1.0):
            particle[i] = 1.0
        if (particle[i] < 0.0):
            particle[i] = 0.0
        first_element = max_k + (i * feat_num)
        last_element = first_element + feat_num
        counter = 0
        for j in xrange(first_element, last_element):
            max_min = find_max_min_ele(data, counter)
            max_ele = max_min.get("max_ele")
            min_ele = max_min.get("min_ele")
            if (particle[j] > max_ele):
                particle[j] = max_ele
            if (particle[j] < min_ele):
                particle[j] = min_ele
            counter = counter + 1
    return particle

def update_velocity(omega_min, omega_max, particle, velocity, weight, p_best, g_best, debug_flag):
    if (debug_flag == True):
        print "\nUpdating velocity..."
    omega_1 = random.uniform(omega_min, omega_max)
    omega_2 = random.uniform(omega_min, omega_max)
    particle_len = len(particle)
    if (debug_flag == True):
        print "Velocity before:", velocity
    for i in xrange(0, particle_len):
        velocity[i] = (weight * velocity[i]) + (omega_1 * (p_best[i] - particle[i])) + (omega_2 * (g_best[i] - particle[i]))
    if (debug_flag == True):
        print "Velocity after:", velocity
    return velocity

    
    