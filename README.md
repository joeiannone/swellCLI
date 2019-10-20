# swellCLI :ocean::surfer:

## A command line interface for checking the surf!

### Requires:
- python 3.0+

### Setup:
(_***virtualenv*** is recommended_)
```
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```
### Run with:
```
$ python main.py [args]
```

### COMMANDS:
-  **[no argument]**        -- Prompts user to select a location and by default will display the current conditions (unless other flags are specified).
-  **[nickname]**           -- Will display either the current conditions, forecast, or both (depending on specified flags) for the given nickname.
-  **spots**                -- Displays users saved spots by nickname.
-  **add**                  -- Prompts user to add/save a new spot to user data store.
-  **remove [nickname]**    -- Removes saved spot from user data store if it is a valid nickname or spot index.
-  **reset**                -- Resets user data store to original state.

### FLAGS:
-  **-c**                    -- Current conditions
-  **-f**                    -- Forecast
-  **-h**, **--help**        -- Displays manual

\*\ _'-h' and '--help' are only interpreted if used exclusively._
\*\ _Other flags can be used in combination i.e. -fc, -cf._


### Data:
- Scraped from swellinfo.com

### Screenshots:
![screenshot](img/screenshot2.png)

![screenshot](img/screenshot1.png)

![screenshot](img/screenshot3.png)
