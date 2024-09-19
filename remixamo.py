import bpy
from bpy import data as _d
from bpy import context as _c
from bpy import ops as _o

def ren_actions():    
    for _a in range(len(_d.actions)):
        a = _d.actions[_a]
        a.name = str(_a)

def push_all_down():
    for ob in bpy.context.scene.objects:
        if ob.animation_data is not None:
            action = ob.animation_data.action
            if action is not None:
                track = ob.animation_data.nla_tracks.new()
                track.strips.new(action.name, int(action.frame_range[0]), action)
                ob.animation_data.action = None

def action_len(action):
        action_length = action.frame_range.y - action.frame_range.x
        return(action_length)

def first_len():
    return action_len(_d.actions["0"])


def collate_actions(gap_size):
    
    # For first:
    # - get the length + the gap size (for cursor placement)
    # For each:
    # - set the cursor to current cursor location + previous length + gap size
    # For all:
    # - add action
    bpy.context.scene.frame_current = 0
    flag = False
    _area = None
    for area in _c.screen.areas:
        if area.type == "NLA_EDITOR":
            if flag == False:
                _area = area
                flag = True
                break

    for index in range(len(_d.actions)):
        action_name = str(index)
        action = _d.actions[action_name]
        cursor_loc = bpy.context.scene.frame_current
        length = action_len(action)
        add_action = False
        if action.name == "0":
            # set location to zero if it's the first action
            cursor_loc = action_len(action) + gap_size
            #bpy.context.scene.frame_current = int(loc)
        else:
            # set the location to the last action's length + the gap size + the current location
            cursor_loc = action_len(_d.actions[str(index - 1)]) + gap_size + cursor_loc
            #bpy.context.scene.frame_current = int(loc)
            flag = False
            add_action = True
        
        if add_action == True:
            bpy.context.scene.frame_current = int(cursor_loc)
            area = bpy.context.area
            old_type = area.type
            area.type = 'NLA_EDITOR'
            _c.temp_override(active_object=area)
            print(cursor_loc)
            bpy.ops.nla.actionclip_add(action=action.name)
            area.type = old_type
    _c.scene.frame_current = 0

                    
def get_last_root_key_values(act,root,index_offset,get_z):
    last_key_values = []
    last_key_values.append(act.groups[root].channels[index_offset].keyframe_points[-1].co.y)
    last_key_values.append(act.groups[root].channels[index_offset + 1].keyframe_points[-1].co.y)
    if get_z:
        last_key_values.append(act.groups[root].channels[index_offset + 2].keyframe_points[-1].co.y)
    else:
        last_key_values.append(0)

    return last_key_values


#for idx in range(len(_d.actions)):
#    action = _d.actions[str(idx)]
#    last_keys = get_last_root_keys(action,"Root",0,False)
#    print(last_keys)


#flag_first = True
#root_group = "mixamorig:Hips"
def offset_action_root(root_fcurve_group,channel_index_offset,move_z):
    
    for action_index in range(len(_d.actions)):
        act = _d.actions[str(action_index)]
        last_action = None
        if act.name == "0":
            continue
        else:
            last_action = _d.actions[str(action_index-1)]

        root_bone_offsets = get_last_root_key_values(last_action,root_fcurve_group,channel_index_offset,move_z)
        
        channel_keyframe_map = {}
        # Do we move z? I dunno...
        channel_range = 3

        this_group = act.groups[root_fcurve_group]
        for chan_idx in range(0 + channel_index_offset, channel_index_offset + channel_range):
                        
            this_channel = this_group.channels[chan_idx + channel_index_offset]
            
            keyframe_list = []
            for key in this_channel.keyframe_points:
                new_value = key.co.y + root_bone_offsets[chan_idx]
                if move_z == False and chan_idx - channel_index_offset == 1:
                    new_value = key.co.y
                this_channel.keyframe_points.insert(key.co.x,new_value,options={"REPLACE"})

# If you're a chaos-inspired weirdo like me, and you want to burn it all down, run these all at once.
# What I would really like to do is make this a proper addon, but I'm not there yet.
# Uncomment these one by one and observe the chaos. Adjust as needed

# print("Renaming actions to '0' through the number of actions in the scene")
#ren_actions()

# print("Pushing all actions down to NLA tracks")
#push_all_down()

# print("Consolidate actions into one track (the first, usually '0') with a gap size of 10")
#collate_actions(10)

# Offset each action's root bone by the last frame's root bone position. Last argument is whether or not to move the Z axis.
# NOTE: the root bone z axis movement is slightly broken. The z axis is not being moved correctly but the x and y are.
# NOTE: THIS CAN PROBABLY BE DONE MORE ELEGANTLY WITH VECTOR MATH
offset_action_root("mixamorig:Hips",0,True)
