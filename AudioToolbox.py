from ctypes import *
import ctypes.util

from CoreFoundation import *

_at = CDLL(ctypes.util.find_library("AudioToolbox"))

OpaqueAUGraph = c_void_p
AUGraph = POINTER(OpaqueAUGraph)  # typedef struct OpaqueAUGraph *AUGraph;
AUNode = c_int32  # typedef SInt32 AUNode;
AudioComponentInstance = c_void_p  # typedef struct ComponentInstanceRecord *AudioComponentInstance;
AudioUnit = AudioComponentInstance  # typedef AudioComponentInstance AudioUnit;
MusicDeviceComponent = AudioComponentInstance  # typedef AudioComponentInstance MusicDeviceComponent;
AudioUnitParameterID = c_uint32  # typedef UInt32 AudioUnitParameterID;
AudioUnitScope = c_uint32  # typedef UInt32 AudioUnitScope;
AudioUnitElement = c_uint32  # typedef UInt32 AudioUnitElement;
AudioUnitParameterValue = c_float  # typedef Float32 AudioUnitParameterValue;

kMusicDeviceParam_Volume = AudioUnitParameterID(1)
kAudioUnitScope_Global = AudioUnitScope(0)

def FOUR_CHAR_CODE(code):
    value = 0
    for i in range(4):
        value += ord(code[i]) << (3 - i) * 8
    return value

kAudioUnitManufacturer_Apple = FOUR_CHAR_CODE('appl')
kAudioUnitType_MusicDevice = FOUR_CHAR_CODE('aumu')
kAudioUnitSubType_DLSSynth = FOUR_CHAR_CODE('dls ')
kAudioUnitType_Effect = FOUR_CHAR_CODE('aufx')
kAudioUnitSubType_PeakLimiter = FOUR_CHAR_CODE('lmtr')
kAudioUnitType_Output = FOUR_CHAR_CODE('auou')
kAudioUnitSubType_DefaultOutput = FOUR_CHAR_CODE('def ')

class AudioComponentDescription(Structure):
    _fields_ = [("componentType", OSType),  # OSType componentType;
                ("componentSubType", OSType),  # OSType componentSubType;
                ("componentManufacturer", OSType),  # OSType componentManufacturer;
                ("componentFlags", c_uint32),  # UInt32 componentFlags;
                ("componentFlagsMask", c_uint32)]  # UInt32 componentFlagsMask;

# OSStatus NewAUGraph(AUGraph  _Nullable *outGraph);
_at.NewAUGraph.argtypes = [POINTER(AUGraph)]
_at.NewAUGraph.restype = OSStatus
NewAUGraph = _at.NewAUGraph

# OSStatus AUGraphAddNode(AUGraph inGraph, const AudioComponentDescription *inDescription, AUNode *outNode);
_at.AUGraphAddNode.argtypes = [AUGraph, POINTER(AudioComponentDescription), POINTER(AUNode)]
_at.AUGraphAddNode.restype = OSStatus
AUGraphAddNode = _at.AUGraphAddNode

# OSStatus AUGraphOpen(AUGraph inGraph);
_at.AUGraphOpen.argtypes = [AUGraph]
_at.AUGraphOpen.restype = OSStatus
AUGraphOpen = _at.AUGraphOpen

# OSStatus AUGraphConnectNodeInput(AUGraph inGraph, AUNode inSourceNode, UInt32 inSourceOutputNumber, AUNode inDestNode, UInt32 inDestInputNumber);
_at.AUGraphConnectNodeInput.argtypes = [AUGraph, AUNode, c_uint32, AUNode, c_uint32]
_at.AUGraphConnectNodeInput.restype = OSStatus
AUGraphConnectNodeInput = _at.AUGraphConnectNodeInput

# OSStatus AUGraphNodeInfo(AUGraph inGraph, AUNode inNode, AudioComponentDescription *outDescription, AudioUnit  _Nullable *outAudioUnit);
_at.AUGraphNodeInfo.argtypes = [AUGraph, AUNode, POINTER(AudioComponentDescription), POINTER(AudioUnit)]
_at.AUGraphNodeInfo.restype = OSStatus
AUGraphNodeInfo = _at.AUGraphNodeInfo

# OSStatus AUGraphInitialize(AUGraph inGraph);
_at.AUGraphInitialize.argtypes = [AUGraph]
_at.AUGraphInitialize.restype = OSStatus
AUGraphInitialize = _at.AUGraphInitialize

# OSStatus AUGraphStart(AUGraph inGraph);
_at.AUGraphStart.argtypes = [AUGraph]
_at.AUGraphStart.restype = OSStatus
AUGraphStart = _at.AUGraphStart

# OSStatus AudioUnitGetParameter(AudioUnit inUnit, AudioUnitParameterID inID, AudioUnitScope inScope, AudioUnitElement inElement, AudioUnitParameterValue *outValue);
_at.AudioUnitGetParameter.argtypes = [AudioUnit, AudioUnitParameterID, AudioUnitScope, AudioUnitElement, POINTER(AudioUnitParameterValue)]
_at.AudioUnitGetParameter.restype = OSStatus
AudioUnitGetParameter = _at.AudioUnitGetParameter

# OSStatus AudioUnitSetParameter(AudioUnit inUnit, AudioUnitParameterID inID, AudioUnitScope inScope, AudioUnitElement inElement, AudioUnitParameterValue inValue, UInt32 inBufferOffsetInFrames);
_at.AudioUnitSetParameter.argtypes = [AudioUnit, AudioUnitParameterID, AudioUnitScope, AudioUnitElement, AudioUnitParameterValue, c_uint32]
_at.AudioUnitSetParameter.restype = OSStatus
AudioUnitSetParameter = _at.AudioUnitSetParameter

# OSStatus MusicDeviceMIDIEvent(MusicDeviceComponent inUnit, UInt32 inStatus, UInt32 inData1, UInt32 inData2, UInt32 inOffsetSampleFrame);
_at.MusicDeviceMIDIEvent.argtypes = [MusicDeviceComponent, c_uint32, c_uint32, c_uint32, c_uint32]
_at.MusicDeviceMIDIEvent.restype = OSStatus
MusicDeviceMIDIEvent = _at.MusicDeviceMIDIEvent

# void CAShow(void *inObject);
_at.CAShow.argtypes = [c_void_p]
CAShow = _at.CAShow
