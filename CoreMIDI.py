from ctypes import *
import ctypes.util

from CoreFoundation import *

_cm = CDLL(ctypes.util.find_library("CoreMIDI"))

kMIDIPropertyDisplayName = c_char_p(b"displayName")

ItemCount = c_ulong
ByteCount = c_ulong
Byte = c_ubyte
MIDIObjectRef = c_uint32 # typedef UInt32 MIDIObjectRef;
MIDIEndpointRef = MIDIObjectRef # typedef MIDIObjectRef MIDIEndpointRef;
MIDIClientRef = MIDIObjectRef # typedef MIDIObjectRef MIDIClientRef;
MIDINotifyProc = c_void_p # typedef void (*MIDINotifyProc)(const MIDINotification *message, void *refCon);
MIDIReadProc = c_void_p # typedef void (*MIDIReadProc)(const MIDIPacketList *pktlist, void *readProcRefCon, void *srcConnRefCon);
MIDIPortRef = MIDIObjectRef # typedef MIDIObjectRef MIDIPortRef;
MIDITimeStamp = c_uint64 # typedef UInt64 MIDITimeStamp;

class MIDIPacket(Structure):
    _pack_ = 1
    _fields_ = [("timeStamp", MIDITimeStamp), # MIDITimeStamp timeStamp;
                ("length", c_uint16), # UInt16 length;
                ("data", Byte*256)] # Byte data[256];

class MIDIPacketList(Structure):
    _fields_ = [("numPackets", c_uint32), # UInt32 numPackets;
                ("packet", MIDIPacket*1)] # MIDIPacket packet[1];

# MIDIEndpointRef MIDIGetSource(ItemCount sourceIndex0);
_cm.MIDIGetSource.argtypes = [ItemCount]
_cm.MIDIGetSource.restype = MIDIEndpointRef
MIDIGetSource = _cm.MIDIGetSource

# MIDIEndpointRef MIDIGetDestination(ItemCount destIndex0);
_cm.MIDIGetDestination.argtypes = [ItemCount]
_cm.MIDIGetDestination.restype = MIDIEndpointRef
MIDIGetDestination = _cm.MIDIGetDestination

# ItemCount MIDIGetNumberOfSources(void);
_cm.MIDIGetNumberOfSources.restype = ItemCount
MIDIGetNumberOfSources = _cm.MIDIGetNumberOfSources

# ItemCount MIDIGetNumberOfDestinations(void);
_cm.MIDIGetNumberOfDestinations.restype = ItemCount
MIDIGetNumberOfDestinations = _cm.MIDIGetNumberOfDestinations

# OSStatus MIDIObjectGetStringProperty(MIDIObjectRef obj, CFStringRef propertyID, CFStringRef  _Nullable *str);
_cm.MIDIObjectGetStringProperty.argtypes = [MIDIObjectRef, CFStringRef, POINTER(CFStringRef)]
_cm.MIDIObjectGetStringProperty.restype = OSStatus
MIDIObjectGetStringProperty = _cm.MIDIObjectGetStringProperty

# OSStatus MIDIClientCreate(CFStringRef name, MIDINotifyProc notifyProc, void *notifyRefCon, MIDIClientRef *outClient);
_cm.MIDIClientCreate.argtypes = [CFStringRef, MIDINotifyProc, c_void_p, POINTER(MIDIClientRef)]
_cm.MIDIClientCreate.restype = OSStatus
MIDIClientCreate = _cm.MIDIClientCreate

# OSStatus MIDIInputPortCreate(MIDIClientRef client, CFStringRef portName, MIDIReadProc readProc, void *refCon, MIDIPortRef *outPort);
_cm.MIDIInputPortCreate.argtypes = [MIDIClientRef, CFStringRef, MIDIReadProc, c_void_p, POINTER(MIDIPortRef)]
_cm.MIDIInputPortCreate.restype = OSStatus
MIDIInputPortCreate = _cm.MIDIInputPortCreate

# OSStatus MIDIOutputPortCreate(MIDIClientRef client, CFStringRef portName, MIDIPortRef *outPort);
_cm.MIDIOutputPortCreate.argtypes = [MIDIClientRef, CFStringRef, POINTER(MIDIPortRef)]
_cm.MIDIOutputPortCreate.restype = OSStatus
MIDIOutputPortCreate = _cm.MIDIOutputPortCreate

# OSStatus MIDIPortConnectSource(MIDIPortRef port, MIDIEndpointRef source, void *connRefCon);
_cm.MIDIPortConnectSource.argtypes = [MIDIPortRef, MIDIEndpointRef, c_void_p]
_cm.MIDIPortConnectSource.restype = OSStatus
MIDIPortConnectSource = _cm.MIDIPortConnectSource

# OSStatus MIDIPortDisconnectSource(MIDIPortRef port, MIDIEndpointRef source);
_cm.MIDIPortDisconnectSource.argtypes = [MIDIPortRef, MIDIEndpointRef]
_cm.MIDIPortDisconnectSource.restype = OSStatus
MIDIPortDisconnectSource = _cm.MIDIPortDisconnectSource

# MIDIPacket * MIDIPacketListInit(MIDIPacketList *pktlist);
_cm.MIDIPacketListInit.argtypes = [POINTER(MIDIPacketList)]
_cm.MIDIPacketListInit.restype = POINTER(MIDIPacket)
MIDIPacketListInit = _cm.MIDIPacketListInit

# MIDIPacket * MIDIPacketListAdd(MIDIPacketList *pktlist, ByteCount listSize, MIDIPacket *curPacket, MIDITimeStamp time, ByteCount nData, const Byte *data);
_cm.MIDIPacketListAdd.argtypes = [POINTER(MIDIPacketList), ByteCount, POINTER(MIDIPacket), MIDITimeStamp, ByteCount, POINTER(Byte)]
_cm.MIDIPacketListAdd.restype = POINTER(MIDIPacket)
MIDIPacketListAdd = _cm.MIDIPacketListAdd

# OSStatus MIDISend(MIDIPortRef port, MIDIEndpointRef dest, const MIDIPacketList *pktlist);
_cm.MIDISend.argtypes = [MIDIPortRef, MIDIEndpointRef, POINTER(MIDIPacketList)]
_cm.MIDISend.restype = OSStatus
MIDISend = _cm.MIDISend
