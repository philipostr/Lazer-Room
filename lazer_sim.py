from math import gcd

# Helper Functions

def smallest_vec(vec):
    '''
        ((int))->(int)
        'Normalizes' a vector to its smallest possible integer
        components (compared to actual normalization, this is much
        more accurate as it uses ints not floats). Because it is
        used only for comparing if two vectors have the same
        direction, this is all that is needed.
    '''
    div = gcd(vec[0], vec[1])
    if div == 0:
        return vec
    return (vec[0]//div, vec[1]//div)

def generate_surroundings(og_room, room, width, height):
    '''
        (dict, dict, int, int)->[dict]
        `og_room` is used to calculate the differences in positions
        between points and barriers, where `room` uses these
        differences to calculate virtual positions of points in
        mirrored rooms as if they were part of one continuous plane.
    '''
    surroundings = []
    inc_right = width - og_room['inc'][0]
    inc_left = og_room['inc'][0]
    inc_up = height - og_room['inc'][1]
    inc_down = og_room['inc'][1]
    tar_right = width - og_room['tar'][0]
    tar_left = og_room['tar'][0]
    tar_up = height - og_room['tar'][1]
    tar_down = og_room['tar'][1]

    # left-right and up-down are interchanged depending on the
    # reflected nature of the mirrored room.
    if room['xflip']:
        inc_right, inc_left = inc_left, inc_right
        tar_right, tar_left = tar_left, tar_right
    if room['yflip']:
        inc_up, inc_down = inc_down, inc_up
        tar_up, tar_down = tar_down, tar_up
        
    # up
    surroundings.append({
        'inc': (
            room['inc'][0], room['inc'][1] + 2*inc_up
        ),
        'tar': (
            room['tar'][0], room['tar'][1] + 2*tar_up
        ),
        'xflip': room['xflip'],
        'yflip': not room['yflip']
    })
    # right
    surroundings.append({
        'inc': (
            room['inc'][0] + 2*inc_right, room['inc'][1]
        ),
        'tar': (
            room['tar'][0] + 2*tar_right, room['tar'][1]
        ),
        'xflip': not room['xflip'],
        'yflip': room['yflip']
    })
    # down
    surroundings.append({
        'inc': (
            room['inc'][0], room['inc'][1] - 2*inc_down
        ),
        'tar': (
            room['tar'][0], room['tar'][1] - 2*tar_down
        ),
        'xflip': room['xflip'],
        'yflip': not room['yflip']
    })
    # left
    surroundings.append({
        'inc': (
            room['inc'][0] - 2*inc_left, room['inc'][1]
        ),
        'tar': (
            room['tar'][0] - 2*tar_left, room['tar'][1]
        ),
        'xflip': not room['xflip'],
        'yflip': room['yflip']
    })
    return surroundings

def distance(vec1, vec2):
    '''
        ((int), (int))->num
        Simple Pythagorean theorem implementation to determine
        the distance between two vectors on a plane.
    '''
    return ((vec1[0]-vec2[0])**2 + (vec1[1]-vec2[1])**2)**0.5

# Principal Function

def simulate(width, height, inc, tar, bounces, ignore_inc):
    '''
        (int, int, (int), (int), int, boolean)->[(int)]
        Takes the dimensions of a room, the positions of incidence
        and the target, the max allowed bounces, and whether the
        laser is allowed to pass through the incidence point. What is
        returned is a list of tuples with the pattern
        (x-direction, y-direction, bounces) where the initial
        direction of the laser is split into its x and y components
        and the amount of bounces for that laser to reach the target.
        Naturally, all initial laser directions will be returned
        by this function; that is its main purpose.
    '''
    valid_dirs = []
    og_room = {'inc': inc, 'tar': tar, 'xflip': False, 'yflip': False}
    room_queue = [og_room]
    # for making sure that initial directions are not used more than
    # once.
    used_dirs = set()
    # for making sure that reflected targets are not used more than
    # once.
    used_tars = {tar}
    # reflection layer for the current `room_queue` (aka how many
    # bounces it will take to reach).
    layer = 0
    layer_size = 1
    
    while room_queue:
        curr_room = room_queue.pop(0)
        layer_size -= 1

        tar_dir = smallest_vec((
            curr_room['tar'][0]-inc[0], curr_room['tar'][1]-inc[1]
        ))

        if not ignore_inc:
            tar_dist = distance(inc, curr_room['tar'])
            inc_dir = smallest_vec((
                curr_room['inc'][0]-inc[0], curr_room['inc'][1]-inc[1]
            ))
            inc_dist = distance(inc, curr_room['inc'])

            if tar_dir not in used_dirs:
                if inc_dir != tar_dir or inc_dist > tar_dist:
                    valid_dirs.append((*tar_dir, layer))
                    used_dirs.add(tar_dir)
            used_dirs.add(inc_dir)
                
        elif tar_dir not in used_dirs:
            valid_dirs.append((*tar_dir, layer))
            used_dirs.add(tar_dir)

        # add surrounding rooms to `room_queue`
        
        if layer < bounces:
            next_rooms = [
                r for r in generate_surroundings(og_room, curr_room,
                                                 width, height)
                if r['tar'] not in used_tars
            ]
            for r in next_rooms:
                used_tars.add(r['tar'])
            room_queue.extend(next_rooms)

            if layer_size == 0:
                layer += 1
                layer_size = len(room_queue)

    return valid_dirs
