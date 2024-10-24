# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: nucliadb_protos/dataset.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from nucliadb_protos import resources_pb2 as nucliadb__protos_dot_resources__pb2
try:
  nucliadb__protos_dot_utils__pb2 = nucliadb__protos_dot_resources__pb2.nucliadb__protos_dot_utils__pb2
except AttributeError:
  nucliadb__protos_dot_utils__pb2 = nucliadb__protos_dot_resources__pb2.nucliadb_protos.utils_pb2

from nucliadb_protos.resources_pb2 import *

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1dnucliadb_protos/dataset.proto\x12\x07\x64\x61taset\x1a\x1fnucliadb_protos/resources.proto\"\x82\x02\n\x08TrainSet\x12\x1f\n\x04type\x18\x01 \x01(\x0e\x32\x11.dataset.TaskType\x12(\n\x06\x66ilter\x18\x02 \x01(\x0b\x32\x18.dataset.TrainSet.Filter\x12\x12\n\nbatch_size\x18\x03 \x01(\x05\x1a\x96\x01\n\x06\x46ilter\x12\x0e\n\x06labels\x18\x01 \x03(\t\x12\r\n\x05paths\x18\x02 \x03(\t\x12\x0c\n\x04rids\x18\x03 \x03(\t\x12\x0c\n\x04tags\x18\x04 \x03(\t\x12\r\n\x05icons\x18\x05 \x03(\t\x12\x10\n\x08metadata\x18\x06 \x03(\t\x12\x10\n\x08\x65ntities\x18\x07 \x03(\t\x12\x0e\n\x06\x66ields\x18\x08 \x03(\t\x12\x0e\n\x06status\x18\t \x03(\t\"L\n\x05Label\x12\x10\n\x08labelset\x18\x01 \x01(\t\x12\r\n\x05label\x18\x02 \x01(\t\x12\"\n\x06origin\x18\x03 \x01(\x0e\x32\x12.dataset.LabelFrom\"9\n\tTextLabel\x12\x0c\n\x04text\x18\x01 \x01(\t\x12\x1e\n\x06labels\x18\x02 \x03(\x0b\x32\x0e.dataset.Label\"F\n\x16MultipleTextSameLabels\x12\x0c\n\x04text\x18\x01 \x03(\t\x12\x1e\n\x06labels\x18\x02 \x03(\x0b\x32\x0e.dataset.Label\"<\n\x18\x46ieldClassificationBatch\x12 \n\x04\x64\x61ta\x18\x01 \x03(\x0b\x32\x12.dataset.TextLabel\"@\n\x1cParagraphClassificationBatch\x12 \n\x04\x64\x61ta\x18\x01 \x03(\x0b\x32\x12.dataset.TextLabel\"L\n\x1bSentenceClassificationBatch\x12-\n\x04\x64\x61ta\x18\x01 \x03(\x0b\x32\x1f.dataset.MultipleTextSameLabels\"4\n\x14TokensClassification\x12\r\n\x05token\x18\x01 \x03(\t\x12\r\n\x05label\x18\x02 \x03(\t\"G\n\x18TokenClassificationBatch\x12+\n\x04\x64\x61ta\x18\x01 \x03(\x0b\x32\x1d.dataset.TokensClassification\";\n\x13ImageClassification\x12\x12\n\nselections\x18\x01 \x01(\t\x12\x10\n\x08page_uri\x18\x02 \x01(\t\"F\n\x18ImageClassificationBatch\x12*\n\x04\x64\x61ta\x18\x01 \x03(\x0b\x32\x1c.dataset.ImageClassification\"/\n\x13ParagraphStreamItem\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04text\x18\x02 \x01(\t\"E\n\x17ParagraphStreamingBatch\x12*\n\x04\x64\x61ta\x18\x01 \x03(\x0b\x32\x1c.dataset.ParagraphStreamItem\"E\n\x0fQuestionDataset\x12\x0c\n\x04text\x18\x01 \x01(\t\x12\x10\n\x08language\x18\x02 \x01(\t\x12\x12\n\nparagraphs\x18\x03 \x03(\t\"<\n\x06\x41nswer\x12\x0c\n\x04text\x18\x01 \x01(\t\x12\x10\n\x08language\x18\x02 \x01(\t\x12\x12\n\nparagraphs\x18\x03 \x03(\t\"\x82\x01\n\x18QuestionAnswerStreamItem\x12*\n\x08question\x18\x01 \x01(\x0b\x32\x18.dataset.QuestionDataset\x12\x1f\n\x06\x61nswer\x18\x02 \x01(\x0b\x32\x0f.dataset.Answer\x12\x19\n\x11\x63\x61ncelled_by_user\x18\x03 \x01(\x08\"O\n\x1cQuestionAnswerStreamingBatch\x12/\n\x04\x64\x61ta\x18\x01 \x03(\x0b\x32!.dataset.QuestionAnswerStreamItem\"\xb0\x02\n\x0e\x46ieldSplitData\x12\r\n\x05split\x18\x01 \x01(\t\x12\x0b\n\x03rid\x18\x02 \x01(\t\x12\r\n\x05\x66ield\x18\x03 \x01(\t\x12\x12\n\nfield_type\x18\x04 \x01(\t\x12\x0e\n\x06labels\x18\x05 \x03(\t\x12\"\n\x04text\x18\x06 \x01(\x0b\x32\x14.utils.ExtractedText\x12\x1f\n\x05\x62\x61sic\x18\x07 \x01(\x0b\x32\x10.resources.Basic\x12*\n\x04\x66ile\x18\x08 \x01(\x0b\x32\x1c.resources.FileExtractedData\x12*\n\x04link\x18\t \x01(\x0b\x32\x1c.resources.LinkExtractedData\x12\x32\n\x08metadata\x18\n \x01(\x0b\x32 .resources.FieldComputedMetadata\"<\n\x13\x46ieldStreamingBatch\x12%\n\x04\x64\x61ta\x18\x01 \x03(\x0b\x32\x17.dataset.FieldSplitData*\xe0\x01\n\x08TaskType\x12\x18\n\x14\x46IELD_CLASSIFICATION\x10\x00\x12\x1c\n\x18PARAGRAPH_CLASSIFICATION\x10\x01\x12\x1b\n\x17SENTENCE_CLASSIFICATION\x10\x02\x12\x18\n\x14TOKEN_CLASSIFICATION\x10\x03\x12\x18\n\x14IMAGE_CLASSIFICATION\x10\x04\x12\x17\n\x13PARAGRAPH_STREAMING\x10\x05\x12\x1d\n\x19QUESTION_ANSWER_STREAMING\x10\x06\x12\x13\n\x0f\x46IELD_STREAMING\x10\x07*3\n\tLabelFrom\x12\r\n\tPARAGRAPH\x10\x00\x12\t\n\x05\x46IELD\x10\x01\x12\x0c\n\x08RESOURCE\x10\x02P\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'nucliadb_protos.dataset_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_TASKTYPE']._serialized_start=1848
  _globals['_TASKTYPE']._serialized_end=2072
  _globals['_LABELFROM']._serialized_start=2074
  _globals['_LABELFROM']._serialized_end=2125
  _globals['_TRAINSET']._serialized_start=76
  _globals['_TRAINSET']._serialized_end=334
  _globals['_TRAINSET_FILTER']._serialized_start=184
  _globals['_TRAINSET_FILTER']._serialized_end=334
  _globals['_LABEL']._serialized_start=336
  _globals['_LABEL']._serialized_end=412
  _globals['_TEXTLABEL']._serialized_start=414
  _globals['_TEXTLABEL']._serialized_end=471
  _globals['_MULTIPLETEXTSAMELABELS']._serialized_start=473
  _globals['_MULTIPLETEXTSAMELABELS']._serialized_end=543
  _globals['_FIELDCLASSIFICATIONBATCH']._serialized_start=545
  _globals['_FIELDCLASSIFICATIONBATCH']._serialized_end=605
  _globals['_PARAGRAPHCLASSIFICATIONBATCH']._serialized_start=607
  _globals['_PARAGRAPHCLASSIFICATIONBATCH']._serialized_end=671
  _globals['_SENTENCECLASSIFICATIONBATCH']._serialized_start=673
  _globals['_SENTENCECLASSIFICATIONBATCH']._serialized_end=749
  _globals['_TOKENSCLASSIFICATION']._serialized_start=751
  _globals['_TOKENSCLASSIFICATION']._serialized_end=803
  _globals['_TOKENCLASSIFICATIONBATCH']._serialized_start=805
  _globals['_TOKENCLASSIFICATIONBATCH']._serialized_end=876
  _globals['_IMAGECLASSIFICATION']._serialized_start=878
  _globals['_IMAGECLASSIFICATION']._serialized_end=937
  _globals['_IMAGECLASSIFICATIONBATCH']._serialized_start=939
  _globals['_IMAGECLASSIFICATIONBATCH']._serialized_end=1009
  _globals['_PARAGRAPHSTREAMITEM']._serialized_start=1011
  _globals['_PARAGRAPHSTREAMITEM']._serialized_end=1058
  _globals['_PARAGRAPHSTREAMINGBATCH']._serialized_start=1060
  _globals['_PARAGRAPHSTREAMINGBATCH']._serialized_end=1129
  _globals['_QUESTIONDATASET']._serialized_start=1131
  _globals['_QUESTIONDATASET']._serialized_end=1200
  _globals['_ANSWER']._serialized_start=1202
  _globals['_ANSWER']._serialized_end=1262
  _globals['_QUESTIONANSWERSTREAMITEM']._serialized_start=1265
  _globals['_QUESTIONANSWERSTREAMITEM']._serialized_end=1395
  _globals['_QUESTIONANSWERSTREAMINGBATCH']._serialized_start=1397
  _globals['_QUESTIONANSWERSTREAMINGBATCH']._serialized_end=1476
  _globals['_FIELDSPLITDATA']._serialized_start=1479
  _globals['_FIELDSPLITDATA']._serialized_end=1783
  _globals['_FIELDSTREAMINGBATCH']._serialized_start=1785
  _globals['_FIELDSTREAMINGBATCH']._serialized_end=1845
# @@protoc_insertion_point(module_scope)
