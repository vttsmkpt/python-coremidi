from ctypes import *
import ctypes.util

_cf = CDLL(ctypes.util.find_library("CoreFoundation"))

FourCharCode = c_uint  # typedef unsigned int FourCharCode;
OSType = FourCharCode   # typedef FourCharCode OSType;
OSStatus = c_int32  # typedef SInt32 OSStatus;

CFIndex = c_long  # typedef long CFIndex;
CFStringEncoding = c_uint32  # typedef UInt32 CFStringEncoding;
CFString = c_void_p
CFArray = c_void_p
CFDictionary = c_void_p
CFError = c_void_p
CFType = c_void_p

CFAllocatorRef = c_void_p
CFStringRef = POINTER(CFString)
CFArrayRef = POINTER(CFArray)
CFDictionaryRef = POINTER(CFDictionary)
CFErrorRef = POINTER(CFError)
CFTypeRef = POINTER(CFType)

kCFStringEncodingUTF8 = CFStringEncoding(0x08000100)

# CFStringRef CFStringCreateWithCString(CFAllocatorRef alloc, const char *cStr, CFStringEncoding encoding);
_cf.CFStringCreateWithCString.argstype = [CFAllocatorRef, c_char_p, CFStringEncoding]
_cf.CFStringCreateWithCString.restype = CFStringRef
CFStringCreateWithCString = _cf.CFStringCreateWithCString

# Boolean CFStringGetCString(CFStringRef theString, char *buffer, CFIndex bufferSize, CFStringEncoding encoding);
_cf.CFStringGetCString.argtypes = [CFStringRef, c_char_p, CFIndex, CFStringEncoding]
_cf.CFStringGetCString.restype = c_bool
CFStringGetCString = _cf.CFStringGetCString

# const char * CFStringGetCStringPtr(CFStringRef theString, CFStringEncoding encoding);
_cf.CFStringGetCStringPtr.argtypes = [CFStringRef, CFStringEncoding]
_cf.CFStringGetCStringPtr.restype = c_char_p
CFStringGetCStringPtr = _cf.CFStringGetCStringPtr

# CFIndex CFStringGetLength(CFStringRef theString);
_cf.CFStringGetLength.argtypes = [CFStringRef]
_cf.CFStringGetLength.restype = CFIndex
CFStringGetLength = _cf.CFStringGetLength
