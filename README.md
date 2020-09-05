This project attempts to create a MakeHuman model using OpenFace. 

I'm not sure where I found applyModifier.py, genericCommand.py, getAppliedTargets.py, listAvailableModifiers.py or mhrc.JsonCall, but I didn't write them and credit is due.

Use main_approximate.py to iteratively adjust a MakeHuman model's face based on a source photo.

Use main_generate to generate a dataset with JPG files and corresponding MakeHuman modifier values in JSON format.

NOTE: Hard coded filenames make this unusable without modification to match your own environment for now.

Requirements:
- 
- MakeHuman Community Edition
- Plugin: 8_server_socket
- OpenFace
