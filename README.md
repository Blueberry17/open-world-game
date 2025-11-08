# Open-world Procedural Generation Game
Procedural generation open-world game, developed for my A-Level coursework.

© 2024-2025 Anthony Berry.  
This project is part of my A-Level coursework.  
Shared publicly for viewing and educational purposes only.  
No reuse, redistribution, or modification is permitted without permission.

## Completed game testing

New world start-up example:

<img width="452" height="469" alt="image" src="https://github.com/user-attachments/assets/b38c4d94-ed93-4fc4-b9b8-d21629127565" />

More advanced gameplay:

<img width="452" height="469" alt="image" src="https://github.com/user-attachments/assets/3fcce6a0-eca9-4d0d-8774-0f25c30a4538" />


## Procedural generation prototyping

Perlin noise:

<img width="452" height="243" alt="image" src="https://github.com/user-attachments/assets/4e179564-b650-446a-8633-5ba6e4ff3f20" />

Combined with Voronoi diagrams:

<img width="452" height="451" alt="image" src="https://github.com/user-attachments/assets/07a34cf9-0cbc-4141-a3d5-cf06be866a52" />

## Project objectives and unit testing

For testing of game content, I have duplicated my quantitative project objectives table and provided evidence for each objective, either referencing a testing video or referencing a screenshot and explanation below the table. For video evidence, timestamps are cited from one of the videos (in the format m:ss). Video 2 contains many objectives that are also shown in video 1 to provide a greater feel of game content, these already-passed objectives are not specifically named (e.g. both show evidence of Qt2.1 – user movement, but it is not named for video 2). The video links for testing are below:
-	Video 1: https://youtu.be/FUJtOsW1Zgc (objectives Qt1.4, Qt2.1-2.6, Qt3.1-3.5).
-	Video 2: https://youtu.be/YW5LX02xTHM (objectives Qt1.5, Qt2.4, Qt2.6-2.7, Qt3.4, Qt4.1-4.2).

| ID | Description | Justification | Evidence | Passed? / Next Actions |
|----|--------------|----------------|-----------|-------------------------|
| Qt1.1 | The creation of a 2D top-down, noise map. | As my client wants smooth and natural-looking top-down terrain (Q1 of 1.3), I have chosen to use a noise algorithm for the base terrain of my game (see 1.4.1 for more). A 2D noise map is the first step of this process. | Screenshot below + throughout both testing videos. | Passed – no next actions required. |
| Qt1.2 | The translation of each point in the lattice to a type of base terrain (i.e. water, sand, land, mountains), based on its height value. | For the noise map to mean anything in terms of gameplay, each point in the map must be converted to a type of terrain, based on its height value (see 1.4.1 for more). | Screenshot below + throughout both testing videos. | Passed – no next actions required. |
| Qt1.3 | The splitting of the map into different biomes, using a different procedural technique, combining each point’s type of terrain with its biome type to specify exactly what terrain it is. | As one of the main objectives of this project is the provision of many biomes (Q3 of 1.3), terrain must be different in each biome. For example: land in a desert should be sand, but land in a forest should be grass (see 1.4.1 for more). | Screenshot below + throughout both testing videos. | Passed – no next actions required. |
| Qt1.4 | The ability of the program to only show a certain portion of the map at any one point – the portion that immediately surrounds the user. | The entire map should be large enough so that a user cannot easily traverse all of it (Q1 of 1.3), and not all of this should be shown to the user at once, otherwise the details of the map would be so small, they would be basically invisible (see 2.6.1 for more). | Video 1, T0:25 – T0:50. | Passed – no next actions required. |
| Qt1.5 | The generation of objects on the map (e.g. trees and flowers), that eventually, a user will be able to gather (Qt2.7). | For the world to feel alive as desired by my client (Q3 of 1.3), the world should have objects that a user can go collect and use when they play the game. | Generation in screenshot below + throughout both testing videos. Gathering: video 2, T… | Passed – no next actions required. |
| Qt2.1 | The creation of a user’s sprite, that acts as the user’s character in-game, that can traverse the map (at a slower speed in water), based on user controls. | This is an essential part of the project (Q1, Q3 of 1.3). As only a portion of the map is shown at any one time, this portion should be changed, respective to the user’s movements. When in water, a user should move more slowly as realistically swimming is slower than walking/running. | Video 1, T00:25 – T1:00. | Passed – no next actions required. |
| Qt2.2 | The creation of user value statistics – health and hunger. | For the game to function at the request of my client (Q3 of 1.3) and for immersion, there must be some element of jeopardy, otherwise systems like combat will mean nothing. | Top left corner throughout both testing videos, except the pause/help menu (e.g. video 1, T0:25). | Passed – no next actions required. |
| Qt2.3 | The creation of a death mechanic where a user respawns at the centre of the world (with their health and hunger fully restored), having lost a small percentage of their items, if their health falls to zero. | For health to have any meaning, the player should die when they have no health remaining. My client described exactly how this should work in the follow-up to Q3 of the client interview. | Video 1, T2:50 – T3:08. | Passed – no next actions required. |
| Qt2.4 | The ability of the user to eat/heal. | The user must be able to recover for the game to function over long periods of time, also requested by my client (Q3 of 1.3). | Healing is a continuous process whenever the user hunger is greater than 50, so this can be seen throughout both videos during when the game is not paused. Replenishing hunger is shown in video 2, T2:56 – T3:00 & T5:30 – T5:38. | Passed – no next actions required. |
| Qt2.5 | The creation of a user inventory, to store items. | For the user to be able to gather and then use items (Q3 of 1.3), the user must be able to store their items in an inventory of some sort. | Throughout both videos, the user inventory hotbar is always displayed centrally at the bottom of the window, when the game is not paused. Both videos show many examples of items being successfully added to the user inventory (e.g. video 1, T1:08 – T1:14). | Passed – no next actions required. |
| Qt2.6 | The creation of a user toolbar, to store tools, which can be upgraded with the appropriate items. | For the user to be able to craft and then use tools (Q3 of 1.3), the user must be able to store their tools in a toolbar of some sort. To add an element of progression in-game, these tools should be upgradable such that they do their purpose more efficiently. | Just like the user inventory hotbar, the toolbar hotbar is shown in the same way except that it is located centrally at the top of the window. Upgrading tools is shown with bugs in video 1, T5:05 – T5:09), without bugs in video 2, T0:50 – T1:27. Video 3 (see below) also confirms that the bugs have been resolved. | **Failed – two bugs were found in testing.** The first issue was that when a user’s iron or diamond levels fell to zero, the user’s hotbar displayed a count of 0 instead of removing the item (video 1, T5:05 – T5:08). The second issue was that when a user had zero iron/diamond and tried to upgrade a tool of that material, the upgrade_tool() subroutine was attempting to fetch the user’s count of this material before testing to see if the material existed in the user inventory in the first place, causing a key error. Resultantly, both these issues have been resolved, see screenshots below. |
| Qt2.7 | The ability of the user to obtain a relatively small selection of items from the map. | The user should be able to gather items from the map (FU to Q3 or 1.3). N.B. there should not be so many items that the game becomes bloated, like Terraria (1.2.1). | Video 2, T1:32 – T2:25 (note that both the shovel and pickaxe are diamond, so gather terrain at the fastest rate). | Passed – no next actions required. |
| Qt3.1 | The creation and rendering of mob objects in the world (unmoving at first), using OOP. | As requested by my client (Q3 of 1.3), there should be plenty of biome-specific mobs that help keep the world alive and fresh. OOP has been chosen as an easy technique to repeatedly generate mobs in the world that share very similar attributes (see 1.1.1 for more). | Video 1, T0:20 – T0:25. | Passed – no next actions required. |
| Qt3.2 | The automatic generation of mobs, at random intervals and random locations, close to the user’s sprite. | So that mobs populate the world, they must periodically generate, near to the user’s sprite so that the user can interact with them (Q3 of 1.3). | Video 1, T0:20 – T0:25. | Passed – no next actions required. |
| Qt3.3 | The implementation of pathfinding algorithms for each type of mob (i.e. passive: random grazing, aggressive: towards the player). | As discussed by my client (Q3 of 1.3), mobs should move around the world, making it feel alive. Specifically, only aggressive mobs should actively move towards the player, ‘attacking’ the user. | Video 1, T0:22 – T0:26, T2:40 – T2:50. Furthermore, as this a complex algorithm, to make sure that the A* pathfinding is properly working, I have conducted modularised tests below (which are passed). | Passed – no next actions required. |
| Qt3.4 | The implementation of collision detection algorithms, so that an aggressive mob can reduce a user’s health when it touches the user’s sprite. Mobs should also not collide with each other or with terrain objects. | For aggressive mobs to be able to fight the user, they damage a user when too close, threatening death for the user (Q3 of 1.3). This system is simple but should be effective and cohesive, as requested (Q2 of 1.3). | Harming user: video 1, T2:48 – T3:00. Avoiding mobs colliding with each other: video 1, T2:50 – T:3:00 (the two zombies to the furthest left). Avoiding terrain objects: video 2, T0:15 – T0:42. | Passed – no next actions required. |
| Qt3.5 | The implementation of an algorithm that allows the user to harm mobs, and eventually kill them, potentially causing it to drop item(s). | Users themselves must be able to fight mobs (Q3 of 1.3) and should be rewarded for victory over certain mobs (passive or aggressive). | Video 1, T3:40 – T4:25. | Passed – no next actions required. |
| Qt4.1 | The implementation of a pause button and pause menu in-game, that allows a user to quit their world or get help. | The user must be able to pause the game when necessary, and should be able to quit the game, or get help if they are struggling (Q2 of 1.3). | Video 2, T5:43 – T6:04. | Passed – no next actions required. |
| Qt4.2 | The displaying of help messages when the user attempts an invalid action. | These types of help messages are necessary to make the game easier to understand and less opaque in its design (Q2 of 1.3). | Video 2, T1:10 – T1:25 (tool messages), T1:38 – T2:25 (terrain gathering messages), T5:30 – T5:38 (eating messages). | Passed – no next actions required. |


