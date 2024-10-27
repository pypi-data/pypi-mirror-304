# RVS Merging

This project is **NOT** to be set public.

It is an improved version of RVS with plenoptic, video streams, head mounted display, advanced configurations, external shaders, etc.



When the project is completed, it is to be cut in part, and only public parts are to be shared publicly.

# How to develop new feature:
suppose you are in the `master` branch. We pull last version and create a branch `new_feature` for our feature.

> git pull origin master

> git checkout -b new_feature

We can now develop the new feature in the `new_feature` branch.

When we have finished, let's merge the last version of master in our branch, and resolve all conflicts.

> git checkout master

> git pull origin master

> git checkout new_feature

> git pull origin master

When this is done, we can merge back our branch to master, but we do NOT want to push all the commits into master, as they could have non compiling code

> git checkout master

> git pull origin master

> git checkout -b new_feature_merging

> git merge --squash new_feature

> git commit # without -m

> git checkout master

> git merge new_feature_merging

Now ask all your teammates to pull master.


# TODO
    [ ] Make Python Build
        [ ] Integrate In Cmake 
        [ ] Publish Package In Pip
    [~] Merging plenoptic RVS last version with this project
    [v] Fix bug of bad resizing when all the input and output do not have the same resolution
    [~] NEW CMAKE
        [ ] CMAKE for HMD
        [ ] CMAKE for CUDA video decoder
            [ ] Find FFMPEG automatically, instead of using static libs in the code
    [~] OpenGL loading functions that work with windows and linux
    [~] Better profiler than easy profiler
    [ ] Integrate the better profiler (Tracy) into the code
    [ ] Optional build for public and private distribuable versions
        [ ] With cuda (?)
        [ ] With video decoder
        [x] With companion
        [ ] With Head mounted display (includes companion windows by default)
        [ ] Selecting which shaders are in the installation folder
    [ ] UNIT TESTS
    [ ] CI
    [ ] Integration tests with mean psnr when pushing into master ?
    [ ] Cleanup config files
        [ ] Profile files
        [ ] Bounding box stuffs
        [ ] Depth map/background parameters useless
        [ ] Version RVS
        [ ] BlendingMethod when opengl
        [ ] Block plenoptic
        [ ] Remove all old parameters in the json
        [ ] Rethink better parameters for different shaders, etc..
        [v] Remove double information between camera and config files
        [ ] default oculus camera embedded in code instead of config (?)
            [v] when not occulus take input camera parameters
            [ ] when occulus use oculus parameters ? maybe need to use FBO->resize()
    [ ] Better camera movements
        [v] Start with good rotation
        [v] Align translation with screens camera
        [v] Align rotation with screens camera
        [~] Do that for HMD also
    [ ] Refactor companion main
    [v] Vsync as a shortcut
    [ ] Posetrace
    [ ] Video from posetrace file
    [ ] Check all WITH_OPENGL and refactor them in the code
    [ ] SOLVE THE RELATIVE PATH TO SHADERS
    [x] Doxygen
    [ ] Not sure the "rvs" makefile is using OpenGL, check the cmake and at the execution


And way more things, such as:
    [ ] testing with random cameras in space
    [ ] big size scenes
    ...