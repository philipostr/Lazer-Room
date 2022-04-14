from tkinter import *
from lazer_sim import simulate

# Functions Called By TKinter Events

def set_error(msg):
    '''
        (str)->None
        Sets the error message widget as `msg`.
    '''
    error_lbl.config(text=msg)

def change_room(*_args):
    '''
        (ignored-arguments)->None
        Called when a change in the room is made.
    '''
    set_error('')
    roomc_btn.config(state=NORMAL)

def set_room():
    '''
        ()->None
        Called by clicking `roomc_btn`. Tests for errors in the
        room settings, and actually draws the room if no errors
        are found.
    '''
    roomc_btn.config(state=DISABLED)
    rows = rows_var.get()
    cols = cols_var.get()
    # there must be at least two possible placement positions
    if rows == 2 and cols == 2:
        set_error('Rows and columns cannot both be 2.')
        return

    inc_x = inc_x_var.get()
    if inc_x >= cols:
        set_error('Incidence X cannot be >= columns.')
        return
    inc_y = inc_y_var.get()
    if inc_y >= rows:
        set_error('Incidence Y cannot be >= rows.')
        return
    tar_x = tar_x_var.get()
    if tar_x >= cols:
        set_error('Target X cannot be >= columns.')
        return
    tar_y = tar_y_var.get()
    if tar_y >= rows:
        set_error('Target Y cannot be >= rows.')
        return

    if inc_x == tar_x and inc_y == tar_y:
        set_error('Incidence and target cannot be in same position.')
        return

    global curr_sim_num, sims
    row_diff = R_HEIGHT / rows
    col_diff = R_WIDTH / cols
    room.delete('all')
    create_grid(rows, cols, row_diff, col_diff)
    # draw the incidence point
    room.create_oval(inc_x*col_diff-5, inc_y*row_diff-5,
                     inc_x*col_diff+5, inc_y*row_diff+5,
                     width=0, fill='black')
    # draw the target point
    room.create_oval(tar_x*col_diff-5, tar_y*row_diff-5,
                     tar_x*col_diff+5, tar_y*row_diff+5,
                     width=0, fill='red')
    sim_btn.config(state=NORMAL)
    sim_switch_view.config(text='')
    sim_switch_left.config(state=DISABLED)
    sim_switch_right.config(state=DISABLED)
    curr_sim_num = 1
    sims = []

def switch_sim(diff):
    '''
        (int)->None
        Called with -1 by clicking `sim_switch_left`, and 1 by
        clicking `sim_switch_right`. Scrolls between the
        different simulated lazer paths.
    '''
    global curr_sim_num
    curr_sim_num += diff

    sim_switch_view.config(text=f'{curr_sim_num}/{len(sims)}')
    if curr_sim_num == 1:
        sim_switch_left.config(state=DISABLED)
    else:
        sim_switch_left.config(state=NORMAL)
    if curr_sim_num == len(sims):
        sim_switch_right.config(state=DISABLED)
    else:
        sim_switch_right.config(state=NORMAL)

    room.delete('lazer')
    draw_sim(sims[curr_sim_num-1])

def make_sims():
    '''
        ()->None
        Called by clicking`sim_btn`. It takes the currently set
        room conditions and makes all the possible lazer paths.
    '''
    rows = rows_var.get()
    cols = cols_var.get()
    inc = (inc_x_var.get(), inc_y_var.get())
    tar = (tar_x_var.get(), tar_y_var.get())
    dirs = simulate(cols, rows, inc, tar, bounce_var.get(),
                    bool(pass_var.get()))
    
    global curr_sim_num, sims
    curr_sim_num = 1
    sims = []
    for d in dirs:
        sims.append(create_sim(list(d)))
    switch_sim(0)

# Helper Functions

def create_grid(rows, cols, row_diff, col_diff):
    '''
        (int, int, num, num)->None
        Draws a grid with specified dimensions into the room widget.
    '''
    for c in range(1, cols):
        x_pos = c*col_diff
        room.create_line(x_pos, 0, x_pos, R_HEIGHT, width=3,
                         fill='#8e9e9a')
    for r in range(1, rows):
        y_pos = r*row_diff
        room.create_line(0, y_pos, R_WIDTH, y_pos, width=3,
                         fill='#8e9e9a')

def create_sim(simulation):
    '''
        ((int))->([(num)])
        `simulation` is a tuple containing
        (initial-direction-x, initial-direction-y, bounces)
        which describes the initial direction of the lazer as well
        as the amount of bounces within its path to the target point.
        The returned list contains tuple coordinates of the path
        vertices in order.

        That information is used in conjunction with linear functions
        to determine the bounce points and overall path that the
        laser will take.

        Basic premise is that if the laser is moving left, linear
        functions are used to determine the y position of the
        intersect between the left wall and the current laser
        path. If y is greater than the height of the ceiling, it must
        hit the ceiling. If it is between the ceiling and the floor,
        it must hit the left wall. If it is smaller than 0, it must
        hit the floor. Similar logic is used when moving right.
    '''
    rows = rows_var.get()
    cols = cols_var.get()
    row_diff = R_HEIGHT / rows
    col_diff = R_WIDTH / cols
    coord = [inc_x_var.get(), inc_y_var.get()]
    tar = (tar_x_var.get(), tar_y_var.get())
    points = []
    corner_bounce = 0

    for b in range(simulation[2]):
        # makes sure that corner bounces count as two bounces
        if corner_bounce == 2:
            corner_bounce = 0
            continue
        corner_bounce = 0
        
        curr_sim = (simulation[0], simulation[1])
        if curr_sim[0] == 0:
            if curr_sim[1] < 0:
                x = coord[0]
                y = 0
            else:
                x = coord[0]
                y = rows
        elif curr_sim[1] == 0:
            if curr_sim[0] < 0:
                x = 0
                y = coord[1]
            else:
                x = cols
                y = coord[1]
        elif curr_sim[0] > 0:
            y = curr_sim[1]/curr_sim[0]*(cols-coord[0])+coord[1]
            # hit the ceiling
            if y >= rows:
                x = curr_sim[0]/curr_sim[1]*(rows-coord[1])+coord[0]
                simulation[1] = -simulation[1]
                corner_bounce += 1
            # hit the right wall
            if y <= rows and y >= 0:
                x = cols
                simulation[0] = -simulation[0]
                corner_bounce += 1
            # hit the floor
            if y <= 0:
                x = curr_sim[0]/curr_sim[1]*(-coord[1])+coord[0]
                simulation[1] = -simulation[1]
                corner_bounce += 1
            y = curr_sim[1]/curr_sim[0]*(x-coord[0])+coord[1]
        elif curr_sim[0] < 0:
            y = curr_sim[1]/curr_sim[0]*(-coord[0])+coord[1]
            # hit the ceiling
            if y >= rows:
                x = curr_sim[0]/curr_sim[1]*(rows-coord[1])+coord[0]
                simulation[1] = -simulation[1]
                corner_bounce += 1
            # hit the left wall
            if y <= rows and y >= 0:
                x = 0
                simulation[0] = -simulation[0]
                corner_bounce += 1
            # hit the floor
            if y <= 0:
                x = curr_sim[0]/curr_sim[1]*(-coord[1])+coord[0]
                simulation[1] = -simulation[1]
                corner_bounce += 1
            y = curr_sim[1]/curr_sim[0]*(x-coord[0])+coord[1]
            
        points.append((x*col_diff, y*row_diff))
        coord[0] = x
        coord[1] = y

    # to make sure the path reaches the target point properly,
    # simply include the target point as the last point in the
    # path instead of calculating to it.
    points.append((tar[0]*col_diff, tar[1]*row_diff))
    return points

def draw_sim(sim):
    '''
        (([(num)]))->None
        Draws the path determined by `create_sim` by simply drawing
        lines between each specified point.
    '''
    row_diff = R_HEIGHT / rows_var.get()
    col_diff = R_WIDTH / cols_var.get()
    previous_point = (inc_x_var.get()*col_diff, inc_y_var.get()*row_diff)
    for point in sim:
        room.create_line(*previous_point, *point, width=3,
                         fill='red', arrow=LAST,
                         arrowshape=(11, 10, 8), tag='lazer')
        previous_point = point

# Constants

R_HEIGHT = 500
R_WIDTH = 500

# Main Window Stuff

root = Tk()
root.title('Lazer Room!')
root.resizable(False, False)

# Room Widget Stuff

curr_sim_num = 1
sims = []

room = Canvas(root, height=R_HEIGHT, width=R_WIDTH,
                 bg='#34ebe1')
room.grid(row=0, column=0, padx=30, pady=30)

# Options Widget Stuff

opt_row = 0

opts = Frame(root, height=500, width=300)
opts.grid(row=0, column=1, padx=30, pady=30)
for i in range(0, 2):
    opts.columnconfigure(i, weight=1)
opts.grid_propagate(False)

# Options Row - 'Configuration Options'

Label(opts, text='Configuration Options').grid(
    row=opt_row, column=0, columnspan=2, pady=(0, 30), sticky=N
)

# Options Row - Max bounces

opt_row += 1
Label(opts, text='Max Bounces').grid(
    row=opt_row, column=0, sticky=W
)
bounce_var = IntVar(root, 0)
bounce_om = OptionMenu(
    opts, bounce_var, *[i for i in range(0, 21)],
)
bounce_om.grid(row=opt_row, column=1, sticky=E)

# Options Row - Can go through incidence point

opt_row += 1
Label(opts, text='Can Pass Through Incidence Point').grid(
    row=opt_row, column=0, sticky=W
)
pass_var = IntVar(root, 0)
pass_cbtn = Checkbutton(opts, variable=pass_var)
pass_cbtn.grid(row=opt_row, column=1, sticky=E)

# Options Row - Room's rows

opt_row += 1
Label(opts, text='Room\'s rows').grid(row=opt_row, column=0,
                                      sticky=W)
rows_var = IntVar(root, 2)
rows_om = OptionMenu(
    opts, rows_var, *[i for i in range(2, 21)],
    command=change_room
)
rows_om.grid(row=opt_row, column=1, sticky=E)

# Options Row - Room's columns

opt_row += 1
Label(opts, text='Room\'s columns').grid(row=opt_row, column=0,
                                         sticky=W)
cols_var = IntVar(root, 2)
cols_om = OptionMenu(
    opts, cols_var, *[i for i in range(2, 21)],
    command=change_room
)
cols_om.grid(row=opt_row, column=1, sticky=E)

# Options Row - 'Incidence Position (black):'

opt_row += 1
Label(opts, text='Incidence Position (black):').grid(
    row=opt_row, column=0, columnspan=2
)

# Options Row - Incidence X Position

opt_row += 1
Label(opts, text='X').grid(row=opt_row, column=0, sticky=W)
inc_x_var = IntVar(root, 1)
inc_x_om = OptionMenu(opts, inc_x_var,
                      *[i for i in range(1, 20)],
                      command=change_room)
inc_x_om.grid(row=opt_row, column=1, sticky=E)

# Options Row - Incidence Y Position

opt_row += 1
Label(opts, text='Y').grid(row=opt_row, column=0, sticky=W)
inc_y_var = IntVar(root, 1)
inc_y_om = OptionMenu(opts, inc_y_var,
                      *[i for i in range(1, 20)],
                      command=change_room)
inc_y_om.grid(row=opt_row, column=1, sticky=E)

# Options Row - 'Target Position (red):'

opt_row += 1
Label(opts, text='Target Position (red):').grid(
    row=opt_row, column=0, columnspan=2
)

# Options Row - Target X Position

opt_row += 1
Label(opts, text='X').grid(row=opt_row, column=0, sticky=W)
tar_x_var = IntVar(root, 1)
tar_x_om = OptionMenu(opts, tar_x_var,
                      *[i for i in range(1, 20)],
                      command=change_room)
tar_x_om.grid(row=opt_row, column=1, sticky=E)

# Options Row - Incidence Y Position

opt_row += 1
Label(opts, text='Y').grid(row=opt_row, column=0, sticky=W)
tar_y_var = IntVar(root, 1)
tar_y_om = OptionMenu(opts, tar_y_var,
                      *[i for i in range(1, 20)],
                      command=change_room)
tar_y_om.grid(row=opt_row, column=1, sticky=E)

# Options Row - Set Room Changes Button

opt_row += 1
roomc_btn = Button(opts, text='Set Room Changes',
                   state=DISABLED, command=set_room)
roomc_btn.grid(row=opt_row, column=0, columnspan=2)

# Options Row - Simulate Lazer Button

opt_row += 1
sim_btn = Button(
    opts, text='Simulate Lazer', command=make_sims, state=DISABLED
)
sim_btn.grid(row=opt_row, column=0, columnspan=2, pady=(20, 0))

# Options Row - Simulation Switcher

opt_row += 1
sim_switch_row = Frame(opts)
sim_switch_row.grid(
    row=opt_row, column=0, columnspan=2, pady=(20, 0), sticky=W+E
)
sim_switch_row.columnconfigure(0, weight=1)
sim_switch_row.columnconfigure(1, weight=1)
sim_switch_row.columnconfigure(2, weight=1)

sim_switch_left = Button(
    sim_switch_row, text='<<', state=DISABLED,
    command=lambda:switch_sim(-1)
)
sim_switch_view = Label(sim_switch_row)
sim_switch_right = Button(
    sim_switch_row, text='>>', state=DISABLED,
    command=lambda:switch_sim(1)
)
sim_switch_left.grid(row=0, column=0, sticky=W)
sim_switch_view.grid(row=0, column=1)
sim_switch_right.grid(row=0, column=2, sticky=E)

# Options Row - Error Messages

opt_row += 1
opts.rowconfigure(opt_row, weight=1)
error_lbl = Label(opts, fg='red')
error_lbl.grid(row=opt_row, column=0, columnspan=2, sticky=S)

# main program

root.mainloop()
