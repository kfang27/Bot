# Project Auto
The idea of this project is to create an automated bot that can play FGO. The plan is to have the automation screen capture the LDplayer window, read the screen capture and make decisions based on it. 

Before entering a stage, it will ask the user some questions (such as "Loop?', "How many times?", etc...) and follow a protocol when given the conditions

When in a stage, the bot will take a screenshot and analyze it every turn to decide what cards to play. I will most likely have it follow a pattern when it comes to looping a stage. 

When a stage is completed, it will look to see if the stage can be repeated based on certain conditions. 

Tools: PyAutoGUI for interaction (mouse movement, clicks...), maybe OpenCV for screen capture and analysis  

For looping process:  
- It will seek to use the skills of supports and target the DPS unit. 
- Click the "Attack" button and look for the DPS unit's cards
- During a scene transition, have the bot tap anywhere on the screen to skip the transition
- Repeat the process of using skills if needed, and attack