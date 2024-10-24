# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: schema.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cschema.proto\x12\x13\x66\x65nnel.proto.schema\x1a\x1fgoogle/protobuf/timestamp.proto\"\xb8\x07\n\x08\x44\x61taType\x12\x30\n\x08int_type\x18\x01 \x01(\x0b\x32\x1c.fennel.proto.schema.IntTypeH\x00\x12\x36\n\x0b\x64ouble_type\x18\x02 \x01(\x0b\x32\x1f.fennel.proto.schema.DoubleTypeH\x00\x12\x36\n\x0bstring_type\x18\x03 \x01(\x0b\x32\x1f.fennel.proto.schema.StringTypeH\x00\x12\x32\n\tbool_type\x18\x04 \x01(\x0b\x32\x1d.fennel.proto.schema.BoolTypeH\x00\x12<\n\x0etimestamp_type\x18\x05 \x01(\x0b\x32\".fennel.proto.schema.TimestampTypeH\x00\x12\x34\n\narray_type\x18\x06 \x01(\x0b\x32\x1e.fennel.proto.schema.ArrayTypeH\x00\x12\x30\n\x08map_type\x18\x07 \x01(\x0b\x32\x1c.fennel.proto.schema.MapTypeH\x00\x12<\n\x0e\x65mbedding_type\x18\x08 \x01(\x0b\x32\".fennel.proto.schema.EmbeddingTypeH\x00\x12\x34\n\x0c\x62\x65tween_type\x18\t \x01(\x0b\x32\x1c.fennel.proto.schema.BetweenH\x00\x12\x31\n\x0bone_of_type\x18\n \x01(\x0b\x32\x1a.fennel.proto.schema.OneOfH\x00\x12\x34\n\nregex_type\x18\x0b \x01(\x0b\x32\x1e.fennel.proto.schema.RegexTypeH\x00\x12:\n\roptional_type\x18\x0c \x01(\x0b\x32!.fennel.proto.schema.OptionalTypeH\x00\x12\x36\n\x0bstruct_type\x18\r \x01(\x0b\x32\x1f.fennel.proto.schema.StructTypeH\x00\x12\x38\n\x0c\x64\x65\x63imal_type\x18\x0e \x01(\x0b\x32 .fennel.proto.schema.DecimalTypeH\x00\x12\x32\n\tdate_type\x18\x0f \x01(\x0b\x32\x1d.fennel.proto.schema.DateTypeH\x00\x12\x34\n\nbytes_type\x18\x10 \x01(\x0b\x32\x1e.fennel.proto.schema.BytesTypeH\x00\x12\x32\n\tnull_type\x18\x11 \x01(\x0b\x32\x1d.fennel.proto.schema.NullTypeH\x00\x42\x07\n\x05\x64type\"C\n\x05\x46ield\x12\x0c\n\x04name\x18\x01 \x01(\t\x12,\n\x05\x64type\x18\x02 \x01(\x0b\x32\x1d.fennel.proto.schema.DataType\"\n\n\x08NullType\"\t\n\x07IntType\"\x0c\n\nDoubleType\"\x0c\n\nStringType\"\n\n\x08\x42oolType\"\x0f\n\rTimestampType\"\n\n\x08\x44\x61teType\"\x0b\n\tBytesType\"\x1c\n\tRegexType\x12\x0f\n\x07pattern\x18\x01 \x01(\t\"6\n\tArrayType\x12)\n\x02of\x18\x01 \x01(\x0b\x32\x1d.fennel.proto.schema.DataType\"\'\n\rEmbeddingType\x12\x16\n\x0e\x65mbedding_size\x18\x02 \x01(\x05\"c\n\x07MapType\x12*\n\x03key\x18\x01 \x01(\x0b\x32\x1d.fennel.proto.schema.DataType\x12,\n\x05value\x18\x02 \x01(\x0b\x32\x1d.fennel.proto.schema.DataType\"F\n\nStructType\x12\x0c\n\x04name\x18\x01 \x01(\t\x12*\n\x06\x66ields\x18\x02 \x03(\x0b\x32\x1a.fennel.proto.schema.Field\"\xb1\x01\n\x07\x42\x65tween\x12,\n\x05\x64type\x18\x01 \x01(\x0b\x32\x1d.fennel.proto.schema.DataType\x12\'\n\x03min\x18\x02 \x01(\x0b\x32\x1a.fennel.proto.schema.Value\x12\'\n\x03max\x18\x03 \x01(\x0b\x32\x1a.fennel.proto.schema.Value\x12\x12\n\nstrict_min\x18\x04 \x01(\x08\x12\x12\n\nstrict_max\x18\x05 \x01(\x08\"_\n\x05OneOf\x12)\n\x02of\x18\x01 \x01(\x0b\x32\x1d.fennel.proto.schema.DataType\x12+\n\x07options\x18\x02 \x03(\x0b\x32\x1a.fennel.proto.schema.Value\"9\n\x0cOptionalType\x12)\n\x02of\x18\x01 \x01(\x0b\x32\x1d.fennel.proto.schema.DataType\"\x1c\n\x0b\x44\x65\x63imalType\x12\r\n\x05scale\x18\x01 \x01(\x05\"4\n\x06Schema\x12*\n\x06\x66ields\x18\x01 \x03(\x0b\x32\x1a.fennel.proto.schema.Field\"\x89\x01\n\x08\x44SSchema\x12)\n\x04keys\x18\x01 \x01(\x0b\x32\x1b.fennel.proto.schema.Schema\x12+\n\x06values\x18\x02 \x01(\x0b\x32\x1b.fennel.proto.schema.Schema\x12\x11\n\ttimestamp\x18\x03 \x01(\t\x12\x12\n\nerase_keys\x18\x04 \x03(\t\"\xda\x03\n\x05Value\x12)\n\x04none\x18\x01 \x01(\x0b\x32\x19.fennel.proto.schema.NoneH\x00\x12\x0e\n\x04\x62ool\x18\x02 \x01(\x08H\x00\x12\r\n\x03int\x18\x03 \x01(\x03H\x00\x12\x0f\n\x05\x66loat\x18\x04 \x01(\x01H\x00\x12\x10\n\x06string\x18\x05 \x01(\tH\x00\x12/\n\ttimestamp\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.TimestampH\x00\x12\x33\n\tembedding\x18\x07 \x01(\x0b\x32\x1e.fennel.proto.schema.EmbeddingH\x00\x12)\n\x04list\x18\x08 \x01(\x0b\x32\x19.fennel.proto.schema.ListH\x00\x12\'\n\x03map\x18\t \x01(\x0b\x32\x18.fennel.proto.schema.MapH\x00\x12\x32\n\x06struct\x18\n \x01(\x0b\x32 .fennel.proto.schema.StructValueH\x00\x12/\n\x07\x64\x65\x63imal\x18\x0b \x01(\x0b\x32\x1c.fennel.proto.schema.DecimalH\x00\x12)\n\x04\x64\x61te\x18\x0c \x01(\x0b\x32\x19.fennel.proto.schema.DateH\x00\x12\x0f\n\x05\x62ytes\x18\r \x01(\x0cH\x00\x42\t\n\x07variant\"\x1b\n\tEmbedding\x12\x0e\n\x06values\x18\x01 \x03(\x01\"`\n\x04List\x12,\n\x05\x64type\x18\x01 \x01(\x0b\x32\x1d.fennel.proto.schema.DataType\x12*\n\x06values\x18\x02 \x03(\x0b\x32\x1a.fennel.proto.schema.Value\"\xf9\x01\n\x03Map\x12\x30\n\tkey_dtype\x18\x01 \x01(\x0b\x32\x1d.fennel.proto.schema.DataType\x12\x32\n\x0bvalue_dtype\x18\x02 \x01(\x0b\x32\x1d.fennel.proto.schema.DataType\x12/\n\x07\x65ntries\x18\x03 \x03(\x0b\x32\x1e.fennel.proto.schema.Map.Entry\x1a[\n\x05\x45ntry\x12\'\n\x03key\x18\x01 \x01(\x0b\x32\x1a.fennel.proto.schema.Value\x12)\n\x05value\x18\x02 \x01(\x0b\x32\x1a.fennel.proto.schema.Value\"\x87\x01\n\x0bStructValue\x12\x36\n\x06\x66ields\x18\x01 \x03(\x0b\x32&.fennel.proto.schema.StructValue.Entry\x1a@\n\x05\x45ntry\x12\x0c\n\x04name\x18\x01 \x01(\t\x12)\n\x05value\x18\x02 \x01(\x0b\x32\x1a.fennel.proto.schema.Value\"\'\n\x07\x44\x65\x63imal\x12\r\n\x05scale\x18\x01 \x01(\x05\x12\r\n\x05value\x18\x02 \x01(\x03\"\x14\n\x04\x44\x61te\x12\x0c\n\x04\x64\x61ys\x18\x02 \x01(\x03\"\x06\n\x04Noneb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'schema_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_DATATYPE']._serialized_start=71
  _globals['_DATATYPE']._serialized_end=1023
  _globals['_FIELD']._serialized_start=1025
  _globals['_FIELD']._serialized_end=1092
  _globals['_NULLTYPE']._serialized_start=1094
  _globals['_NULLTYPE']._serialized_end=1104
  _globals['_INTTYPE']._serialized_start=1106
  _globals['_INTTYPE']._serialized_end=1115
  _globals['_DOUBLETYPE']._serialized_start=1117
  _globals['_DOUBLETYPE']._serialized_end=1129
  _globals['_STRINGTYPE']._serialized_start=1131
  _globals['_STRINGTYPE']._serialized_end=1143
  _globals['_BOOLTYPE']._serialized_start=1145
  _globals['_BOOLTYPE']._serialized_end=1155
  _globals['_TIMESTAMPTYPE']._serialized_start=1157
  _globals['_TIMESTAMPTYPE']._serialized_end=1172
  _globals['_DATETYPE']._serialized_start=1174
  _globals['_DATETYPE']._serialized_end=1184
  _globals['_BYTESTYPE']._serialized_start=1186
  _globals['_BYTESTYPE']._serialized_end=1197
  _globals['_REGEXTYPE']._serialized_start=1199
  _globals['_REGEXTYPE']._serialized_end=1227
  _globals['_ARRAYTYPE']._serialized_start=1229
  _globals['_ARRAYTYPE']._serialized_end=1283
  _globals['_EMBEDDINGTYPE']._serialized_start=1285
  _globals['_EMBEDDINGTYPE']._serialized_end=1324
  _globals['_MAPTYPE']._serialized_start=1326
  _globals['_MAPTYPE']._serialized_end=1425
  _globals['_STRUCTTYPE']._serialized_start=1427
  _globals['_STRUCTTYPE']._serialized_end=1497
  _globals['_BETWEEN']._serialized_start=1500
  _globals['_BETWEEN']._serialized_end=1677
  _globals['_ONEOF']._serialized_start=1679
  _globals['_ONEOF']._serialized_end=1774
  _globals['_OPTIONALTYPE']._serialized_start=1776
  _globals['_OPTIONALTYPE']._serialized_end=1833
  _globals['_DECIMALTYPE']._serialized_start=1835
  _globals['_DECIMALTYPE']._serialized_end=1863
  _globals['_SCHEMA']._serialized_start=1865
  _globals['_SCHEMA']._serialized_end=1917
  _globals['_DSSCHEMA']._serialized_start=1920
  _globals['_DSSCHEMA']._serialized_end=2057
  _globals['_VALUE']._serialized_start=2060
  _globals['_VALUE']._serialized_end=2534
  _globals['_EMBEDDING']._serialized_start=2536
  _globals['_EMBEDDING']._serialized_end=2563
  _globals['_LIST']._serialized_start=2565
  _globals['_LIST']._serialized_end=2661
  _globals['_MAP']._serialized_start=2664
  _globals['_MAP']._serialized_end=2913
  _globals['_MAP_ENTRY']._serialized_start=2822
  _globals['_MAP_ENTRY']._serialized_end=2913
  _globals['_STRUCTVALUE']._serialized_start=2916
  _globals['_STRUCTVALUE']._serialized_end=3051
  _globals['_STRUCTVALUE_ENTRY']._serialized_start=2987
  _globals['_STRUCTVALUE_ENTRY']._serialized_end=3051
  _globals['_DECIMAL']._serialized_start=3053
  _globals['_DECIMAL']._serialized_end=3092
  _globals['_DATE']._serialized_start=3094
  _globals['_DATE']._serialized_end=3114
  _globals['_NONE']._serialized_start=3116
  _globals['_NONE']._serialized_end=3122
# @@protoc_insertion_point(module_scope)
