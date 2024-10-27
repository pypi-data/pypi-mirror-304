"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from PyDefold.ddf import ddf_extensions_pb2 as ddf_dot_ddf__extensions__pb2
from PyDefold.ddf import ddf_math_pb2 as ddf_dot_ddf__math__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x19gamesys/gamesys_ddf.proto\x12\x0fdmGameSystemDDF\x1a\x18ddf/ddf_extensions.proto\x1a\x12ddf/ddf_math.proto"i\n\x0bFactoryDesc\x12\x17\n\tprototype\x18\x01 \x02(\tB\x04\xa0\xbb\x18\x01\x12\x1f\n\x10load_dynamically\x18\x02 \x01(\x08:\x05false\x12 \n\x11dynamic_prototype\x18\x03 \x01(\x08:\x05false"s\n\x15CollectionFactoryDesc\x12\x17\n\tprototype\x18\x01 \x02(\tB\x04\xa0\xbb\x18\x01\x12\x1f\n\x10load_dynamically\x18\x02 \x01(\x08:\x05false\x12 \n\x11dynamic_prototype\x18\x03 \x01(\x08:\x05false"\xb9\x01\n\x06Create\x12&\n\x08position\x18\x01 \x02(\x0b2\x0e.dmMath.Point3B\x04\xa0\xb5\x18\x01\x12$\n\x08rotation\x18\x02 \x02(\x0b2\x0c.dmMath.QuatB\x04\xa0\xb5\x18\x01\x12\r\n\x02id\x18\x03 \x01(\x04:\x010\x12\x10\n\x05scale\x18\x04 \x01(\x02:\x011\x12%\n\x06scale3\x18\x05 \x01(\x0b2\x0f.dmMath.Vector3B\x04\xa0\xb5\x18\x01\x12\x19\n\x05index\x18\x06 \x01(\r:\n4294967295"G\n\x13CollectionProxyDesc\x12\x18\n\ncollection\x18\x01 \x02(\tB\x04\xa0\xbb\x18\x01\x12\x16\n\x07exclude\x18\x02 \x01(\x08:\x05false"J\n\x0bSetTimeStep\x12\x0e\n\x06factor\x18\x01 \x02(\x02\x12+\n\x04mode\x18\x02 \x02(\x0e2\x1d.dmGameSystemDDF.TimeStepMode"\xd0\x01\n\tLightDesc\x12\n\n\x02id\x18\x01 \x02(\t\x12(\n\x04type\x18\x02 \x02(\x0e2\x1a.dmGameSystemDDF.LightType\x12\x11\n\tintensity\x18\x03 \x02(\x02\x12\x1e\n\x05color\x18\x04 \x02(\x0b2\x0f.dmMath.Vector3\x12\r\n\x05range\x18\x05 \x02(\x02\x12\r\n\x05decay\x18\x06 \x02(\x02\x12\x12\n\ncone_angle\x18\x07 \x01(\x02\x12\x16\n\x0epenumbra_angle\x18\x08 \x01(\x02\x12\x10\n\x08drop_off\x18\t \x01(\x02"w\n\x08SetLight\x12 \n\x08position\x18\x01 \x02(\x0b2\x0e.dmMath.Point3\x12\x1e\n\x08rotation\x18\x02 \x02(\x0b2\x0c.dmMath.Quat\x12)\n\x05light\x18\x03 \x02(\x0b2\x1a.dmGameSystemDDF.LightDesc"c\n\x11SetViewProjection\x12\n\n\x02id\x18\x01 \x02(\x04\x12\x1d\n\x04view\x18\x02 \x02(\x0b2\x0f.dmMath.Matrix4\x12#\n\nprojection\x18\x03 \x02(\x0b2\x0f.dmMath.Matrix4"m\n\tPlaySound\x12\x10\n\x05delay\x18\x01 \x01(\x02:\x010\x12\x0f\n\x04gain\x18\x02 \x01(\x02:\x011\x12\x0e\n\x03pan\x18\x03 \x01(\x02:\x010\x12\x10\n\x05speed\x18\x04 \x01(\x02:\x011\x12\x1b\n\x07play_id\x18\x05 \x01(\r:\n4294967295"(\n\tStopSound\x12\x1b\n\x07play_id\x18\x01 \x01(\r:\n4294967295"!\n\nPauseSound\x12\x13\n\x05pause\x18\x01 \x01(\x08:\x04true" \n\nSoundEvent\x12\x12\n\x07play_id\x18\x01 \x01(\x05:\x010"\x1a\n\x07SetGain\x12\x0f\n\x04gain\x18\x01 \x01(\x02:\x011"\x18\n\x06SetPan\x12\x0e\n\x03pan\x18\x01 \x01(\x02:\x010"\x1c\n\x08SetSpeed\x12\x10\n\x05speed\x18\x01 \x01(\x02:\x011"\x10\n\x0ePlayParticleFX"0\n\x0eStopParticleFX\x12\x1e\n\x0fclear_particles\x18\x01 \x01(\x08:\x05false"x\n\x15SetConstantParticleFX\x12\x12\n\nemitter_id\x18\x01 \x02(\x04\x12\x11\n\tname_hash\x18\x02 \x02(\x04\x12$\n\x05value\x18\x03 \x02(\x0b2\x0f.dmMath.Matrix4B\x04\xa0\xb5\x18\x01\x12\x12\n\nis_matrix4\x18\x04 \x01(\x08"@\n\x17ResetConstantParticleFX\x12\x12\n\nemitter_id\x18\x01 \x02(\x04\x12\x11\n\tname_hash\x18\x02 \x02(\x04"X\n\x0bSetConstant\x12\x11\n\tname_hash\x18\x01 \x02(\x04\x12$\n\x05value\x18\x02 \x02(\x0b2\x0f.dmMath.Vector4B\x04\xa0\xb5\x18\x01\x12\x10\n\x05index\x18\x03 \x01(\x05:\x010""\n\rResetConstant\x12\x11\n\tname_hash\x18\x01 \x02(\x04"0\n\x08SetScale\x12$\n\x05scale\x18\x01 \x02(\x0b2\x0f.dmMath.Vector3B\x04\xa0\xb5\x18\x01*J\n\x0cTimeStepMode\x12\x1d\n\x19TIME_STEP_MODE_CONTINUOUS\x10\x00\x12\x1b\n\x17TIME_STEP_MODE_DISCRETE\x10\x01* \n\tLightType\x12\t\n\x05POINT\x10\x00\x12\x08\n\x04SPOT\x10\x01B&\n\x18com.dynamo.gamesys.protoB\nGameSystem')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'gamesys.gamesys_ddf_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n\x18com.dynamo.gamesys.protoB\nGameSystem'
    _FACTORYDESC.fields_by_name['prototype']._options = None
    _FACTORYDESC.fields_by_name['prototype']._serialized_options = b'\xa0\xbb\x18\x01'
    _COLLECTIONFACTORYDESC.fields_by_name['prototype']._options = None
    _COLLECTIONFACTORYDESC.fields_by_name['prototype']._serialized_options = b'\xa0\xbb\x18\x01'
    _CREATE.fields_by_name['position']._options = None
    _CREATE.fields_by_name['position']._serialized_options = b'\xa0\xb5\x18\x01'
    _CREATE.fields_by_name['rotation']._options = None
    _CREATE.fields_by_name['rotation']._serialized_options = b'\xa0\xb5\x18\x01'
    _CREATE.fields_by_name['scale3']._options = None
    _CREATE.fields_by_name['scale3']._serialized_options = b'\xa0\xb5\x18\x01'
    _COLLECTIONPROXYDESC.fields_by_name['collection']._options = None
    _COLLECTIONPROXYDESC.fields_by_name['collection']._serialized_options = b'\xa0\xbb\x18\x01'
    _SETCONSTANTPARTICLEFX.fields_by_name['value']._options = None
    _SETCONSTANTPARTICLEFX.fields_by_name['value']._serialized_options = b'\xa0\xb5\x18\x01'
    _SETCONSTANT.fields_by_name['value']._options = None
    _SETCONSTANT.fields_by_name['value']._serialized_options = b'\xa0\xb5\x18\x01'
    _SETSCALE.fields_by_name['scale']._options = None
    _SETSCALE.fields_by_name['scale']._serialized_options = b'\xa0\xb5\x18\x01'
    _TIMESTEPMODE._serialized_start = 1824
    _TIMESTEPMODE._serialized_end = 1898
    _LIGHTTYPE._serialized_start = 1900
    _LIGHTTYPE._serialized_end = 1932
    _FACTORYDESC._serialized_start = 92
    _FACTORYDESC._serialized_end = 197
    _COLLECTIONFACTORYDESC._serialized_start = 199
    _COLLECTIONFACTORYDESC._serialized_end = 314
    _CREATE._serialized_start = 317
    _CREATE._serialized_end = 502
    _COLLECTIONPROXYDESC._serialized_start = 504
    _COLLECTIONPROXYDESC._serialized_end = 575
    _SETTIMESTEP._serialized_start = 577
    _SETTIMESTEP._serialized_end = 651
    _LIGHTDESC._serialized_start = 654
    _LIGHTDESC._serialized_end = 862
    _SETLIGHT._serialized_start = 864
    _SETLIGHT._serialized_end = 983
    _SETVIEWPROJECTION._serialized_start = 985
    _SETVIEWPROJECTION._serialized_end = 1084
    _PLAYSOUND._serialized_start = 1086
    _PLAYSOUND._serialized_end = 1195
    _STOPSOUND._serialized_start = 1197
    _STOPSOUND._serialized_end = 1237
    _PAUSESOUND._serialized_start = 1239
    _PAUSESOUND._serialized_end = 1272
    _SOUNDEVENT._serialized_start = 1274
    _SOUNDEVENT._serialized_end = 1306
    _SETGAIN._serialized_start = 1308
    _SETGAIN._serialized_end = 1334
    _SETPAN._serialized_start = 1336
    _SETPAN._serialized_end = 1360
    _SETSPEED._serialized_start = 1362
    _SETSPEED._serialized_end = 1390
    _PLAYPARTICLEFX._serialized_start = 1392
    _PLAYPARTICLEFX._serialized_end = 1408
    _STOPPARTICLEFX._serialized_start = 1410
    _STOPPARTICLEFX._serialized_end = 1458
    _SETCONSTANTPARTICLEFX._serialized_start = 1460
    _SETCONSTANTPARTICLEFX._serialized_end = 1580
    _RESETCONSTANTPARTICLEFX._serialized_start = 1582
    _RESETCONSTANTPARTICLEFX._serialized_end = 1646
    _SETCONSTANT._serialized_start = 1648
    _SETCONSTANT._serialized_end = 1736
    _RESETCONSTANT._serialized_start = 1738
    _RESETCONSTANT._serialized_end = 1772
    _SETSCALE._serialized_start = 1774
    _SETSCALE._serialized_end = 1822
