# GamersHeaven


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
   - 26 Subtrees (6 is default I believe)
   - Double the hashing bins (512 rather than 256)
   - .5 (1/2) subsample (I don't remember why I do this, there's an optimization reason in the python docs for XGBoost).
   - .36 data weight (my dataset was roughly 36 falses to 100 trues, yours might be different).
- NVIDIA CUDA 10.1 Compatibility *STRONGLY RECOMMENDED*!!! *CODE WILL TAKE DAYS TO RUN IF YOU DON'T HAVE CUDA INSTALLED!!!*
- Python (Go In-Depth of all the dependencies required)


---------------------------------------------
  What Did the Project Conclude?
---------------------------------------------

Under Construction
