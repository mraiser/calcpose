This project attempts to create a MakeHuman model using MediaPipe. 

[![Watch the video](https://img.youtube.com/vi/BZZrwHYLXkw/maxresdefault.jpg)](https://www.youtube.com/watch?v=BZZrwHYLXkw)

Requirements:
- 
- MakeHuman Community Edition
- Plugins: 
  - 8_server_socket https://github.com/mraiser/community-plugins-socket
  - 1_mhapi https://github.com/makehumancommunity/community-plugins-mhapi
- CV2
- MediaPipe
- Imutils
- Numpy
- An up-to-date working installation of the Newbound software https://github.com/mraiser/newbound

Installation:
-
1. Move the data/calcpose and runtime/calcpose folders into your Newbound installation's data and runtime folders, respectively
2. Launch the Newbound software
3. Toggle ON the "Inactive" apps in the Metabot app and select "Calcpose"
4. Click the "ACTIVATE" button
5. Copy the "mhrc/mhrc" folder (the *inner* one) (https://github.com/mraiser/community-plugins-socket/tree/master/cli/mhrc/mhrc) from community-plugins-socket to your Newbound installations "lib_python" folder
6. Restart the Newbound software
7. Launch MakeHuman as a separate process

*Instead of moving the data/calcpose and runtime/calcpose folders you can create symbolic links to them, leaving your git project folder intact for easy updating*

