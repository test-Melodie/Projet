# -*- coding: utf-8 -*-
#                           ██╗██████╗ ██╗           
#                           ██║╚════██╗██║           
#                           ██║ █████╔╝██║           
#                      ██   ██║██╔═══╝ ██║           
#                      ╚█████╔╝███████╗███████╗      
#                       ╚════╝ ╚══════╝╚══════╝      
#                       https://jusdeliens.com
#
# Designed with 💖 by Jusdeliens
# Under CC BY-NC-ND 3.0 licence 
# https://creativecommons.org/licenses/by-nc-nd/3.0/ 

# Allow import without error 
# "relative import with no known parent package"
# In vscode, add .env file with PYTHONPATH="..." 
# with the same dir to allow intellisense
import sys
import os
__workdir__ = os.path.dirname(os.path.abspath(__file__))
__libdir__ = os.path.dirname(__workdir__)
sys.path.append(__libdir__)

os.system("export LANG=en_US.UTF-8")
#os.system("pip install paho-mqtt")
#os.system("pip install pillow")

import random
import uuid
import time
import traceback
import threading
import io
import json
from paho.mqtt.client import Client
from datetime import datetime
from PIL import Image
from typing import Any, Callable

import pymusx.converter as msx
import pychromatx.converter as cmx
import pyanalytx.logger as anx

class RobotEvent:
	robotConnected = "robotConnected"
	robotDisconnected = "robotDisconnected"
	arenaConnected = "arenaConnected"
	arenaDisconnected = "arenaDisconnected"
	updated = "updated"
	robotChanged = "robotChanged"
	playerChanged = "playerChanged"
	arenaChanged = "arenaChanged"
	imageReceived = "imageReceived"

class IRobot:
	def addEventListener(self,eventName:str, callback:Callable[[Any,str,Any], None]) -> None:
		"""
		Subscribe to event to call the specified callback
		as soon as a event occurs
		"""
		...
	def changeRobot(self, robotId:str, autoconnect:bool):
		"""
		Connect to a new robot id.
		"""
		...
	def connect(self) -> bool :
		"""
		Connect the client to the broker.
		Should be called once just after the __init__
		"""
		...
	def disconnect(self) -> None :
		"""
		Disconnect the client from the broker.
		"""
		...
	def isConnectedToRobot(self) -> bool :
		"""
		Returns whether the client is connected to the robot or not.
		"""
		...
	def isConnectedToArena(self) -> bool :
		"""
		Returns whether the client is connected to the arena or not.
		"""
		...
	def update(self) -> None :
		"""
		Fetch the last values of robot sensors from server
		And send buffered requests in one shot to limit bandwidth.
		To be call in the main loop at least every 10 msecs.
		"""
		...
	def request(self, key:str, value:Any) -> None:
		"""
		Send a request to arena (when useProxy is True) 
		or to robot (if useProxy is False)
		"""
		...
	def getRobotId(self) -> str :
		"""
		Returns the unique id of the robot
		"""
		...
	def getBatteryVoltage(self) -> int :
		"""
		Returns the battery voltage in mV.
		"""
		...
	def getFrontLuminosity(self) -> int :
		"""
		Returns the front sensor luminosity from 0 (dark) to 255 (bright)
		"""
		...
	def getFrontLuminosityLevel(self) -> int :
		"""
		Returns the front sensor luminosity from 0 (dark) to 100 (bright)
		"""
		...
	def getBackLuminosity(self) -> int :
		"""
		Returns the back sensor luminosity from 0 (dark) to 255 (bright)
		"""
		...
	def getBackLuminosityLevel(self) -> int :
		"""
		Returns the back sensor luminosity from 0 (dark) to 100 (bright)
		"""
		...
	def getTimestamp(self) -> int :
		"""
		Returns the last timestamp received from Ova,
		i.e. the time elapsed in milliseconds since the boot of the robot
		"""
		...
	def getImageWidth(self) -> int :
		"""
		Returns the width of the last image captured during the last update
		in pixels. 0 If no image captured.
		"""
		...
	def getImageHeight(self) -> int :
		"""
		Returns the height of the last image captured during the last update
		in pixels. 0 If no image captured.
		"""
		...
	def getImageTimestamp(self) -> int :
		"""
		Returns the time elapsed in milliseconds between 
		the last time an image has been captured from the robot 
		and the creating of the robot class.
		"""
		...
	def getImagePixelRGB(self, x:int, y:int) -> tuple[int,int,int] :
		"""
		Returns the RGB code of the pixel at the specified x,y location.
		Returns (0,0,0) if the specified cordinate is invalid.
		"""
		...
	def getImagePixelLuminosity(self, x:int, y:int) -> int :
		"""
		Returns the luminosity from 0 (dark) to 100 (bright) of the pixel at the specified x,y location.
		Returns 0 if the specified cordinate is invalid.
		"""
		...
	def getRobotState(self) -> dict[str,Any] :
		"""
		Returns the infos of the robot as a dict
		"""
		...
	def getPlayerState(self) -> dict[str,Any] :
		"""
		Returns the infos of the player connected to ova in the arena
		"""
		...
	def getArenaState(self) -> dict[str,Any] :
		"""
		Returns the infos of the arena
		"""
		...
	def setMotorSpeed(self, left:int, right:int, durationInMsecs:int=0) -> None:
		"""
		Changes the speed of the 2 motors on the robot.
		The requested speeds will be send the next update call 

		# Arguments

		* `left` - The speed from -100 (backward) to 100 (forward) on the left wheel
		* `right` - The speed from -100 (backward) to 100 (forward) on the right wheel
		* `durationInMsecs` - The motors will be on during this duration in milliseconds.
		0 means forever. 
		"""
		...
	def setMotorAnimation(self, moves:list[tuple[int,int,int]]) -> None:
		"""
		Changes the speed of the 2 motors on the robot,
		following specified moves during the specified duration for each color.
		The requested animation will be started the next update call 

		# Arguments

		* `moves` - A list motor requests to be played in the same order from index 0,
		to the end of the list, each request as a tuple of 3 integer values
		(speedMotorLeft,speedMotorRight,durationInMsecs). 
		The speed of each motor should be from -100 (backward) to 100 (forward).
		"""
		...
	def setLedColor(self, r:int, g:int, b:int) -> None:
		"""
		Changes the color of the RGB led on the top of the robot
		The requested color will be send the next update call 

		# Arguments

		* `r` - The red from 0 to 255
		* `g` - The green from 0 to 255
		* `b` - The blue from 0 to 255
		"""
		...
	def setLedTwinkle(self, r:int, g:int, b:int, periodInMsecs:int, repeat:int=0):
		"""
		Twinkle the color of the RGB led on the top of the robot.
		The requested rgb animation will be started the next update call, 
		then will stop after 'repeat' time if a >0 value is specified. 

		# Arguments

		* `r` - The red from 0 to 255
		* `g` - The green from 0 to 255
		* `b` - The blue from 0 to 255
		* `periodInMsecs` - The LED will light on during periodInMsecs/2, 
		then light off during periodInMsecs/2
		* `repeat` - The number of time the animation will be repeated. 
		0 means repeat forever
		"""
		...
	def setLedFade(self, r:int, g:int, b:int, periodInMsecs:int, repeat:int=0):
		"""
		Fade in and out the color of the RGB led on the top of the robot.
		The requested rgb animation will be started the next update call, 
		then will stop after 'repeat' time if a >0 value is specified. 

		# Arguments

		* `r` - The red from 0 to 255
		* `g` - The green from 0 to 255
		* `b` - The blue from 0 to 255
		* `periodInMsecs` - The LED will smoothly light on during periodInMsecs/2, 
		then smoothly light off during periodInMsecs/2
		* `repeat` - The number of time the animation will be repeated. 
		0 means repeat forever
		"""
		...
	def setLedHue(self, periodInMsecs:int, repeat:int=0):
		"""
		Change the color of the RGB led on the top of the robot following hue wheel.
		The requested animation will be started the next update call, 
		then will stop after 'repeat' time if a >0 value is specified. 

		# Arguments

		* `periodInMsecs` - The LED will go from red to green during periodInMsecs/3, 
		to blue during periodInMsecs/3, to red during periodInMsecs/3
		* `repeat` - The number of time the animation will be repeated. 
		0 means repeat forever
		"""
		...
	def setLedAnimation(self, colors:list[tuple[int,int,int,int]], repeat:int=1):
		"""
		Change the colors of the RGB led on the top of the robot, 
		following specified colors during the specified duration for each color.
		The requested animation will be started the next update call, 
		then will stop after 'repeat' time if a >0 value is specified. 

		# Arguments

		* `colors` - A list color to be played in the same order from index 0,
		to the end of the list, each color as a tuple of 4 integer values
		(red,green,blue,durationInMsecs)  
		* `repeat` - The number of time the animation will be repeated. 
		0 means repeat forever
		"""
		...
	def playMelody(self, tones:list[tuple[int or str,int]]) -> None:
		"""
		Plays a melody of tones with the buzzer of the robot.
		The requested melody will be send the next update call 

		# Arguments

		* `tones` - A list of tones to be played in the same order from index 0,
		to the end of the list. Each tone must be a tuple of two parms :
		(ToneHeight, DurationInMilliseconds) 
		ToneHeight can be either
		- a str for an anglosaxon tone (i.e. A4, D#5, Gb7) 
		- a int for a frequency in Hz (i.e. 440) 
		- a int for a tone index (i.e. 0 for A4, 1 for A#4, 2 for B4 ...) 
		Duration should be an int 
		"""
		...
	def requestPlayer(self, key:str, value:Any) -> None :
		"""
		Generic method to request arena to do something on the player
		"""
		...
	def requestArena(self, key:str, value:Any) -> None :
		"""
		Generic method to request arena to do something
		"""
		...
	def _onConnectedToRobot(self) -> None:
		"""
		Called on update() call when the client is connected to the robot
		In order to use this method, follow these steps:
			1. Create your own robot class that inherits from OvaClientMqtt 
			2. Create a __init__ method and calls super().__init__(...) at the end
			2. Rewrite this method to override its behaviour
			3. Instanciate the robot class
			4. Call update() from OvaClientMqtt periodically in the main loop
		"""
		...
	def _onDisconnectedFromRobot(self) -> None:
		"""
		Called on update() call when the client is disconnected from the robot
		In order to use this method, follow these steps:
			1. Create your own robot class that inherits from OvaClientMqtt 
			2. Create a __init__ method and calls super().__init__(...) at the end
			2. Rewrite this method to override its behaviour
			3. Instanciate the robot class
			4. Call update() from OvaClientMqtt periodically in the main loop
		"""
		...
	def _onConnectedToArena(self):
		"""Called after the client is connected to the arena"""
		...
	def _onDisconnectedFromArena(self):
		"""Called after the client is disconnected from the arena"""
		...
	def _onUpdated(self) -> None:
		"""
		Called each time update() function is called"
		In order to use this method, follow these steps:
			1. Create your own robot class that inherits from OvaClientMqtt 
			2. Create a __init__ method and calls super().__init__(...) at the end
			2. Rewrite this method to override its behaviour
			3. Instanciate the robot class
			4. Call update() from OvaClientMqtt periodically in the main loop
		"""
		...
	def _onRobotChanged(self, robotState:dict[str,Any]) -> None:
		"""
		Called on update() call each time new state is received from the robot
		In order to use this method, follow these steps:
			1. Create your own robot class that inherits from OvaClientMqtt 
			2. Create a __init__ method and calls super().__init__(...) at the end
			2. Rewrite this method to override its behaviour
			3. Instanciate the robot class
			4. Call update() from OvaClientMqtt periodically in the main loop
			
		# Arguments

		* `robotState` - The new sensor's states and other attributes of the robot
		as a dict of str key and any typed value
		"""
		...
	def _onPlayerChanged(self, playerState:dict[str,Any]) -> None:
		"""
		Called on update() call each time new state is received from the player 
		in the game.
		In order to use this method, follow these steps:
			1. Create your own robot class that inherits from OvaClientMqtt 
			2. Create a __init__ method and calls super().__init__(...) at the end
			2. Rewrite this method to override its behaviour
			3. Instanciate the robot class
			4. Call update() from OvaClientMqtt periodically in the main loop
			
		# Arguments

		* `playerState` - The new player's states and other attributes of the player
		as a dict of str key and any typed value
		"""
		...
	def _onArenaChanged(self, arenaState:dict[str,Any]) -> None:
		"""
		Called on update() call each time new state is received from the arena game.
		In order to use this method, follow these steps:
			1. Create your own robot class that inherits from OvaClientMqtt 
			2. Create a __init__ method and calls super().__init__(...) at the end
			2. Rewrite this method to override its behaviour
			3. Instanciate the robot class
			4. Call update() from OvaClientMqtt periodically in the main loop
			
		# Arguments

		* `arenaState` - The new arena's states and other attributes of the arena
		as a dict of str key and any typed value
		"""
		...
	def _onImageReceived(self, img:Image) -> None:
		"""
		Called on update() call each time new complete image is received from the robot.
		In order to use this method, follow these steps:
			1. Create your own robot class that inherits from OvaClientMqtt 
			2. Create a __init__ method and calls super().__init__(...) at the end
			2. Rewrite this method to override its behaviour
			3. Instanciate the robot class
			4. Call update() from OvaClientMqtt periodically in the main loop
			
		# Arguments

		* `img` - A pillow Image instance on which you could do various operations. 
		For more info, see https://pillow.readthedocs.io/en/stable/reference/Image.html
		"""
		...

class OvaClientMqtt(IRobot):
	"""
	Concrete class to handle input output operation with
	a Jusdeliens Ova robot connected to a mqtt broker
	"""
	melodySizeLimit = 100 # In tone number
	melodyDurationLimit = 10000 # In msecs
	isConnectedTimeout = 10000 # In msecs
	dtTx = 100 # In msecs
	dtPing = 5000 # In msecs
	dtSleepUpdate = 100 # In msecs
	batteryMax = 3900 # In mV
	batteryMin = 3500 # In mV

	def __onChunkImageReceived(self, data:bytes):
		"""Called when rx payload on image topic"""
		payloadLen = len(data)
		if ( payloadLen < 3 ):
			anx.debug("⚠️ Rx image corrupted. Payload len too small")
			return
		imgLen = int.from_bytes(data[0:4],'big', signed=False)
		chunkOfs = int.from_bytes(data[4:8],'big', signed=False)
		chunkLen = int.from_bytes(data[8:12],'big', signed=False)
		anx.debug("📡 Rx image ["+str(chunkOfs)+":"+str(chunkOfs+chunkLen)+"] / "+str(imgLen))
		chunkImg = data[12:]
		if ( chunkOfs == 0 ):
			self.__bufImgOffset = 0
			self.__bufImgExpectedLength = imgLen
		elif ( imgLen != self.__bufImgExpectedLength or self.__bufImgOffset != chunkOfs ):
			anx.debug("⚠️ Rx image corrupted. Expected "+str(self.__bufImgOffset)+"/"+str(self.__bufImgExpectedLength)+" instead of rx "+str(chunkOfs)+"/"+str(imgLen))
			return
		self.__bufImg.append(chunkImg)
		self.__bufImgOffset += chunkLen
		if ( self.__bufImgOffset == self.__bufImgExpectedLength ):
			with self.__bufImgMutex:
				self.__bufImgComplete = self.__bufImg.copy()
				self.__bufImg = []
				self.__rxFromRobot = True
	def __onSensorsReceived(self, data:bytes):
		"""Called when rx payload on sensors topic"""
		self.__prevRxFromRobot = datetime.now()
		newState = {}
		# Parse json payload
		try:
			payloadLen = len(data)
			if ( payloadLen <= 0 ):
				return
			payloadStr = data.decode()
			newState = json.loads(payloadStr)
			anx.debug("📡 Rx state of "+str(payloadLen)+" byte(s): "+payloadStr)
		except:
			anx.debug("⚠️ Rx state failed to parse json")
		with self.__bufRobotStateMutex:
			self.__bufRobotState = newState
			self.__rxFromRobot = True
	def __onPlayerStateReceived(self, data:bytes):
		"""Called when rx payload on player state topic"""
		self.__prevRxFromArena = datetime.now()
		newState = {}
		# Parse json payload
		try:
			payloadLen = len(data)
			if ( payloadLen <= 0 ):
				return
			payloadStr = data.decode()
			newState = json.loads(payloadStr)
			anx.debug("📡 Rx state of "+str(payloadLen)+" byte(s): "+payloadStr)
		except:
			anx.debug("⚠️ Rx state failed to parse json")
		with self.__bufPlayerStateMutex:
			self.__bufPlayerState = newState
			self.__rxFromPlayer = True
	def __onArenaStateReceived(self, data:bytes):
		"""Called when rx payload on arena state topic"""
		self.__prevRxFromArena = datetime.now()
		newState = {}
		# Parse json payload
		try:
			payloadLen = len(data)
			if ( payloadLen <= 0 ):
				return
			payloadStr = data.decode()
			newState = json.loads(payloadStr)
			anx.debug("📡 Rx state of "+str(payloadLen)+" byte(s): "+payloadStr)
		except:
			anx.debug("⚠️ Rx state failed to parse json")
		with self.__bufArenaStateMutex:
			self.__bufArenaState = newState
			self.__rxFromArena = True
	def __onMessage(client, userdata, message):
		"""Called when rx message from mqtt broker"""
		rxTopic = message.topic
		rxPayload = message.payload
		if ( rxTopic == userdata.__topicImgStream ):
			userdata.__onChunkImageReceived(rxPayload)
		elif ( rxTopic == userdata.__topicRobotState ):
			userdata.__onSensorsReceived(rxPayload)
		elif ( rxTopic == userdata.__topicPlayerState ):
			userdata.__onPlayerStateReceived(rxPayload)
		elif ( rxTopic == userdata.__topicArenaState ):
			userdata.__onArenaStateReceived(rxPayload)
		else:
			anx.debug("📡 Rx "+userdata.__id+" on topic "+rxTopic+": "+str(len(rxPayload))+" byte(s)")
	def __onConnect(client, userdata, flags, rc):
		"""Called after a connection to mqtt broker is requested"""
		if ( rc == 0 ):
			if ( userdata.__isConnectedToBroker == False ):
				userdata.__isConnectedToBroker = True
				anx.info("🟢 Connected "+userdata.__id+" to broker")
				for topic in userdata.__topicsToSubcribe:
					anx.info("⏳ Subscribing "+userdata.__id+" to topic "+topic)
					userdata.__client.subscribe(topic)
				pingRequest = json.dumps({"ping": True})
				topicsToPub = [userdata.__topicPlayerRequest]
				if ( userdata.__useProxy == False ):
					topicsToPub.append(userdata.__topicRobotRequest)
				for topic in topicsToPub:
					anx.debug("📡 Tx "+str(userdata.__id)+" to topic "+str(topic)+": "+str(len(pingRequest))+" byte(s)")
					userdata.__client.publish(topic, pingRequest)
		else:
			anx.error("❌ FAIL to connected "+userdata.__id+" to broker")
	def __onDisconnect(client, userdata, rc):
		"""Called when disconnected from mqtt broker"""
		anx.info("🔴 Disconnected "+userdata.__id+" from broker")
		userdata.__isConnectedToBroker = False
	def __onSubscribe(client, userdata, mid, granted_qos):
		"""Called after suscribed on mqtt topic"""
		anx.info("🔔 Subscribed "+userdata.__id+" to topic "+str(mid))
	def __onUnsubscribe(client, userdata, mid):
		"""Called after unsuscribed from mqtt topic"""
		anx.info("🔔 Unsubscribed "+userdata.__id+" from topic "+str(mid))	

	def _onConnectedToRobot(self):
		"""Called after the client is connected to the robot"""
		...
	def _onDisconnectedFromRobot(self):
		"""Called after the client is disconnected from the robot"""
		...
	def _onConnectedToArena(self):
		"""Called after the client is connected to the arena"""
		...
	def _onDisconnectedFromArena(self):
		"""Called after the client is disconnected from the arena"""
		...
	def _onUpdated(self):
		"""Called each time update function is called"""
		...
	def _onRobotChanged(self, robot:dict[str,Any]):
		"""Called each time new state is received from the robot"""
		...
	def _onPlayerChanged(self, player:dict[str,Any]):
		"""Called each time new player state is received from the game"""
		...
	def _onArenaChanged(self, arena:dict[str,Any]):
		"""Called each time new player state is received from the game"""
		...
	def _onImageReceived(self, img:Image):
		"""Called each time new complete image is received from the robot"""
		...

	def __init__(self,robotId:str or None=None, arena:str or None=None, username:str or None=None, password:str or None=None, server:str or None=None, port:int=1883, imgOutputPath:str or None="img.jpeg", autoconnect:bool=True, useProxy:bool=True, verbosity:int=3, clientId:str or None=None, welcomePrint=True):
		"""
		Build a mqtt client to communicate with an ova robot through a mqtt broker

		# Arguments

		* `robotId` - The unique name of the robot to control (e.g. ovaxxxxxxxxxxxx) as str
		* `clientId` - The name of the ovamqttclient used for logging in the broker. Leave None will use a random one
		* `arena` - The name of the arena to join as str
		* `username` - The username to join the server as str
		* `password` - The password to join the server as str
		* `server` - The ip address of the server (e.g. 192.168.x.x) or a domain name (e.g. mqtt.jusdeliens.com) as str
		* `port` - The port of the server (e.g. 1883) as an int
		* `autoconnect` - If True, connect to the broker during init. If False, you should call update or connect yourself after init.
		* `useProxy` - If False, send request directly to robot through broker only. If true, sending to server proxy, which then redirect to robot.
		* `verbosity` - The level of logs as an int. See Verbosity class for more info.
		"""
		anx.setVerbosity(verbosity)
		if ( welcomePrint ):
			print("Hi there 👋")
			print("Turn on your Ova to make it sing like a diva 🎤")
			print("Then wait until your hear the congrat jingle 🎵")
			print("You don't have a robot ? Follow the link 👉 https://jusdeliens.com/ova")
		if ( arena == None or username == None or password == None or server == None):
			print("Enter your credentials to connect to your robot")
		while ( robotId == None or len(robotId) > 32 or len(robotId) == 0 ):
			robotId=input("🤖 robot id (< 32 characters): ")
		while ( server == None or len(server) == 0 ):
			server=input("🌐 server address: ")
			port=int(input("🌐 server port: "))
		if ( arena == None ):
			arena=input("🎲 arena: ")
		if ( username == None ):
			username=input("🧑 username: ")
		if ( password == None ):
			password=input("🔑 password: ")
		self.__startTime = datetime.now()
		
		userLogin=""
		try: userLogin=str(os.getlogin()) 
		except: ...
		macAddr=""
		try: macAddr=str(hex(uuid.getnode())) 
		except: ...

		if ( clientId == None ):
			clientId = "OvaClientMqtt-"+robotId+"-"+userLogin+"-"+macAddr+"-"+str(random.randint(0,99999))

		self.__id : str = clientId
		self.__arena : str = arena 
		self.__idRobot : str = robotId 
		self.__isConnectedToRobot : bool = False
		self.__isConnectedToArena : bool = False
		self.__reqRobot = {}
		self.__reqArena = {}
		self.__reqPlayer = {}
		self.__camImgOutputPath = imgOutputPath
		self.__camImg = None
		self.__bufImgComplete = []
		self.__bufImgMutex = threading.Lock()
		self.__bufImg = []
		self.__bufImgOffset = 0
		self.__bufImgExpectedLength = 0
		self.__bufRobotStateMutex = threading.Lock()
		self.__bufRobotState = {}
		self.__robotState = {}
		self.__rxFromRobot: bool = False
		self.__bufPlayerStateMutex = threading.Lock()
		self.__bufPlayerState = []
		self.__playerState = {}
		self.__rxFromPlayer: bool = False
		self.__bufArenaStateMutex = threading.Lock()
		self.__bufArenaState = []
		self.__arenaState = {}
		self.__rxFromArena: bool = False
		self.__melodyDuration = 0
		self.__prevImgRx: int = 0
		self.__prevRxFromRobot: int = datetime.fromtimestamp(0)
		self.__prevRxFromArena: int = datetime.fromtimestamp(0)
		self.__prevTx: int = datetime.fromtimestamp(0)
		self.__prevPing: int = datetime.fromtimestamp(0)
		self.__dtTxToWait: int = OvaClientMqtt.dtTx
		self.__useProxy = useProxy
		self.__isConnectedToBroker: bool = False
		self.__serverAddress: str = server
		self.__username: str  or  None = username
		self.__password: str  or  None = password
		self.__serverPort: int = port
		self.__isLoopStarted : bool = False
		self.__onEventCallbacks : dict[str, Callable[[Any,str,Any], None] or None] = {}
		for eventName in RobotEvent.__dict__.values():
			self.__onEventCallbacks[eventName] = None
		self.__topicImgStream : str = ""
		self.__topicRobotState : str = ""
		self.__topicPlayerState : str = ""
		self.__topicArenaState : str = ""
		self.__topicArenaRequest : str = ""
		self.__topicPlayerRequest : str = ""
		self.__topicRobotRequest : str = ""
		self.__topicsToSubcribe = []
		self.__client: Client or None = None
		self.__useClientThreadLoop:bool = True
		self.__clientThreadLoop:threading.Thread or None = None
		self.changeRobot(robotId, autoconnect)

	def __clientLoop(self):
		anx.info("🟢 Started mqtt loop")
		self.__isLoopStarted = True
		try:
			while ( self.__isLoopStarted ):
				self.__client.loop()
				time.sleep(0.1)
		except:
			anx.error("⚠️💔 CRITICAL ERROR in mqtt loop")
		anx.info("🔴 Stopped mqtt thread loop")
		self.__isLoopStarted = False

	def changeRobot(self, robotId, autoconnect):
		anx.info("⏳ Connecting to robot "+str(robotId)+" ...")
		self.disconnect()
		self.__idRobot : str = robotId 
		self.__prevRxFromRobot: int = datetime.fromtimestamp(0)
		self.__topicImgStream : str  = "optx/clients/stream/"+self.__idRobot
		self.__topicRobotState : str  = "robotx/clients/state/"+self.__idRobot
		self.__topicPlayerState : str  = "ludx/clients/state/"+self.__arena+"/"+self.__id
		self.__topicArenaState : str  = "ludx/server/state/"+self.__arena
		self.__topicArenaRequest : str  = "ludx/server/request/"+self.__arena
		self.__topicPlayerRequest : str  = "ludx/clients/request/"+self.__arena+"/"+self.__id
		self.__topicRobotRequest : str  = "robotx/clients/request/"+self.__idRobot
		self.__topicsToSubcribe = [self.__topicImgStream, self.__topicRobotState, self.__topicPlayerState, self.__topicArenaState]
		self.__client: Client = Client(self.__id, userdata=self)
		self.__client.on_message = OvaClientMqtt.__onMessage
		self.__client.on_connect = OvaClientMqtt.__onConnect
		self.__client.on_disconnect = OvaClientMqtt.__onDisconnect
		self.__client.on_subscribe = OvaClientMqtt.__onSubscribe
		self.__client.on_unsubscribe = OvaClientMqtt.__onUnsubscribe
		if ( autoconnect ):
			self.connect()

	def addEventListener(self,eventName:str, callback:Callable[[Any,str,Any], None]) -> None:
		if ( eventName not in self.__onEventCallbacks ):
			anx.warning("⚠️ Cannot add event listener for event "+eventName)
			anx.warning("⚠️ Can only add event on "+str(self.__onEventCallbacks.keys()))
			return
		self.__onEventCallbacks[eventName] = callback

	def connect(self) -> bool :
		if self.__isLoopStarted and self.__isConnectedToBroker:
			return False
		if (self.__username is not None and self.__password is not None):
			self.__client.username_pw_set(self.__username, self.__password)
		try:
			if ( self.__isConnectedToBroker == False ):
				anx.info("⏳ Connecting "+str(self.__id)+" to broker "+self.__serverAddress+":"+str(self.__serverPort)+" ...")
				self.__client._connect_timeout = 5.0
				rc=self.__client.connect(self.__serverAddress, self.__serverPort)
				#OvaClientMqtt.__onConnect(self.__client, self, None, rc) # TODO to remove if using loopstart loopstop
			if ( self.__isLoopStarted == False ):
				anx.info("⏳ Starting mqtt thread loop ...")
				if ( self.__useClientThreadLoop ):
					self.__client.loop_start()
					anx.info("🟢 Started mqtt loop")
					self.__isLoopStarted = True
				else:
					self.__clientThreadLoop = threading.Thread(target=self.__clientLoop)
					self.__clientThreadLoop.start()
			time.sleep(2)
			return rc == 0
		except:
			return False

	def disconnect(self) -> None :
		if self.__isConnectedToBroker:
			anx.info("⏳ Disconnecting "+str(self.__id)+" from broker...")
			self.__client.disconnect()
		if self.__isLoopStarted: 
			anx.info("⏳ Stopping mqtt thread loop ...")
			self.__isLoopStarted = False	
			if ( self.__useClientThreadLoop ):
				self.__client.loop_stop()
				anx.info("🔴 Stopped mqtt thread loop")
			else:
				self.__clientThreadLoop.join()

	def isConnectedToArena(self) -> bool:
		dtRx = (datetime.now() - self.__prevRxFromArena).total_seconds() * 1000
		return self.__isConnectedToBroker and dtRx < OvaClientMqtt.isConnectedTimeout

	def isConnectedToRobot(self) -> bool:
		dtRx = (datetime.now() - self.__prevRxFromRobot).total_seconds() * 1000
		return self.__isConnectedToBroker and dtRx < OvaClientMqtt.isConnectedTimeout

	def update(self, enableSleep=True) -> None:
		if ( self.__isConnectedToBroker == False ):
			self.connect()

		try:
			self._onUpdated()
			if ( self.__onEventCallbacks[RobotEvent.updated] != None ):
				self.__onEventCallbacks[RobotEvent.updated](self, RobotEvent.updated, None)
		except Exception as e:
			anx.error("⚠️ Exception during _onUpdated call : "+str(e))
			anx.error(traceback.format_exc())
		
		# Rx states and stream
		if ( self.__rxFromRobot ):
			self.__rxFromRobot = False
			# Triggers on connected event
			if ( self.__isConnectedToRobot == False ):
				self.__isConnectedToRobot = True
				anx.info("🟢 Robot "+str(self.__idRobot)+" connected")
				try:
					self._onConnectedToRobot()
					if ( self.__onEventCallbacks[RobotEvent.robotConnected] != None ):
						self.__onEventCallbacks[RobotEvent.robotConnected](self, RobotEvent.robotConnected, None)
				except Exception as e:
					anx.error("⚠️ Exception during _onConnectedToRobot call : "+str(e))
					anx.error(traceback.format_exc())
			# Swap bug img and sensor states 
			try:
				with self.__bufImgMutex:
					if ( len(self.__bufImgComplete) > 0 ):
						self.__camImg = Image.open(io.BytesIO(b''.join(self.__bufImgComplete)))
						self.__bufImgComplete = []
						self.__prevImgRx = (datetime.now() - self.__startTime).total_seconds() * 1000
						if ( self.__camImgOutputPath != None ):
							try:
								self.__camImg.save(self.__camImgOutputPath)
								anx.debug("📸 Save camera image in "+str(os.getcwd())+"\\"+str(self.__camImgOutputPath))
							except:
								anx.debug("⚠️ Fail to write "+str(self.__camImgOutputPath))
						anx.debug("🖼️ Camera img received: "+str(self.__camImg.width)+"x"+str(self.__camImg.height))
						try:
							self._onImageReceived(self.__camImg)
							if ( self.__onEventCallbacks[RobotEvent.imageReceived] != None ):
								self.__onEventCallbacks[RobotEvent.imageReceived](self, RobotEvent.imageReceived, self.__camImg)
						except Exception as e:
							anx.debug("⚠️ Exception during _onImageReceived call : "+str(e))
							anx.debug(traceback.format_exc())
			except:
				anx.debug("⚠️ Rx image corrupted. Fail to swap buffer.")

			try:
				with self.__bufRobotStateMutex:
					if ( self.__bufRobotState != self.__robotState ):
						anx.debug("🤖 Robot changed: "+str(self.__bufRobotState))
						for key,value in self.__bufRobotState.items():
							self.__robotState[key] = value
						self.__bufRobotState = {}
						try:
							self._onRobotChanged(self.__robotState)
							if ( self.__onEventCallbacks[RobotEvent.robotChanged] != None ):
								self.__onEventCallbacks[RobotEvent.robotChanged](self, RobotEvent.robotChanged, self.__robotState)
						except Exception as e:
							anx.debug("⚠️ Exception during _onRobotChanged call : "+str(e))
							anx.debug(traceback.format_exc())
			except:
				anx.debug("⚠️ Rx robot state corrupted. Fail to swap buffer.")
		elif ( self.__isConnectedToRobot == True and self.isConnectedToRobot() == False ):
			self.__isConnectedToRobot = False
			anx.info("🔴 Robot "+str(self.__idRobot)+" disconnected")
			try:
				self._onDisconnectedFromRobot()
				if ( self.__onEventCallbacks[RobotEvent.robotDisconnected] != None ):
					self.__onEventCallbacks[RobotEvent.robotDisconnected](self, RobotEvent.robotDisconnected, None)
			except Exception as e:
				anx.error("⚠️ Exception during _onDisconnectedFromRobot call : "+str(e))
				anx.error(traceback.format_exc())
		if ( self.__rxFromPlayer ):
			self.__rxFromPlayer = False
			try:
				with self.__bufPlayerStateMutex:
					if ( self.__bufPlayerState != self.__playerState ):
						anx.debug("♟️ Player changed: "+str(self.__bufPlayerState))
						for key,value in self.__bufPlayerState.items():
							self.__playerState[key] = value
						self.__bufPlayerState = {}
						try:
							self._onPlayerChanged(self.__playerState)
							if ( self.__onEventCallbacks[RobotEvent.playerChanged] != None ):
								self.__onEventCallbacks[RobotEvent.playerChanged](self, RobotEvent.playerChanged, self.__playerState)
						except Exception as e:
							anx.error("⚠️ Exception during _onPlayerChanged call : "+str(e))
							anx.error(traceback.format_exc())
			except:
				anx.debug("⚠️ Rx player state corrupted. Fail to swap buffer.")
		if ( self.__rxFromArena ):
			self.__rxFromArena = False
			# Triggers on connected event
			if ( self.__isConnectedToArena == False ):
				self.__isConnectedToArena = True
				anx.info("🟢 Arena "+str(self.__arena)+" connected")
				try:
					self._onConnectedToArena()
					if ( self.__onEventCallbacks[RobotEvent.arenaConnected] != None ):
						self.__onEventCallbacks[RobotEvent.arenaConnected](self, RobotEvent.arenaConnected, None)
				except Exception as e:
					anx.error("⚠️ Exception during _onConnectedToArena call : "+str(e))
					anx.error(traceback.format_exc())
			try:
				with self.__bufArenaStateMutex:
					if ( self.__bufArenaState != self.__arenaState ):
						anx.debug("🎲 Arena changed: "+str(self.__bufArenaState))
						for key,value in self.__bufArenaState.items():
							self.__arenaState[key] = value
						self.__bufArenaState = {}
						try:
							self._onArenaChanged(self.__arenaState)
							if ( self.__onEventCallbacks[RobotEvent.arenaChanged] != None ):
								self.__onEventCallbacks[RobotEvent.arenaChanged](self, RobotEvent.arenaChanged, self.__arenaState)
						except Exception as e:
							anx.error("⚠️ Exception during _onArenaChanged call : "+str(e))
							anx.error(traceback.format_exc())
			except:
				anx.debug("⚠️ Rx player state corrupted. Fail to swap buffer.")
		elif ( self.__isConnectedToArena == True and self.isConnectedToArena() == False ):
			self.__isConnectedToArena = False
			anx.info("🔴 Arena "+str(self.__arena)+" disconnected")
			try:
				self._onDisconnectedFromArena()
				if ( self.__onEventCallbacks[RobotEvent.arenaDisconnected] != None ):
					self.__onEventCallbacks[RobotEvent.arenaDisconnected](self, RobotEvent.arenaDisconnected, None)
			except Exception as e:
				anx.error("⚠️ Exception during _onDisconnectedFromArena call : "+str(e))
				anx.error(traceback.format_exc())

		# Tx requests
		dtTx = (datetime.now()-self.__prevTx).total_seconds() * 1000
		if ( dtTx > self.__dtTxToWait ):
			self.__prevTx = datetime.now()
			robotReqTopicsToPub = [self.__topicPlayerRequest]
			if ( self.__useProxy == False ):
				robotReqTopicsToPub.append(self.__topicRobotRequest)
			reqsToTx = [
				(self.__reqRobot, robotReqTopicsToPub),
				(self.__reqPlayer, [self.__topicPlayerRequest]),
				(self.__reqArena, [self.__topicArenaRequest])
			]
			for req in reqsToTx:
				request, topicsToPub = req
				if ( len(request) == 0 ):
					continue
				payloadStr = json.dumps(request)
				payloadBytes = str.encode(payloadStr)
				for topic in topicsToPub:
					anx.debug("📡 Tx "+str(self.__id)+" to topic "+str(topic)+": "+str(len(payloadBytes))+" byte(s)")
					self.__client.publish(topic, payloadBytes)

			self.__reqArena = {}
			self.__reqPlayer = {}
			self.__reqRobot = {}
			if ( self.__melodyDuration > 0 ):
				self.__dtTxToWait = self.__melodyDuration
				time.sleep(self.__melodyDuration/1000.0)
				self.__melodyDuration = 0
			else:
				self.__dtTxToWait = OvaClientMqtt.dtTx

		# Ping server
		dtPing = (datetime.now()-self.__prevPing).total_seconds() * 1000
		if ( dtPing > OvaClientMqtt.dtPing ):
			self.__prevPing = datetime.now()
			payloadStr = json.dumps({"ping":True})
			payloadBytes = str.encode(payloadStr)
			topicsToPub = [self.__topicPlayerRequest]
			for topic in topicsToPub:
				anx.debug("📡 Ping "+str(self.__id))
				self.__client.publish(topic, payloadBytes)

		if (enableSleep):
			time.sleep(OvaClientMqtt.dtSleepUpdate/1000)

	def requestPlayer(self, key, value) -> None :
		self.__reqPlayer[key] = value

	def requestArena(self, key, value) -> None :
		self.__reqArena[key] = value

	def getRobotId(self) -> str :
		return self.__idRobot

	def getBatteryVoltage(self) -> int :
		if ( "battery" not in self.__robotState or "voltage" not in self.__robotState["battery"] ):
			return 0
		return self.__robotState["battery"]["voltage"]
	
	def getBatteryLevel(self) -> int :
		voltage = self.getBatteryVoltage()
		if ( voltage > OvaClientMqtt.batteryMax ): return 100
		elif ( voltage < OvaClientMqtt.batteryMin ): return 0
		else:
			return int(100*(voltage-OvaClientMqtt.batteryMin) / (OvaClientMqtt.batteryMax-OvaClientMqtt.batteryMin))

	def getFrontLuminosity(self) -> int :
		if ( "photoFront" not in self.__robotState or "lum" not in self.__robotState["photoFront"] ):
			return 0
		return self.__robotState["photoFront"]["lum"]
	
	def getFrontLuminosityLevel(self) -> int :
		return int(100*self.getFrontLuminosity()/255)

	def getBackLuminosity(self) -> int :
		if ( "photoBack" not in self.__robotState or "lum" not in self.__robotState["photoBack"] ):
			return 0
		return self.__robotState["photoBack"]["lum"]

	def getBackLuminosityLevel(self) -> int :
		return int(100*self.getBackLuminosity()/255)

	def getTimestamp(self) -> int :
		if ( "t" not in self.__robotState ):
			return (self.__prevRxFromArena-self.__startTime).total_seconds() * 1000
		return self.__robotState["t"]

	def getImageWidth(self) -> int :
		if ( self.__camImg == None ):
			return 0
		return self.__camImg.width

	def getImageHeight(self) -> int :
		if ( self.__camImg == None ):
			return 0
		return self.__camImg.height

	def getImageTimestamp(self) -> int :
		return self.__prevImgRx

	def getImagePixelRGB(self, x:int,y:int) -> tuple[int,int,int] :
		if ( x < 0 or x >= self.getImageWidth() or y < 0 or y >= self.getImageHeight() ):
			return (0,0,0)
		r,g,b = self.__camImg.getpixel((x, y))
		return (r,g,b)
	def getImagePixelLuminosity(self, x:int,y:int) -> int :
		if ( x < 0 or x >= self.getImageWidth() or y < 0 or y >= self.getImageHeight() ):
			return 0
		r,g,b = self.__camImg.getpixel((x, y))
		h,s,l = cmx.RGBToHSL(r,g,b)
		return l

	def getRobotState(self) -> dict[str,Any] :
		return self.__robotState

	def getPlayerState(self) -> dict[str,Any] :
		return self.__playerState

	def getArenaState(self) -> dict[str,Any] :
		return self.__arenaState

	def setMotorSpeed(self, leftPower:int, rightPower:int, durationInMsecs:int=1000):
		if ( leftPower < -100 or rightPower < -100 or leftPower > 100 or rightPower > 100):
			anx.warning("⚠️ Motor speed should be between -100 and +100!")
			return
		if ( type(durationInMsecs)!=int or durationInMsecs < 0 or durationInMsecs > 10000 ):
			anx.warning("⚠️ Incorrect motor speed duration. Should be a positive integer value in ms lesser than 10000 !")
			return
		self.__reqRobot["motor"] = [[leftPower,rightPower,durationInMsecs]]

	def setMotorAnimation(self, moves:list[tuple[int,int,int]]):
		for move in moves:
			if ( len(move) != 3 ):
				anx.warning("⚠️ Incorrect move in motor animation. Should be a list of tuples of 3 params : speedMotorLeft, speedMotorRight, durationInMs !")
				return
			for i in range(2):
				if ( type(move[i])!=int or move[i] < -100 or move[i] > 100 ):
					anx.warning("⚠️ Incorrect move in motor animation. Move speed should be an integer value between -100 (backward) and 100 (forward) !")
					return
			if ( type(move[2])!=int or move[2] < 0 or move[2] > 10000 ):
				anx.warning("⚠️ Incorrect move in motor animation. Move duration should be a positive integer value in ms lesser than 10000 !")
				return
		self.__reqRobot["motor"] = moves

	def setLedColor(self, r:int, g:int, b:int):
		if ( r < 0 or g < 0 or b < 0 or r > 255 or g > 255 or b > 255 ):
			anx.warning("⚠️ LED RGB should be between 0 and 255!")
			return
		self.__reqRobot["led"] = {
			"animation":"static",
			"rgb":[r,g,b],
			"repeat":0,
			"duration":0
		}

	def setLedTwinkle(self, r:int, g:int, b:int, periodInMsecs:int, repeat:int=0):
		if ( r < 0 or g < 0 or b < 0 or r > 255 or g > 255 or b > 255 ):
			anx.warning("⚠️ LED RGB should be between 0 and 255!")
			return
		if ( periodInMsecs < 0 or periodInMsecs > 65535):
			anx.warning("⚠️ LED twinkle period should be between 0 and 65535 ms!")
			return
		if ( repeat < 0 or repeat > 65535):
			anx.warning("⚠️ LED twinkle repeat should be between 0 (means forever) and 65535 ms!")
			return
		self.__reqRobot["led"] = {
			"animation":"twinkle",
			"rgb":[r,g,b],
			"duration":periodInMsecs, 
			"repeat":repeat
		}
	def setLedFade(self, r:int, g:int, b:int, periodInMsecs:int, repeat:int=0):
		if ( r < 0 or g < 0 or b < 0 or r > 255 or g > 255 or b > 255 ):
			anx.warning("⚠️ LED RGB should be between 0 and 255!")
			return
		if ( periodInMsecs < 0 or periodInMsecs > 65535):
			anx.warning("⚠️ LED fade period should be between 0 and 65535 ms!")
			return
		if ( repeat < 0 or repeat > 65535):
			anx.warning("⚠️ LED fade repeat should be between 0 (means forever) and 65535 ms!")
			return
		self.__reqRobot["led"] = {
			"animation":"fade",
			"rgb":[r,g,b],
			"duration":periodInMsecs, 
			"repeat":repeat
		}
	def setLedHue(self, periodInMsecs:int, repeat:int=0):
		if ( periodInMsecs < 0 or periodInMsecs > 65535):
			anx.warning("⚠️ LED HUE period should be between 0 and 65535 ms!")
			return
		if ( repeat < 0 or repeat > 65535):
			anx.warning("⚠️ LED HUE repeat should be between 0 (means forever) and 65535 ms!")
			return
		self.__reqRobot["led"] = {
			"animation":"hue",
			"duration":periodInMsecs, 
			"repeat":repeat
		}
	def setLedAnimation(self, colors:list[tuple[int,int,int,int]], repeat:int=0):
		if ( repeat < 0 or repeat > 65535):
			anx.warning("⚠️ LED animation repeat should be between 0 (means forever) and 65535 ms!")
			return
		for color in colors:
			if ( len(color) != 4 ):
				anx.warning("⚠️ Incorrect color in led animation. Should be a list of tuples of 4 params : r,g,b, duration !")
				return
			for i in range(3):
				if ( type(color[i])!=int or color[i] < 0 or color[i] > 255 ):
					anx.warning("⚠️ Incorrect color in led animation. Color rgb should be a positive integer value between 0 (dark) and 255 (bright) !")
					return
			if ( type(color[3])!=int or color[3] < 0 or color[3] > 10000 ):
				anx.warning("⚠️ Incorrect color in led animation. Color duration should be a positive integer value in ms lesser than 10000 !")
				return
		self.__reqRobot["led"] = {
			"animation":"custom",
			"repeat":repeat,
			"colors":colors
		}

	def playMelody(self, tones:list[tuple[int or str,int]]):
		if ( len(tones) <= 0 ):
			anx.warning("⚠️ No tone in melody!")
			return
		if ( len(tones) > OvaClientMqtt.melodySizeLimit ):
			anx.warning("⚠️ Too much tones in melody!")
			return
		duration = 0
		tonesHzMs = []
		for tone in tones:
			if ( len(tone) != 2 ):
				anx.warning("⚠️ Incorrect tone in melody. Should be a list of tuples of 2 params : frequency, duration !")
				return
			toneHeight = tone[0]
			toneDuration = tone[1]
			if ( type(toneDuration)!=int or toneDuration < 0 or toneDuration > 10000 ):
				anx.warning("⚠️ Incorrect duration in melody. Should be a positive integer value in ms lesser than 10000 !")
				return
			toneHeight = msx.toneToFreq(toneHeight)
			if ( toneHeight == None ):
				return
			# freq as index
			tonesHzMs.append((toneHeight,toneDuration))
			duration += toneDuration
		if ( duration > OvaClientMqtt.melodyDurationLimit ):
			anx.warning("⚠️ Melody duration is too long!")
			return
		self.__melodyDuration = duration
		self.__reqRobot["buzzer"] = tonesHzMs

	def prompt(self, jsonReq:str) -> bool:
		try:
			self.__reqRobot = json.loads(jsonReq)
			return True
		except:
			return False
			
	def print(self) -> None:
		if self.isConnectedToRobot():
			print("🟢 Robot connected")
		else:
			print("🔴 Robot disconnected")
		if self.isConnectedToArena():
			print("🟢 Arena connected")
		else:
			print("🔴 Arena disconnected")
		print("🎲 Arena state: ", self.getArenaState())
		print("♟️ Player state: ", self.getPlayerState())
		print("🤖 Robot state: ", self.getRobotState())
		print("⬆️ Photo front lum: ", self.getFrontLuminosity())
		print("⬇️ Photo back lum: ", self.getBackLuminosity())
		print("🔋 Battery voltage: ", self.getBatteryVoltage())
		print("⏱️ Timestamp: ", self.getTimestamp(),"ms")
		print("📸 Camera img "+str(self.getImageWidth())+"x"+str(self.getImageWidth())+" shot after "+str(self.getImageTimestamp())+" ms")

class OvaDebugClientMqtt(OvaClientMqtt):
	def __init__(self,id:str or None=None, arena:str or None=None, username:str or None=None, password:str or None=None, server:str or None=None, port:int=1883, imgOutputPath:str or None="img.jpeg", autoconnect:bool=True, useProxy:bool=True, verbosity:int=3):
		super().__init__(id=id, arena=arena, username=username, password=password, server=server, port=port, imgOutputPath=imgOutputPath, autoconnect=autoconnect, useProxy=useProxy, verbosity=verbosity)
	def _onUpdated(self):
		os.system('cls')
		self.print()
		time.sleep(0.1)
		return super()._onUpdated()