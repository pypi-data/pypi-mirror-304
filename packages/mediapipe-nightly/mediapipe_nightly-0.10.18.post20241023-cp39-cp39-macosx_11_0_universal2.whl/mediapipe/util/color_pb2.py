# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/util/color.proto
# Protobuf Python Version: 4.25.5
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1amediapipe/util/color.proto\x12\tmediapipe\"(\n\x05\x43olor\x12\t\n\x01r\x18\x01 \x01(\x05\x12\t\n\x01g\x18\x02 \x01(\x05\x12\t\n\x01\x62\x18\x03 \x01(\x05\"\x90\x01\n\x08\x43olorMap\x12=\n\x0elabel_to_color\x18\x01 \x03(\x0b\x32%.mediapipe.ColorMap.LabelToColorEntry\x1a\x45\n\x11LabelToColorEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x1f\n\x05value\x18\x02 \x01(\x0b\x32\x10.mediapipe.Color:\x02\x38\x01\x42-\n\x1f\x63om.google.mediapipe.util.protoB\nColorProto')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.util.color_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\037com.google.mediapipe.util.protoB\nColorProto'
  _globals['_COLORMAP_LABELTOCOLORENTRY']._options = None
  _globals['_COLORMAP_LABELTOCOLORENTRY']._serialized_options = b'8\001'
  _globals['_COLOR']._serialized_start=41
  _globals['_COLOR']._serialized_end=81
  _globals['_COLORMAP']._serialized_start=84
  _globals['_COLORMAP']._serialized_end=228
  _globals['_COLORMAP_LABELTOCOLORENTRY']._serialized_start=159
  _globals['_COLORMAP_LABELTOCOLORENTRY']._serialized_end=228
# @@protoc_insertion_point(module_scope)
