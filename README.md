# mixamizer

## Some Stuff
* Make sure you have the NLA editor open in one of your "areas" when you run the script fromm the text editor.
* Make sure you have ONE track selected in the NLA editor. This track SHOULD BE for whatever armature/action that is the 'zero' action.
* Don't run all these functions at once. Do them function by function and observe the results. *I want comments and feedback, and I would love for someone to fork this.*

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
