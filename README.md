# SlimeVR-3D-Projects
A collection of projects or 3d models around slimevr


### Project Structure

#### **./resources**
Resources that are to be shared across scenes/renders are to go into this directory. For example,  Nighty character model would go here to be shared across render projects. 

#### **./projects**
This is where the projects for verious scenes, poses, and animations will go. 

#### **./render**
Each blender file in **./projects** will have it's own directory created here. All of the rendered images for a project can be found in the respective directories. 


## Usage
This section explains how to add a new pose. 
It's reccomended to watch a [beginner's tutorial](https://youtu.be/8gi9lUYMRcI?si=XMZEfs8m354rdvqH) for keyframing if you're unfamilliar with blender.  

### Adding Poses

1. To add a new pose, either start with a copy the _PROJECT_TEMPLATE.blend file or add onto an existing project if the new pose is related. 

2. Open the blender project and navigate to the animation tab if not already. 

3. Select the the armature by clicking one of the pose controls in Object Mode and then enter Pose Mode by selecting it from the dropdown box in the top left of the 3d viewport. 

4. Select a control object in Pose Mode and move it to change the positon of the avatar. 

5. To place a keyframe for the selected object, press the *i* key to place a keyframe at the current scrubber position. If you have multiple objects selected, keyframes for each object will be created. 

6. Once finished, set the End Frame to your last keyframe. 

https://github.com/user-attachments/assets/19c5e868-23c0-4cd4-9ba8-474090d7fc6c


### Linking New Collections:

1. In a blender file in ./resources, create a new collection and add contents to it. 

2. After saving and opening the project you wish to add it to, link the collection by going to **File->Link** and navigate to the blender file containing your collection. You will see the object structure of the blender file, navigate to **Collection->** and select your collection and link.

3. In your blender file, right click on the imported collection in the View Layer and select **Library Override->Make->Selected & Content**. Sometimes you may need to do this for child objects as well. 

https://github.com/user-attachments/assets/df0cc59e-d7b5-4199-8708-cbabb1c4b0fb



### Rendering: 
To render, run the following script in a terminal. 
```
python render.py [path to blender] 

Ex:
python render.py "C:\Program Files\Blender Foundation\Blender 4.3\blender-launcher.exe"
```






