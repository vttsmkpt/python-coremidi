# Python Core MIDI

Core MIDI Framework C API wrapper for Python built on [ctypes](https://docs.python.org/3/library/ctypes.html).

## Setup

Simply copy the source files to your directory and import it.

## Usage Example

```python
from AudioToolbox import *
from CoreMIDI import *


# ========== DLS AU GRAPH ==========

graph = AUGraph()
NewAUGraph(byref(graph))

cd = AudioComponentDescription()
cd.componentManufacturer = kAudioUnitManufacturer_Apple
cd.componentType = kAudioUnitType_MusicDevice
cd.componentSubType = kAudioUnitSubType_DLSSynth
cd.componentFlags = 0
cd.componentFlagsMask = 0
synthNode = AUNode()
AUGraphAddNode(graph, byref(cd), byref(synthNode))

cd.componentType = kAudioUnitType_Effect
cd.componentSubType = kAudioUnitSubType_PeakLimiter
limiterNode = AUNode()
AUGraphAddNode(graph, byref(cd), byref(limiterNode))

cd.componentType = kAudioUnitType_Output
cd.componentSubType = kAudioUnitSubType_DefaultOutput
outNode = AUNode()
AUGraphAddNode(graph, byref(cd), byref(outNode))

AUGraphOpen(graph)
AUGraphConnectNodeInput(graph, synthNode, 0, limiterNode, 0)
AUGraphConnectNodeInput(graph, limiterNode, 0, outNode, 0)

outSynth = AudioUnit()
description = AudioComponentDescription()
AUGraphNodeInfo(graph, synthNode, byref(description), byref(outSynth))

AUGraphInitialize(graph)
AUGraphStart(graph)
CAShow(graph)

volume = AudioUnitParameterValue(10)
AudioUnitSetParameter(outSynth, kMusicDeviceParam_Volume, kAudioUnitScope_Global, 0, volume, 0)


# ========== CORE MIDI ==========

delegate = None

# typedef void (*MIDIReadProc)(const MIDIPacketList *pktlist, void *readProcRefCon, void *srcConnRefCon);
def readProc(pktlist, readProcRefCon, srcConnRefCon):
	packet  = pktlist.contents.packet[0]
	status = packet.data[0]
	data1 = packet.data[1]
	data2 = packet.data[2]
	if delegate: delegate(status, data1, data2)

callback = CFUNCTYPE(None, POINTER(MIDIPacketList), c_void_p, c_void_p)(readProc)

client = MIDIClientRef()
client_name = CFStringCreateWithCString(None, __file__, kCFStringEncodingUTF8)
MIDIClientCreate(client_name, None, None, byref(client))

input_port = MIDIPortRef()
input_name = CFStringCreateWithCString(None, "I_PORT", kCFStringEncodingUTF8)
MIDIInputPortCreate(client, input_name, callback, None, byref(input_port))

output_port = MIDIPortRef()
output_name = CFStringCreateWithCString(None, "O_PORT", kCFStringEncodingUTF8)
MIDIOutputPortCreate(client, output_name, byref(output_port))

def getSources():
	names = []
	for i in range(MIDIGetNumberOfSources()):
		src = MIDIGetSource(i)
		names.append(getMIDIDisplayName(src))
	return names

def getDestinations():
	names = []
	for i in range(MIDIGetNumberOfDestinations()):
		des = MIDIGetDestination(i)
		names.append(getMIDIDisplayName(des))
	return names

def getMIDIDisplayName(endpoint):
	cf_string = CFStringCreateWithCString(None, c_char_p(b""), kCFStringEncodingUTF8)
	cf_name_key = CFStringCreateWithCString(None, kMIDIPropertyDisplayName, kCFStringEncodingUTF8)
	MIDIObjectGetStringProperty(endpoint, cf_name_key, byref(cf_string))
	c_string_buffer = ctypes.create_string_buffer(64)
	CFStringGetCString(cf_string, c_string_buffer, 64, kCFStringEncodingUTF8)
	py_string = c_string_buffer.value.decode("utf-8")
	if py_string != "" : return py_string
	else: return "< Unknown Endpoint >"

current_src = None
current_dest = None

def setInput(index):
	global current_src
	if current_src:
		MIDIPortDisconnectSource(input_port, current_src, None)
	if index > 0:
		current_src = MIDIGetSource(index-1)
		MIDIPortConnectSource(input_port, current_src, None)

def setOutput(index):
	global current_dest
	if current_dest:
		current_dest = None
	if index > 0:
		current_dest = MIDIGetDestination(index-1)	

def sendEvent(status, data1, data2):
	if current_dest:
		packet = MIDIPacket(
			timeStamp=0,
			length=3,
			data=(Byte*256)(status, data1, data2)
			)
		pktlist = MIDIPacketList(
			numPackets=1,
			packet=(MIDIPacket*1)(packet)
			)
		MIDISend(output_port, current_dest, pktlist)
	else:
		MusicDeviceMIDIEvent(outSynth, status, data1, data2, 0)

def softsynth_program_change(number):
	MusicDeviceMIDIEvent(outSynth, 0xC0, number, 0, 0)

```