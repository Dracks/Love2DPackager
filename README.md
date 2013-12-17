Love2DPackager
==============

It's a python script to made easy package a love2d game

### Usage ###
This script can package a folder game into a .love file and/or make an autoexecutable file for windows and/or mac os. The three options can be used at same time, or, otherwise, you can only use the options you wish. 

The requirements are:
  * To package a .love file you need a LovePackager.conf file in root folder game with the configuration of files required to run game and the name you wish for your game. 
  * To made a windows autoexecutable, you need the windows love2d framework unzipped 
  * To made a Mac os X Autoexecutable, like windows, you need love2D for mac downloaded and unzipped

```bash
#To package only to a .love file
python start.py -p pathToGame pathToOutput

#To made a windows exacutable with a .love file:
python start.py -l pathToGame.love -w pathToLoveWindows pathToOutput

#To made a mac executable and .love package with the same command
python start.py -p pathToGame -m pathToLoveMac.app pathToOutput
```

##### package .love configuration #####
To package a .love file you need LovePackager.conf in your Love2D game folder that is a JSON to configure what files should be packaged, main.lua and conf.lua should be added automatically, an example of LovePackager.conf
```JSON
{
	"files":[
		"folder", "folder2/subfolder", "Constants.lua"
	],
	"name":"Example"
}
```



