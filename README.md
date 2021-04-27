# GamersHeaven
---------------------------------------------
DISCLAIMER
---------------------------------------------

This project is not associated with the mom and pop video game store of a nearly identical name, [Gamer's Heaven](https://www.gamersheaven.life/). The name devised for this project was intended for when this project had a different purpose and is not in any way meant to infringe upon the rights of or divert attention from the Arizona brick and mortar location of that name. I, the project creator, am a firm believer in preservation of older technology and believe that those in the Pheonixville area or browsing online should consider this store as a viable source for obtaining legitimate physical copies of older games and gaming hardware.

It is too late in the project development cycle to change the GitHub repository name for this, because this repository link has been cited in the paper for the presentation and changing it would break the link for the work done.

---------------------------------------------
  What is GamersHeaven?
---------------------------------------------

- GamersHeaven Is a project which aims to Find what drives [Steam](https://store.steampowered.com/) User review sentiment the most.

- The hypothesis is that discounts are a Function of review score. That is, it's believed that discounts are what most closely causes user sentiment.

- Other factors of the reviews themselves are being considered, as well.
    - How interactive the Steam Community is with aforementioned review (Any funny votes on the review in question? Upvotes for the review? Review Comments?)
    - What sort of interaction the reviewer has had with the game (Early Access Review? Any Playtime in the last 2 weeks? Those kinds of things).


---------------------------------------------
  Where was the Data Obtained?
---------------------------------------------

- SteamApps.json was downloaded directly through the web browser [IsThereAnyDeal](https://isthereanydeal.com/) API call and cleaned.
  - Another, Similarly Structured json file called AppIDDB.json was obtained directly through the web browser

- Steam Sales Data was obtained with conditional permission from Tomáš Fedor, the API Key owner and mainainer of [IsThereAnyDeal](https://isthereanydeal.com/).
  - The condition was that data from IsThereAnyDeal.com must *NOT* be shared publicly, and any requests to view this data will be treated with respect for the API owner and Declined.

- Steam Review Data was obtained from an HTTP Get call from SteamWorks's Developer Website. This HTTP Get Call can be found [here](https://partner.steamgames.com/doc/store/getreviews).



---------------------------------------------
  How Was the Project Designed?
---------------------------------------------

- XGBoost - Binary classification problem, either it's a Positive or Negative Review Score.
  - The following parameters were changed to the shown amounts, decrease if you feel they're performance hogs:
  
   - Tree Depth is (6 is default I believe0.) Added since CUDA is supported, decrease if needed.
   
   - Double the hashing bins. (512 rather than 256.) Added since CUDA is supported, decrease if needed.
   
   - Subsample of .5 (1/2)  "Setting this to 0.5 means that XGBoost would randomly sample half of the training data prior to growing trees." - [From the XGBoost Docs for Python](https://xgboost.readthedocs.io/en/latest/parameter.html)
   
   - Data weight of .36  (my dataset was roughly 36 falses to 100 trues, yours might be different so adjust here first.
   
   - Seed of 11 (just a default state I changed to ensure model integrity, probably won't matter much.

   - Train/Test Split size of 70%/30% (.7/.3) (Again, something I did to ensure data integrity. For you it might be different.
   
   - shuffle=true (DEFINITELY. KEEP. THIS. You have no way of 100% guaranteeing that your model will be accurately fit to the data specs that your model expects.
   
   - objective set to binary:logistic. Initially this made my model perform terribly, until I set the scale weight to fit my data weight. I'd recommend keeping this just in case.

   - booster set to GBLinear. Initially this made my model perform terribly, until I set the scale weight to fit my data weight. I'd recommend keeping this just in case.


- NVIDIA CUDA Compatibility *STRONGLY RECOMMENDED*!!! *CODE MAY NUKE YOUR MACHINE BY DEFAULT IF YOU DON'T HAVE CUDA INSTALLED!!!*
  - Tree method set to GPU_Hist and gpu_id=0. This is what enabled GPU support on my machine.
- Anaconda Version Control
  - Visual Studio Code
  - Python (There was a point I was experimenting with [phased-lstm-keras](https://github.com/fferroni/PhasedLSTM-Keras) and [tensorflow-phased-lstm](https://github.com/philipperemy/tensorflow-phased-lstm) for this project so at those points I definitely needed version control, since these repositories are broken under current python libraries.
- WAMP Server (LAMP will also work, but I needed to remote into my machine and Parsec is the only thing I've gotten to go past my router).
  - MySQL Backend
  - Web Hosting (The main reason I went with the W/LAMP stack is because it's a possibility that Mr. Fedor takes over.)
- Parsec (Personal use for remote hosting, you can use whatever you wish here.

  - SIDE NOTE: I ***strongly*** recommended that you use a different remote hosting application and/or Stack to do this kind of thing, despite Parsec's simplicity to play nice with my ISP. If you can at all, go with a Remote Desktop protocol that can traverse your firewall ***securely*** while giving you the option to remote into your PC without an attached monitor. I have unfortunately found no setting or ability which lets Parsec do this, nor does Parsec perform any hosting capability on Linux systems, which is the standard for Server Hosting. If it wasn't for my dang ISP I would definitely have gone for a protocol that works on Linux, and used Linux. But it is what it is, I guess.


---------------------------------------------
  What Did the Project Conclude?
---------------------------------------------

- I concluded that there's two key relations found with this project:
    - As Price metrics go down, Steam review scores go up. and Vice versa. This is the original hypothesis that was intended to be tested for.
    - As Review scores go down, Steam Community Interaction Goes Up and vice versa. This phenominon, for those unfamiliar with internet lingo, is known as a ratio, and typically happens when something has been messed up.
    - How much interaction a reviewer has with the game at the time of the review record has little if any bearing on the review score.
 
 - What do these two facts together mean?
    - If your game is being ratioed and you don't want to give up on developing the game, first of all fix what people are upset about (obviously), but also cut the price of the game to generate positive buzz about the game, and bring in new players over time to generate revenue you would have just completely lost otherwise.


No Man's Sky is an infamous example of this phenominon which shows where this conclusion came from. It was 60$ at launch for a game that was just unfinished and in development hell for the longest time, and there was no way the developers were ready to push the game out. Immediately the game was discounted, and Sony forced the developers to finish the game (since the development team also published the game to PlayStation 4 at the time). Over time, more features were added, and more discounts were announced, and finally not only is it the game it was initially promised to be, it managed to get a bunch of positive reception around it.
