# mixamizer

Run these in order:

### This will rename all of your actions to 0-len(actions)!!!!
### AND push them all down
### AND add the corresponding action strips to action["0"]
### AND set the value of root channels to the last value and offset every keyframe

### YOU HAVE BEEN WARNED
```python
# WARNING ZONE!!!!!

# rename
ren_actions()
push_all_down()
# Adds all actions to track for first action
# Arg = the gap between actions
collate_actions(10)
# offset_action_root args:
# root bone group
# group channel offset (if the channels aren't indexed starting at zero)
# move z = if you want to move the z channel. I found some animations to do weird stuff 
offset_action_root("Root",0,False)
```