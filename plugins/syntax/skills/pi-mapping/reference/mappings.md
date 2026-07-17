# Message mappings (XI_TRAFO) - dependency graph

source message -> [mapping] -> target message, plus used function libraries. Field-level logic is in the `tr:blob` payloads (decode with `extract-mapping`).

### `MM_ASC830_004010__2__SCHEDGAGRMTDLIVSCHEDULE_IN`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/customers`
- source: `MT_ASC830_004010`  ->  target: `SPS_S4HC_SCHEDGAGRMTDLIVSCHEDULE_IN`
- function libraries: SyntaxEDI_Text, SyntaxEDI_Node

### `MM_ASC862_004010__2__SCHEDGAGRMTDLIVSCHEDULE_IN`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/customers`
- source: `MT_ASC862_004010`  ->  target: `SPS_S4HC_SCHEDGAGRMTDLIVSCHEDULE_IN`
- function libraries: SyntaxEDI_Text, SyntaxEDI_Node, SyntaxEDI_Common

### `MM_BatchREsponse__2__Mail`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `MT_S4HC_BatchResponse`  ->  target: `XIMail30`

### `MM_BatchRequest__2__BatchResponse`
- package: SPS_S4HC  |  namespace: `http://syntax.com/cdm`
- source: `MT_S4HC_BatchRequest`  ->  target: `MT_S4HC_BatchResponse`
- function libraries: SyntaxS4HC_Json, SyntaxS4HC_Node, SyntaxS4HC_Lookup

### `MM_BatchResponseProductionOrder__2__ProductionOrderRelease`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/internal`
- source: `MT_S4HC_BatchResponse`  ->  target: `MT_S4HC_PostRequest`
- function libraries: Common, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_BatchResponseProductionOrder__2__ProductionOrderRelease`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `MT_S4HC_BatchResponse`  ->  target: `MT_S4HC_PostRequest`
- function libraries: Common, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_CO_EDI_DELIVERY_REQUEST_OUT__2__CO_EDI_DELIVERY_REQUEST_OUT_remap`
- package: SPS_S4HC  |  namespace: `http://syntax.com/cdm`
- source: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_sort_cdm`  ->  target: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_remap_cdm`

### `MM_CO_EDI_DELIVERY_REQUEST_OUT__2__ReceiverDetermination`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/customers`
- source: `SPS_S4HC_CO_EDI_DELIVERY_REQUEST_OUT`  ->  target: `Receivers`
- function libraries: SyntaxEDI_Common

### `MM_CO_EDI_DELIVERY_REQUEST_OUT__2__ReceiverDetermination_V1`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/customers`
- source: `SPS_S4HC_CO_EDI_DELIVERY_REQUEST_OUT`  ->  target: `Receivers`
- function libraries: SyntaxEDI_Common

### `MM_CO_EDI_DELIVERY_REQUEST_OUT__2__ReceiverDetermination_V2`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/customers`
- source: `SPS_S4HC_CO_EDI_DELIVERY_REQUEST_OUT`  ->  target: `Receivers`
- function libraries: SyntaxEDI_Common

### `MM_CO_EDI_DELIVERY_REQUEST_OUT_cdm__2__DESADV_V6`
- package: SPS_S4HC  |  namespace: `http://syntax.com/edi_s4hc`
- source: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_remap_cdm`  ->  target: `MT_DESADV`
- function libraries: SyntaxEDI_Common, SyntaxEDI_Node, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_CO_EDI_INVOICE_REQUEST_OUT_cdm__2__INVOICE`
- package: SPS_S4HC  |  namespace: `http://syntax.com/edi_s4hc`
- source: `MT_S4HC_CO_EDI_INVOICE_REQUEST_OUT_cdm`  ->  target: `MT_INVOICE`
- function libraries: SyntaxEDI_Common, SyntaxEDI_Date, SyntaxEDI_Node, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_CO_EDI_ORDER_REQUEST_OUT__2__CO_EDI_ORDER_REQUEST_OUT_cdm`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `SPS_S4HC_CO_EDI_ORDER_REQUEST_OUT`  ->  target: `MT_S4HC_CO_EDI_ORDER_REQUEST_OUT_cdm`
- function libraries: SyntaxEDI_Text, SyntaxEDI_Node

### `MM_CO_EDI_ORDER_REQUEST_OUT__2__MT_CO_EDI_ORDER_REQUEST_OUT_cdm`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `SPS_S4HC_CO_EDI_ORDER_REQUEST_OUT`  ->  target: `MT_S4HC_CO_EDI_ORDER_REQUEST_OUT_cdm`

### `MM_CO_EDI_SCHEDGAGRMT_OUT__2__DELFOR`
- package: SPS_S4HC  |  namespace: `http://syntax.com/edi_s4hc`
- source: `MT_S4HC_CO_SCHEDAGRMT_OUT_cdm`  ->  target: `MT_DELFOR`
- function libraries: SyntaxEDI_Common, SyntaxEDI_Node, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_CO_PPINT_MFGORD_EXE_REQ_OUT___2__A_ProductionOrderEntity_cdm`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/internal`
- source: `SPS_S4HC_CO_PPINT_MFGORD_EXE_REQ_OUT`  ->  target: `MT_S4HC_BatchRequest`
- function libraries: SyntaxEDI_Date

### `MM_CO_PPINT_MFGORD_EXE_REQ_OUT___2__CO_PPINT_MFGORD_EXE_REQ_OUT`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `SPS_S4HC_CO_PPINT_MFGORD_EXE_REQ_OUT`  ->  target: `SPS_S4HC_CO_PPINT_MFGORD_EXE_REQ_OUT`

### `MM_CO_PPINT_MFGORD_EXE_REQ_OUT___2__CO_PPINT_MFGORD_EXE_REQ_OUT`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/internal`
- source: `SPS_S4HC_CO_PPINT_MFGORD_EXE_REQ_OUT`  ->  target: `SPS_S4HC_CO_PPINT_MFGORD_EXE_REQ_OUT`

### `MM_DELFOR__2__DELFOR_Filter_SCC`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/customers`
- source: `MT_DELFOR`  ->  target: `MT_DELFOR`
- function libraries: SyntaxEDI_Node, SyntaxEDI_Boolean, SyntaxEDI_Text

### `MM_DELFOR__2__SCHEDGAGRMTDLIVSCHEDULE_IN`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/customers`
- source: `MT_DELFOR`  ->  target: `SPS_S4HC_SCHEDGAGRMTDLIVSCHEDULE_IN`
- function libraries: SyntaxEDI_Text, SyntaxEDI_Node

### `MM_DELFOR__2__SCHEDGAGRMTDLIVSCHEDULE_IN_V1`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/customers`
- source: `MT_DELFOR`  ->  target: `SPS_S4HC_SCHEDGAGRMTDLIVSCHEDULE_IN`
- function libraries: SyntaxEDI_Node

### `MM_DELFOR__2__SCHEDGAGRMTDLIVSCHEDULE_IN_V2`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/customers`
- source: `MT_DELFOR`  ->  target: `SPS_S4HC_SCHEDGAGRMTDLIVSCHEDULE_IN`
- function libraries: SyntaxEDI_Text, SyntaxEDI_Node

### `MM_DELFOR__2__SCHEDGAGRMTDLIVSCHEDULE_IN_V3`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/customers`
- source: `MT_DELFOR`  ->  target: `SPS_S4HC_SCHEDGAGRMTDLIVSCHEDULE_IN`
- function libraries: SyntaxEDI_Text, SyntaxEDI_Node

### `MM_DELFOR__2__SchedAgrmtDlivSchedule_In`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc`
- source: `MT_DELFOR`  ->  target: `SPS_S4HC_SCHEDGAGRMTDLIVSCHEDULE_IN`
- function libraries: SyntaxEDI_Node

### `MM_DELFOR__2__SchedAgrmtDlivSchedule_In`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/customers`
- source: `MT_DELFOR`  ->  target: `SPS_S4HC_SCHEDGAGRMTDLIVSCHEDULE_IN`
- function libraries: SyntaxEDI_Node

### `MM_DELIVERYREQUEST_IN__2__DELIVERYREQUEST_IN_test`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `SPS_S4HC_DELIVERYREQUEST_IN`  ->  target: `SPS_S4HC_DELIVERYREQUEST_IN`
- function libraries: SyntaxEDI_Date, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_DELIVERYREQUEST_IN__2__GoodsReceipt`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `SPS_S4HC_DELIVERYREQUEST_IN`  ->  target: `MT_S4HC_PostRequest`
- function libraries: SyntaxEDI_Date, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_DELIVERYREQUEST_IN__2__Goodsreceipt_cdm`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `MT_DESADV`  ->  target: `MT_S4HC_PostRequest`
- function libraries: SyntaxEDI_Common, SyntaxEDI_Date, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_DELIVERYREQUEST_IN__2__Goodsreceipt_cdm`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/internal`
- source: `SPS_S4HC_DELIVERYREQUEST_IN`  ->  target: `MT_S4HC_PostRequest`
- function libraries: SyntaxEDI_Date, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_DELIVERYREQUEST_IN__2__OutboundDelivery_cdm`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `MT_DESADV`  ->  target: `MT_S4HC_BatchRequest`
- function libraries: SyntaxEDI_Common, SyntaxEDI_Date, SyntaxEDI_Text, SyntaxEDI_Lookup
- USED_JARS: org_json

### `MM_DELIVERYREQUEST_IN__2__Putaway`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `SPS_S4HC_DELIVERYREQUEST_IN`  ->  target: `MT_S4HC_BatchRequest`
- function libraries: SyntaxEDI_Date, SyntaxEDI_Lookup, SyntaxEDI_Text

### `MM_DELIVERYREQUEST_IN__2__PutawayAllItems_cdm`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/internal`
- source: `SPS_S4HC_DELIVERYREQUEST_IN`  ->  target: `MT_S4HC_PostRequest`
- function libraries: SyntaxEDI_Date, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_DELIVERYREQUEST_IN__2__PutawayAllItems_cdm`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `MT_DESADV`  ->  target: `MT_S4HC_PostRequest`
- function libraries: SyntaxEDI_Text, SyntaxEDI_Date, SyntaxEDI_Common, SyntaxEDI_Lookup

### `MM_DELIVERYREQUEST_IN__2__Putaway_cdm`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `SPS_S4HC_DELIVERYREQUEST_IN`  ->  target: `MT_S4HC_PostRequest`
- function libraries: SyntaxEDI_Date, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_DELIVERYREQUEST_IN__2__Putaway_cdm`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/internal`
- source: `SPS_S4HC_DELIVERYREQUEST_IN`  ->  target: `MT_S4HC_PostRequest`
- function libraries: SyntaxEDI_Date, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_DELIVERYREQUEST_IN__2__Putaway_cdm_TDUtest`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/internal`
- source: `SPS_S4HC_DELIVERYREQUEST_IN`  ->  target: `MT_InternalActions`
- function libraries: SyntaxEDI_Date, SyntaxEDI_Lookup, SyntaxEDI_Text

### `MM_DESADV__2__DELIVERYREQUEST_IN`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `MT_DESADV`  ->  target: `SPS_S4HC_DELIVERYREQUEST_IN`
- function libraries: SyntaxEDI_Date, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_DESADV__2__DELIVERYREQUEST_IN_TEST`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `MT_DESADV`  ->  target: `SPS_S4HC_DELIVERYREQUEST_IN`
- function libraries: SyntaxEDI_Date, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_DESADV__2__DELIVERYREQUEST_IN_V1`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `MT_DESADV`  ->  target: `SPS_S4HC_DELIVERYREQUEST_IN`
- function libraries: SyntaxEDI_Date, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_DESADV__2__DELIVERYREQUEST_IN_V2`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `MT_DESADV`  ->  target: `SPS_S4HC_DELIVERYREQUEST_IN`
- function libraries: SyntaxEDI_Date, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_DESADV__2__DELIVERYREQUEST_IN_V2_Backup`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `MT_DESADV`  ->  target: `SPS_S4HC_DELIVERYREQUEST_IN`
- function libraries: SyntaxEDI_Date, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_DESADV__2__DELIVERYREQUEST_IN_V2_wo_HU`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `MT_DESADV`  ->  target: `SPS_S4HC_DELIVERYREQUEST_IN`
- function libraries: SyntaxEDI_Date, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_DESADV__2__DELIVERYREQUEST_IN_w_HU_ID`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `MT_DESADV`  ->  target: `SPS_S4HC_DELIVERYREQUEST_IN`
- function libraries: SyntaxEDI_Date, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_DESADV__2__DELIVERYREQUEST_IN_wo_HU`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `MT_DESADV`  ->  target: `SPS_S4HC_DELIVERYREQUEST_IN`
- function libraries: SyntaxEDI_Date, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_DESADV__2__DeliveryRequest_In`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc`
- source: `MT_DESADV`  ->  target: `SPS_S4HC_OP_DELIVERYREQUEST_IN`

### `MM_DESADV__2__DeliveryRequest_In`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `MT_DESADV`  ->  target: `SPS_S4HC_OP_DELIVERYREQUEST_IN`

### `MM_INVOICE_2_BDCREATESELFBILLINGREQUEST_IN`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/customers`
- source: `MT_INVOICE`  ->  target: `SPS_S4HC_BDCREATESELFBILLINGREQUEST_IN`
- function libraries: SyntaxEDI_Date

### `MM_INVOICE_2_BDCREATESELFBILLINGREQUEST_IN`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `MT_INVOICE`  ->  target: `SPS_S4HC_BDCREATESELFBILLINGREQUEST_IN`
- function libraries: SyntaxEDI_Date

### `MM_INVOICE_2_SELFBILLINGREQUEST_API_IN`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/customers`
- source: `MT_INVOICE`  ->  target: `SPS_BTP_SELFBILLINGREQUEST_API_IN`
- function libraries: SyntaxEDI_Date

### `MM_INVOICE__2__INVOICEREQUEST_IN`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `MT_INVOICE`  ->  target: `SPS_S4HC_INVOICEREQUEST_IN`
- function libraries: SyntaxEDI_Date

### `MM_INVOICE__2__INVOICEREQUEST_IN_ATTACHMENT`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `MT_INVOICE`  ->  target: `SPS_S4HC_INVOICEREQUEST_IN`
- function libraries: SyntaxEDI_Date, Common

### `MM_INVOICE__2__SELFBILLINGREQUEST_API_IN`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/customers`
- source: `MT_INVOICE`  ->  target: `SPS_BTP_SELFBILLINGREQUEST_API_IN`
- function libraries: SyntaxEDI_Date

### `MM_ORDRSP__2__SPS_S4HC_ORDERCONFIRMATIONREQUEST_IN`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `MT_ORDRSP`  ->  target: `SPS_S4HC_ORDERCONFIRMATIONREQUEST_IN`
- function libraries: SyntaxEDI_Date

### `MM_OutboundDeliveryBatch__2__BatchResponse`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `MT_S4HC_BatchRequest`  ->  target: `MT_S4HC_BatchResponse`
- function libraries: SyntaxS4HC_Node, SyntaxEDI_Text, SyntaxS4HC_Json, SyntaxEDI_Lookup, SyntaxS4HC_Lookup

### `MM_OutboundDelivery_Batch__2__BatchResponse`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `MT_S4HC_BatchRequest`  ->  target: `MT_S4HC_BatchResponse`
- function libraries: SyntaxS4HC_Node, SyntaxEDI_Text, SyntaxS4HC_Json, SyntaxEDI_Lookup, SyntaxS4HC_Lookup

### `MM_OutboundDelivery__2__Batch`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `MT_S4HC_BatchRequest`  ->  target: `MT_S4HC_BatchRequest`
- function libraries: SyntaxEDI_Common, SyntaxEDI_Date, SyntaxEDI_Text, SyntaxEDI_Lookup
- USED_JARS: SimpleNamespaceContext

### `MM_QALITY_2__ReceiverDetermination_Repeat`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `MT_QALITY`  ->  target: `Receivers`
- function libraries: Date, SyntaxEDI_Common, SyntaxEDI_Text, SyntaxEDI_Node, SyntaxEDI_Lookup

### `MM_QALITY_Repeat_2__ReceiverDetermination`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `MT_QALITY`  ->  target: `Receivers`
- function libraries: Date, SyntaxEDI_Common, SyntaxEDI_Text, SyntaxEDI_Node, SyntaxEDI_Lookup

### `MM_QALITY__2__A_InspectionResultEntity_cdm`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `MT_QALITY`  ->  target: `MT_S4HC_BatchRequest`
- function libraries: SyntaxEDI_Text, SyntaxEDI_Node, SyntaxEDI_Lookup

### `MM_QALITY__2__A_InspectionResultEntity_cdm_filter`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `MT_QALITY`  ->  target: `MT_S4HC_BatchRequest`
- function libraries: SyntaxEDI_Text, SyntaxEDI_Node, SyntaxEDI_Lookup

### `MM_QALITY__2__A_InspectionResultEntity_wo_ResultStatusField_cdm`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `MT_QALITY`  ->  target: `MT_S4HC_BatchRequest`
- function libraries: SyntaxEDI_Text, SyntaxEDI_Node, SyntaxEDI_Lookup

### `MM_QALITY__2__File`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `MT_QALITY`  ->  target: `MT_QALITY`
- function libraries: Date, SyntaxEDI_Common, SyntaxEDI_Text, SyntaxEDI_Node, SyntaxEDI_Lookup

### `MM_QALITY__2__File_Error`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `MT_QALITY`  ->  target: `MT_S4HC_BatchResponse`
- function libraries: Date, SyntaxEDI_Common, SyntaxEDI_Text, SyntaxEDI_Node, SyntaxEDI_Lookup

### `MM_QALITY__2__File_Error_2`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `MT_QALITY`  ->  target: `MT_S4HC_BatchResponse`
- function libraries: Date, SyntaxEDI_Common, SyntaxEDI_Text, SyntaxEDI_Node, SyntaxEDI_Lookup

### `MM_QALITY__2__File_Repeat`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `MT_QALITY`  ->  target: `MT_QALITY`
- function libraries: Date, SyntaxEDI_Common, SyntaxEDI_Text, SyntaxEDI_Node, SyntaxEDI_Lookup

### `MM_QALITY__2__ReceiverDetermination`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `MT_QALITY`  ->  target: `Receivers`
- function libraries: Date, SyntaxEDI_Common, SyntaxEDI_Text, SyntaxEDI_Node, SyntaxEDI_Lookup

### `MM_QALITY__2__ReceiverDetermination_Repeat`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `MT_QALITY`  ->  target: `Receivers`
- function libraries: Date, SyntaxEDI_Common, SyntaxEDI_Text, SyntaxEDI_Node, SyntaxEDI_Lookup

### `MM_QALITY__2__ReceiverDetermination_Repeat_Backup`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `MT_QALITY`  ->  target: `Receivers`
- function libraries: Date, SyntaxEDI_Common, SyntaxEDI_Text, SyntaxEDI_Node, SyntaxEDI_Lookup

### `MM_QALITY__2__ReceiverDetermination_Repeat_Test`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `MT_QALITY`  ->  target: `Receivers`
- function libraries: Date, SyntaxEDI_Common, SyntaxEDI_Text, SyntaxEDI_Node, SyntaxEDI_Lookup

### `MM_QALITY__2__ReceiverDetermination_Repeat_Test2`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `MT_QALITY`  ->  target: `Receivers`
- function libraries: Date, SyntaxEDI_Common, SyntaxEDI_Text, SyntaxEDI_Node, SyntaxEDI_Lookup

### `MM_QALITY__2__batchParts_A_InspectionResultEntityPOST_cdm`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `MT_QALITY`  ->  target: `MT_S4HC_batchParts_A_InspectionResultEntity_POST_cdm`
- function libraries: SyntaxEDI_Text, SyntaxEDI_Node, SyntaxEDI_Lookup

### `MM_S4HC_CO_EDI_ORDER_REQUEST_OUT__2__MT_S4HC_CO_EDI_ORDER_REQUEST_OUT_cdm`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `SPS_S4HC_CO_EDI_ORDER_REQUEST_OUT`  ->  target: `MT_S4HC_CO_EDI_ORDER_REQUEST_OUT_cdm`

### `MM_SELFBILLING_RESPONSE__2__STATUS_RESPONSE`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/customers`
- source: `SPS_BTP_SELFBILLINGREQUEST_API_IN`  ->  target: `SPS_BTP_SELFBILLINGREQUEST_API_IN`

### `MM_SPS_S4HC_CO_EDI_DELIVERY_REQUEST_OUT__2__S4HC_CO_EDI_DELIVERY_REQUEST_OUT_cdm`
- package: SPS_S4HC  |  namespace: `http://sps.shop_/s4hc`
- source: `SPS_S4HC_CO_EDI_DELIVERY_REQUEST_OUT`  ->  target: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_cdm`
- function libraries: SyntaxEDI_Lookup, SyntaxEDI_Node, SyntaxEDI_Text

### `MM_SPS_S4HC_CO_EDI_DELIVERY_REQUEST_OUT__2__S4HC_CO_EDI_DELIVERY_REQUEST_OUT_cdm`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc`
- source: `SPS_S4HC_CO_EDI_DELIVERY_REQUEST_OUT`  ->  target: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_cdm`
- function libraries: SyntaxEDI_Lookup, SyntaxEDI_Node, SyntaxEDI_Text

### `MM_SPS_S4HC_CO_EDI_DELIVERY_REQUEST_OUT__2__S4HC_CO_EDI_DELIVERY_REQUEST_OUT_cdm`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/customers`
- source: `SPS_S4HC_CO_EDI_DELIVERY_REQUEST_OUT`  ->  target: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_cdm`
- function libraries: SyntaxEDI_Lookup, SyntaxEDI_Node, SyntaxEDI_Text

### `MM_SPS_S4HC_CO_EDI_DELIVERY_REQUEST_OUT__2__S4HC_CO_EDI_DELIVERY_REQUEST_OUT_cdm`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `SPS_S4HC_CO_EDI_DELIVERY_REQUEST_OUT`  ->  target: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_cdm`
- function libraries: SyntaxEDI_Lookup, SyntaxEDI_Node, SyntaxEDI_Text

### `MM_SPS_S4HC_CO_EDI_DELIVERY_REQUEST_OUT__2__S4HC_CO_EDI_DELIVERY_REQUEST_OUT_cdm_2`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/customers`
- source: `SPS_S4HC_CO_EDI_DELIVERY_REQUEST_OUT`  ->  target: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_cdm`
- function libraries: SyntaxEDI_Lookup, SyntaxEDI_Node, SyntaxEDI_Text

### `MM_SPS_S4HC_CO_EDI_DELIVERY_REQUEST_OUT__2__S4HC_CO_EDI_DELIVERY_REQUEST_OUT_cdm_3`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/customers`
- source: `SPS_S4HC_CO_EDI_DELIVERY_REQUEST_OUT`  ->  target: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_cdm`
- function libraries: SyntaxEDI_Lookup, SyntaxEDI_Node, SyntaxEDI_Text

### `MM_SPS_S4HC_CO_EDI_DELIVERY_REQUEST_OUT__2__S4HC_CO_EDI_DELIVERY_REQUEST_OUT_cdm_4`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/customers`
- source: `SPS_S4HC_CO_EDI_DELIVERY_REQUEST_OUT`  ->  target: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_cdm`
- function libraries: SyntaxEDI_Lookup, SyntaxEDI_Node, SyntaxEDI_Text

### `MM_SPS_S4HC_CO_EDI_DELIVERY_REQUEST_OUT__2__S4HC_CO_EDI_DELIVERY_REQUEST_OUT_cdm_5`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/customers`
- source: `SPS_S4HC_CO_EDI_DELIVERY_REQUEST_OUT`  ->  target: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_cdm`
- function libraries: SyntaxEDI_Lookup, SyntaxEDI_Node, SyntaxEDI_Text

### `MM_SPS_S4HC_CO_EDI_DELIVERY_REQUEST_OUT__2__S4HC_CO_EDI_DELIVERY_REQUEST_OUT_cdm_6`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/customers`
- source: `SPS_S4HC_CO_EDI_DELIVERY_REQUEST_OUT`  ->  target: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_cdm`
- function libraries: SyntaxEDI_Lookup, SyntaxEDI_Node, SyntaxEDI_Text

### `MM_SPS_S4HC_CO_EDI_DELIVERY_REQUEST_OUT__2__S4HC_CO_EDI_DELIVERY_REQUEST_OUT_cdm_test`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/customers`
- source: `SPS_S4HC_CO_EDI_DELIVERY_REQUEST_OUT`  ->  target: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_cdm`
- function libraries: SyntaxEDI_Lookup, SyntaxEDI_Node, SyntaxEDI_Text

### `MM_SPS_S4HC_CO_EDI_DELIVERY_REQUEST_OUT__2__SPS_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_cdm`
- package: SPS_S4HC  |  namespace: `http://sps.shop_/s4hc`
- source: `SPS_S4HC_CO_EDI_DELIVERY_REQUEST_OUT`  ->  target: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_cdm`

### `MM_SPS_S4HC_CO_EDI_EDI_SCHEDAGTMT_OUT__2__MM_SPS_S4HC_CO_EDI_EDI_SCHEDAGTMT_OUT_cdm`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `SPS_S4HC_CO_EDI_SCHEDGAGRMT_OUT`  ->  target: `MT_S4HC_CO_SCHEDAGRMT_OUT_cdm`
- function libraries: SyntaxEDI_Text, SyntaxEDI_Lookup, SyntaxEDI_Node

### `MM_SPS_S4HC_CO_EDI_EDI_SCHEDAGTMT_OUT__2__MM_SPS_S4HC_CO_EDI_EDI_SCHEDAGTMT_OUT_cdm`
- package: SPS_S4HC  |  namespace: `http://sps.shop_/s4hc`
- source: `SPS_S4HC_CO_EDI_SCHEDGAGRMT_OUT`  ->  target: `MT_S4HC_CO_SCHEDAGRMT_OUT_cdm`

### `MM_SPS_S4HC_CO_EDI_EDI_SCHEDAGTMT_OUT__2__MM_SPS_S4HC_CO_EDI_EDI_SCHEDAGTMT_OUT_cdm`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc`
- source: `SPS_S4HC_CO_EDI_SCHEDGAGRMT_OUT`  ->  target: `MT_S4HC_CO_SCHEDAGRMT_OUT_cdm`

### `MM_SPS_S4HC_CO_EDI_EDI_SCHEDAGTMT_OUT__2__ReceiverDetermination`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/suppliers`
- source: `SPS_S4HC_CO_EDI_SCHEDGAGRMT_OUT`  ->  target: `Receivers`
- function libraries: SyntaxEDI_Common, SyntaxEDI_Text

### `MM_SPS_S4HC_CO_EDI_INVOICE_REQUEST_OUT__2__S4HC_CO_EDI_INVOICE_REQUEST_ARCHIVE_IN`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/customers`
- source: `SPS_S4HC_CO_EDI_INVOICE_REQUEST_OUT`  ->  target: `SPS_S4HC_CO_EDI_INVOICE_REQUEST_OUT`
- function libraries: Common

### `MM_SPS_S4HC_CO_EDI_INVOICE_REQUEST_OUT__2__S4HC_CO_EDI_INVOICE_REQUEST_OUT_cdm`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/customers`
- source: `SPS_S4HC_CO_EDI_INVOICE_REQUEST_OUT`  ->  target: `MT_S4HC_CO_EDI_INVOICE_REQUEST_OUT_cdm`
- function libraries: Common, SyntaxEDI_Date, SyntaxEDI_Lookup, SyntaxEDI_Text, SyntaxEDI_Node

### `MM_SPS_S4HC_Transport_API_OUT__2__S4HC_CO_EDI_DELIVERY_REQUEST_OUT_cdm`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/customers`
- source: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_Transport_API`  ->  target: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_cdm`
- function libraries: SyntaxEDI_Date, SyntaxEDI_Node, SyntaxEDI_Text, SyntaxEDI_Lookup, SyntaxS4HC_Node

### `MM_SPS_S4HC_Transport_API_OUT__2__S4HC_CO_EDI_DELIVERY_REQUEST_OUT_cdm_V2`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/customers`
- source: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_Transport_API`  ->  target: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_cdm`

### `MM_SelfBilling_Response__2__STATUS_RESP`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/customers`
- source: `SPS_BTP_SELFBILLINGREQUEST_API_IN`  ->  target: `SPS_BTP_SELFBILLINGREQUEST_API_IN`

### `MM_Transport_API_OUT__2__ReceiverDetermination_V2`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/customers`
- source: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_Transport_API`  ->  target: `Receivers`
- function libraries: SyntaxEDI_Common, SyntaxEDI_Boolean

### `MM_VDA490500__2__SCHEDAGRMTDLIVSCHEDULE_IN`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/customers`
- source: `MT_VDA490500`  ->  target: `SPS_S4HC_SCHEDGAGRMTDLIVSCHEDULE_IN`
- function libraries: SyntaxEDI_Boolean, SyntaxEDI_Arithmetic, UDFArithmeticsPool, SyntaxEDI_Text

### `MT_SelfBilling_Response__2__STATUS_SYSTAT01`
- package: SPS_S4HC  |  namespace: `http://sps.shop/s4hc/customers`
- source: `MT_SelfBilling_Response`  ->  target: `MT_SelfBilling_Response`

### `ASC830_004010_Split__2__ASC830_004010_Split_filter`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi_ansi`
- source: `MT_ASC830_004010_split`  ->  target: `MT_ASC830_004010_split`
- function libraries: SyntaxEDI_Node

### `ASC830_004010__2__ASC830_004010`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi_ansi`
- source: `MT_ASC830_004010`  ->  target: `MT_ASC830_004010`

### `MM_ANSI_Message__2__ASC830_004010`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi_ansi`
- source: `MT_ANSI_Message`  ->  target: `MT_ASC830_004010`

### `MM_ANSI_Message__2__ASC830_004010_Split_by_Lin`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi_ansi`
- source: `MT_ANSI_Message`  ->  target: `MT_ASC830_004010_split`
- function libraries: SyntaxEDI_Node

### `MM_ANSI_Message__2__ASC830_004010_split`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi_ansi`
- source: `MT_ANSI_Message`  ->  target: `MT_ASC830_004010_split`
- function libraries: SyntaxEDI_Node

### `MM_ANSI_Message__2__ASC862_004010_Split_by_Lin`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi_ansi`
- source: `MT_ANSI_Message`  ->  target: `MT_ASC862_004010_split`
- function libraries: SyntaxEDI_Node

### `MM_ANSI_Message__2__ASC862_004010_Split_by_Lin_test`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi_ansi`
- source: `MT_ASC862_004010`  ->  target: `MT_ASC862_004010_split`
- function libraries: SyntaxEDI_Node

### `MM_ASC830_004010_Split__2__ASC830_004010_Split_filter`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi_ansi`
- source: `MT_ASC830_004010_split`  ->  target: `MT_ASC830_004010_split`
- function libraries: SyntaxEDI_Node

### `MM_ASC830_004010__2__ASC830_004010`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi_ansi`
- source: `MT_ASC830_004010`  ->  target: `MT_ASC830_004010`

### `MM_ASC862_004010_Split__2__ASC862_004010_Split_filter`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi_ansi`
- source: `MT_ASC862_004010_split`  ->  target: `MT_ASC862_004010_split`
- function libraries: SyntaxEDI_Node

### `MM_CO_EDI_DELIVERY_REQUEST_OUT__2__CO_EDI_DELIVERY_REQUEST_OUT_prepare`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi`
- source: `SPS_S4HC_CO_EDI_DELIVERY_REQUEST_OUT`  ->  target: `S4HC_CO_EDI_DELIVERY_REQUEST_OUT_sort`
- function libraries: SyntaxEDI_Node

### `MM_CO_EDI_DELIVERY_REQUEST_OUT__2__CO_EDI_DELIVERY_REQUEST_OUT_remap`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi`
- source: `S4HC_CO_EDI_DELIVERY_REQUEST_OUT_sort`  ->  target: `S4HC_CO_EDI_DELIVERY_REQUEST_OUT_remap`

### `MM_CO_EDI_DELIVERY_REQUEST_OUT__2__DESADV`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi`
- source: `S4HC_CO_EDI_DELIVERY_REQUEST_OUT_remap`  ->  target: `MT_DESADV`
- function libraries: SyntaxEDI_Node, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_CO_EDI_DELIVERY_REQUEST_OUT_cdm__2__DESADV`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi`
- source: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_remap_cdm`  ->  target: `MT_DESADV`
- function libraries: SyntaxEDI_Node, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_CO_EDI_SCHEDGAGRMT_OUT__2__DELFOR`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi`
- source: `S4HC_CO_EDI_SCHEDGAGRMT_OUT`  ->  target: `MT_DELFOR`
- function libraries: SyntaxEDI_Node, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_DELFOR04A_Split__2__DELFOR04A_Split`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi`
- source: `ZDELFOR04A`  ->  target: `ZDELFOR04A`

### `MM_DELFOR04A_Split__2__DELFOR04A_Split_filter`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi`
- source: `MT_DELFOR_split`  ->  target: `MT_DELFOR_split`

### `MM_DELFOR04A__2__DELFOR04A`
- package: SYNTAX_EDI  |  namespace: `http://syntax/edi`
- source: `DELFOR04A`  ->  target: `MT_DELFOR04A`

### `MM_DELFOR04A__2__DELFOR04A_Split`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi`
- source: `DELFOR04A`  ->  target: `ZDELFOR04A`

### `MM_DELFOR04A__2__DELFOR04A_Split_By_Lin`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi`
- source: `DELFOR04A`  ->  target: `ZDELFOR04A`

### `MM_DELFOR04A__2__DELFOR04A_Split_backup`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi`
- source: `DELFOR04A`  ->  target: `ZDELFOR04A`

### `MM_DELFOR96A_split__2__DELFOR_split`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi`
- source: `MT_DELFOR_96A_split`  ->  target: `MT_DELFOR_split`

### `MM_DELFOR97A_split__2__DELFOR_split`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi`
- source: `MT_DELFOR_97A_split`  ->  target: `MT_DELFOR_split`

### `MM_DELFOR_Split__2__DELFOR_Split_filter`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi`
- source: `MT_DELFOR_split`  ->  target: `MT_DELFOR_split`
- function libraries: SyntaxEDI_Common

### `MM_DELFOR_Split_filter__2__DELFOR_Split_group`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi`
- source: `MT_DELFOR_split`  ->  target: `MT_DELFOR_split`
- function libraries: SyntaxEDI_Common

### `MM_DELFOR_filter__2_DELFOR_group`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi`
- source: `MT_DELFOR`  ->  target: `MT_DELFOR`

### `MM_DESADV_Split__2__DESADV_Split_filter`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi`
- source: `MT_DESADV_split`  ->  target: `MT_DESADV_split`

### `MM_DESADV__2__DESADV_sort_prepare`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi`
- source: `MT_DESADV`  ->  target: `MT_DESADV_sort`

### `MM_DESADV__2__DESADV_split`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi`
- source: `MT_DESADV`  ->  target: `MT_DESADV_split`

### `MM_DESADV_sort__2__DESADV_batchsplit`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi`
- source: `MT_DESADV_sort`  ->  target: `MT_DESADV_sort`
- function libraries: SyntaxEDI_Node

### `MM_DESADV_sort__2__DESADV_remap`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi`
- source: `MT_DESADV_sort`  ->  target: `MT_DESADV`

### `MM_DESADV_split__2__DESADV_filter`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi`
- source: `MT_DESADV_split`  ->  target: `MT_DESADV_split`
- function libraries: SyntaxEDI_Node

### `MM_DESADV_split__2__DESADV_split`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi`
- source: `MT_DESADV_split`  ->  target: `MT_DESADV_split`
- function libraries: SyntaxEDI_Node

### `MM_EdifactMessage__2__INVOIC07A`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi_versions`
- source: `MT_EdifactMessage`  ->  target: `MT_INVOIC7A`
- function libraries: SyntaxEDI_Node

### `MM_EdifactMessage__2__INVOIC96A`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi_versions`
- source: `MT_EdifactMessage`  ->  target: `MT_INVOIC96A`
- function libraries: SyntaxEDI_Node

### `MM_EditfactMEssage__2__DELFOR04A_Split`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi`
- source: `MT_EdifactMessage`  ->  target: `ZDELFOR04A`

### `MM_EditfactMEssage__2__DELFOR04A_Split_by_Lin`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi`
- source: `MT_EdifactMessage`  ->  target: `MT_DELFOR_split`
- function libraries: Node_Functions

### `MM_EditfactMessage__2__DELFOR_96A_Split_by_Lin`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi`
- source: `MT_EdifactMessage`  ->  target: `MT_DELFOR_96A_split`
- function libraries: SyntaxEDI_Node

### `MM_EditfactMessage__2__DELFOR_97A_Split_by_Lin`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi`
- source: `MT_EdifactMessage`  ->  target: `MT_DELFOR_97A_split`
- function libraries: SyntaxEDI_Node

### `MM_EditfactMessage__2__DELFOR_Split_by_Lin`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi`
- source: `MT_EdifactMessage`  ->  target: `MT_DELFOR_split`
- function libraries: SyntaxEDI_Node

### `MM_EditfactMessage__2__DESADV`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi`
- source: `MT_EdifactMessage`  ->  target: `MT_DESADV`
- function libraries: SyntaxEDI_Node

### `MM_EditfactMessage__2__DESADV_Split_by_Lin`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi`
- source: `MT_EdifactMessage`  ->  target: `MT_DESADV_split`
- function libraries: SyntaxEDI_Node

### `MM_EditfactMessage__2__DESADV_test`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi/test`
- source: `MT_EdifactMessage`  ->  target: `MT_DESADV`

### `MM_EditfactMessage__2__INVOICE`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi`
- source: `MT_EdifactMessage`  ->  target: `MT_INVOICE`

### `MM_EditfactMessage__2__INVOICE_split`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi`
- source: `MT_EdifactMessage`  ->  target: `MT_INVOICE_split`
- function libraries: SyntaxEDI_Node

### `MM_EditfactMessage__2__INVOIC_split`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi`
- source: `MT_EdifactMessage`  ->  target: `MT_INVOICE_split`
- function libraries: SyntaxEDI_Node

### `MM_EditfactMessage__2__ORDCHG`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi`
- source: `MT_EdifactMessage`  ->  target: `MT_ORDCHG96A`

### `MM_EditfactMessage__2__ORDERS`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi`
- source: `MT_EdifactMessage`  ->  target: `MT_ORDERS`
- function libraries: SyntaxEDI_Node

### `MM_EditfactMessage__2__ORDRSP`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi`
- source: `MT_EdifactMessage`  ->  target: `MT_ORDRSP`

### `MM_EditfactMessage__2__ORDRSP96A`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi`
- source: `MT_EdifactMessage`  ->  target: `MT_ORDRSP96A`
- function libraries: SyntaxEDI_Node

### `MM_EditfactMessage__2__ORDRSP96A`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi_versions`
- source: `MT_EdifactMessage`  ->  target: `MT_ORDRSP96A`
- function libraries: SyntaxEDI_Node

### `MM_EditfactMessage__2__ORDRSP96A_split`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi`
- source: `MT_EdifactMessage`  ->  target: `MT_ORDRSP96A_split`
- function libraries: SyntaxEDI_Node

### `MM_EditfactMessage__2__QALITY`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi`
- source: `MT_EdifactMessage`  ->  target: `MT_QALITY`
- function libraries: SyntaxEDI_Node

### `MM_EditfactMessage__2__QALITY_split`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi`
- source: `MT_EdifactMessage`  ->  target: `MT_QALITY_split`
- function libraries: SyntaxEDI_Node

### `MM_INVOIC96A__2__INVOIC`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi_versions`
- source: `MT_INVOIC96A`  ->  target: `MT_INVOICE`

### `MM_INVOIC96A__2__INVOICE`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi_versions`
- source: `MT_INVOIC96A`  ->  target: `MT_INVOICE`

### `MM_INVOICE7A__2__INVOICE`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi_versions`
- source: `MT_INVOIC7A`  ->  target: `MT_INVOICE`

### `MM_INVOICE_7A__2__INVOICE`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi_versions`
- source: `MT_INVOICE_7A`  ->  target: `MT_INVOICE`

### `MM_INVOICE__2__INVOICE_split`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi`
- source: `MT_INVOICE`  ->  target: `MT_INVOICE_split`

### `MM_INVOICE_split__2__INVOICE_split`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi`
- source: `MT_INVOICE_split`  ->  target: `MT_INVOICE_split`
- function libraries: Common

### `MM_ORDERS__2__ORDERS96A`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi_versions`
- source: `MT_ORDERS`  ->  target: `MT_ORDERS96A`

### `MM_ORDRSP96A__2__ORDRSP`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi_versions`
- source: `MT_ORDRSP96A`  ->  target: `MT_ORDRSP`
- function libraries: SyntaxEDI_Date

### `MM_ORDRSP__2__ORDRSP_split`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi`
- source: `MT_ORDRSP`  ->  target: `MT_ORDRSP_split`

### `MM_QALITY_split__2__QALITY_filter`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi`
- source: `MT_QALITY_split`  ->  target: `MT_QALITY_split`

### `MM_QALITY_split__2__QALITY_split`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi`
- source: `MT_QALITY_split`  ->  target: `MT_QALITY_split`

### `MM_TEST`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi/test`
- source: `MT_DESADV`  ->  target: `MT_EdifactMessage`

### `MM_VDA490500_prepare__2__VDA490500_remap`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi_vda`
- source: `MT_VDA490500_prepare`  ->  target: `MT_VDA490500_split`
- function libraries: SyntaxEDI_Common, SyntaxEDI_Text

### `MM_VDA490500_split__2__VDA490500_filter`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi_vda`
- source: `MT_VDA490500_split`  ->  target: `MT_VDA490500_split`
- function libraries: SyntaxEDI_Common

### `MM_VDA490500_split__2__VDA490500_prepare`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi_vda`
- source: `MT_VDA490500_split`  ->  target: `MT_VDA490500_prepare`
- function libraries: SyntaxEDI_Text, SyntaxEDI_Common

### `MM_VDA491600_split__2__VDA491600_filter`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi_vda`
- source: `MT_VDA491600_split`  ->  target: `MT_VDA491600_split`
- function libraries: SyntaxEDI_Common

### `MM_VDA_Message__2__VDA490500_Split_by_S512`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi_vda`
- source: `MT_VDA_Message`  ->  target: `MT_VDA490500_split`
- function libraries: SyntaxEDI_Node, SyntaxEDI_Common

### `MM_VDA_Message__2__VDA490500_test`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi_vda`
- source: `MT_VDA_Message`  ->  target: `MT_VDA490500_split`
- function libraries: SyntaxEDI_Node

### `MM_VDA_Message__2__VDA491600_Split_by_S662`
- package: SYNTAX_EDI  |  namespace: `http://syntax.com/edi_vda`
- source: `MT_VDA_Message`  ->  target: `MT_VDA491600_split`
- function libraries: SyntaxEDI_Node, SyntaxEDI_Common

### `ASC856_004010_cdm__2__ASC856_004010`
- package: SYNTAX_EDI_S4HC  |  namespace: `http://syntax.com/edi_ansi_s4hc`
- source: `MT_ASC856_004010_HL_Grouping`  ->  target: `MT_ASC856_004010`
- function libraries: SyntaxEDI_Common, SyntaxEDI_Node, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_ASC810_004010_cdm__2__ASC810_004010`
- package: SYNTAX_EDI_S4HC  |  namespace: `http://syntax.com/edi_ansi_s4hc`
- source: `MT_S4HC_CO_EDI_INVOICE_REQUEST_OUT_cdm`  ->  target: `MT_ASC810_004010`
- function libraries: SyntaxEDI_Node, SyntaxEDI_Common, SyntaxEDI_Lookup, SyntaxEDI_Text

### `MM_ASC856_004010_cdm__2__ASC856_004010`
- package: SYNTAX_EDI_S4HC  |  namespace: `http://syntax.com/edi_ansi_s4hc`
- source: `MT_ASC856_004010_HL_Grouping`  ->  target: `MT_ASC856_004010`
- function libraries: SyntaxEDI_Common, SyntaxEDI_Node, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_CO_EDI_DELIVERY_REQUEST_OUT__2__CO_EDI_DELIVERY_REQUEST_OUT_prepare`
- package: SYNTAX_EDI_S4HC  |  namespace: `http://syntax.com/edi_s4hc`
- source: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_cdm`  ->  target: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_sort_cdm`
- function libraries: SyntaxS4HC_Node

### `MM_CO_EDI_DELIVERY_REQUEST_OUT__2__CO_EDI_DELIVERY_REQUEST_OUT_remap`
- package: SYNTAX_EDI_S4HC  |  namespace: `http://syntax.com/edi_s4hc`
- source: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_sort_cdm`  ->  target: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_remap_cdm`

### `MM_CO_EDI_DELIVERY_REQUEST_OUT_cdm__2__ASC856_004010`
- package: SYNTAX_EDI_S4HC  |  namespace: `http://syntax.com/edi_ansi_s4hc`
- source: `MT_ASC856_004010_HL_Grouping`  ->  target: `MT_ASC856_004010`
- function libraries: SyntaxEDI_Common, SyntaxEDI_Node, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_CO_EDI_DELIVERY_REQUEST_OUT_cdm__2__ASC856_004010`
- package: SYNTAX_EDI_S4HC  |  namespace: `http://syntax.com/edi_s4hc`
- source: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_remap_cdm`  ->  target: `MT_ASC856_004010`
- function libraries: SyntaxEDI_Common, SyntaxEDI_Node, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_CO_EDI_DELIVERY_REQUEST_OUT_cdm__2__ASC856_004010_TransportBased`
- package: SYNTAX_EDI_S4HC  |  namespace: `http://syntax.com/edi_ansi_s4hc`
- source: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_remap_cdm`  ->  target: `MT_ASC856_004010_HL_Grouping`
- function libraries: SyntaxEDI_Common, SyntaxEDI_Node, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_CO_EDI_DELIVERY_REQUEST_OUT_cdm__2__ASC856_004010_TransportBased_cdm`
- package: SYNTAX_EDI_S4HC  |  namespace: `http://syntax.com/edi_ansi_s4hc`
- source: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_remap_cdm`  ->  target: `MT_ASC856_004010_HL_Grouping`
- function libraries: SyntaxEDI_Common, SyntaxEDI_Node, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_CO_EDI_DELIVERY_REQUEST_OUT_cdm__2__ASC856_004010_cdm`
- package: SYNTAX_EDI_S4HC  |  namespace: `http://syntax.com/edi_ansi_s4hc`
- source: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_remap_cdm`  ->  target: `MT_ASC856_004010_HL_Grouping`
- function libraries: SyntaxEDI_Common, SyntaxEDI_Node, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_CO_EDI_DELIVERY_REQUEST_OUT_cdm__2__ASC856_004010_cdm_V2`
- package: SYNTAX_EDI_S4HC  |  namespace: `http://syntax.com/edi_ansi_s4hc`
- source: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_remap_cdm`  ->  target: `MT_ASC856_004010_HL_Grouping`
- function libraries: SyntaxEDI_Common, SyntaxEDI_Node, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_CO_EDI_DELIVERY_REQUEST_OUT_cdm__2__DESADV`
- package: SYNTAX_EDI_S4HC  |  namespace: `http://syntax.com/edi_s4hc`
- source: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_remap_cdm`  ->  target: `MT_DESADV`
- function libraries: SyntaxEDI_Common, SyntaxEDI_Node, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_CO_EDI_DELIVERY_REQUEST_OUT_cdm__2__DESADV_NO_HU`
- package: SYNTAX_EDI_S4HC  |  namespace: `http://syntax.com/edi_s4hc`
- source: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_remap_cdm`  ->  target: `MT_DESADV`
- function libraries: SyntaxEDI_Common, SyntaxEDI_Node, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_CO_EDI_DELIVERY_REQUEST_OUT_cdm__2__DESADV_TransportBased`
- package: SYNTAX_EDI_S4HC  |  namespace: `http://syntax.com/edi_s4hc`
- source: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_remap_cdm`  ->  target: `MT_DESADV`
- function libraries: SyntaxEDI_Common, SyntaxEDI_Node, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_CO_EDI_DELIVERY_REQUEST_OUT_cdm__2__DESADV_V2`
- package: SYNTAX_EDI_S4HC  |  namespace: `http://syntax.com/edi_s4hc`
- source: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_remap_cdm`  ->  target: `MT_DESADV`
- function libraries: SyntaxEDI_Common, SyntaxEDI_Node, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_CO_EDI_DELIVERY_REQUEST_OUT_cdm__2__DESADV_V3`
- package: SYNTAX_EDI_S4HC  |  namespace: `http://syntax.com/edi_s4hc`
- source: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_remap_cdm`  ->  target: `MT_DESADV`
- function libraries: SyntaxEDI_Common, SyntaxEDI_Node, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_CO_EDI_DELIVERY_REQUEST_OUT_cdm__2__DESADV_V4`
- package: SYNTAX_EDI_S4HC  |  namespace: `http://syntax.com/edi_s4hc`
- source: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_remap_cdm`  ->  target: `MT_DESADV`
- function libraries: SyntaxEDI_Common, SyntaxEDI_Node, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_CO_EDI_DELIVERY_REQUEST_OUT_cdm__2__DESADV_V5`
- package: SYNTAX_EDI_S4HC  |  namespace: `http://syntax.com/edi_s4hc`
- source: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_remap_cdm`  ->  target: `MT_DESADV`
- function libraries: SyntaxEDI_Common, SyntaxEDI_Node, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_CO_EDI_DELIVERY_REQUEST_OUT_cdm__2__DESADV_V6`
- package: SYNTAX_EDI_S4HC  |  namespace: `http://syntax.com/edi_s4hc`
- source: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_remap_cdm`  ->  target: `MT_DESADV`
- function libraries: SyntaxEDI_Common, SyntaxEDI_Node, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_CO_EDI_DELIVERY_REQUEST_OUT_cdm__2__DESADV_V6_TB`
- package: SYNTAX_EDI_S4HC  |  namespace: `http://syntax.com/edi_s4hc`
- source: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_remap_cdm`  ->  target: `MT_DESADV`
- function libraries: SyntaxEDI_Common, SyntaxEDI_Node, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_CO_EDI_DELIVERY_REQUEST_OUT_cdm__2__DESADV_V6_with_Grouping`
- package: SYNTAX_EDI_S4HC  |  namespace: `http://syntax.com/edi_s4hc`
- source: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_remap_cdm`  ->  target: `MT_DESADV`
- function libraries: SyntaxEDI_Common, SyntaxEDI_Node, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_CO_EDI_DELIVERY_REQUEST_OUT_cdm__2__DESADV_V7`
- package: SYNTAX_EDI_S4HC  |  namespace: `http://syntax.com/edi_s4hc`
- source: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_remap_cdm`  ->  target: `MT_DESADV`
- function libraries: SyntaxEDI_Common, SyntaxEDI_Node, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_CO_EDI_DELIVERY_REQUEST_OUT_cdm__2__VDA491300`
- package: SYNTAX_EDI_S4HC  |  namespace: `http://syntax.com/edi_vda_s4hc`
- source: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_remap_cdm`  ->  target: `MT_VDA491300`
- function libraries: SyntaxEDI_Common, SyntaxEDI_Node, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_CO_EDI_INVOICE_REQUEST_OUT_cdm__2__ASC810_004010`
- package: SYNTAX_EDI_S4HC  |  namespace: `http://syntax.com/edi_ansi_s4hc`
- source: `MT_S4HC_CO_EDI_INVOICE_REQUEST_OUT_cdm`  ->  target: `MT_ASC810_004010`
- function libraries: SyntaxEDI_Node, SyntaxEDI_Common, SyntaxEDI_Lookup, SyntaxEDI_Text

### `MM_CO_EDI_INVOICE_REQUEST_OUT_cdm__2__INVOICE`
- package: SYNTAX_EDI_S4HC  |  namespace: `http://syntax.com/edi_s4hc`
- source: `MT_S4HC_CO_EDI_INVOICE_REQUEST_OUT_cdm`  ->  target: `MT_INVOICE`
- function libraries: SyntaxEDI_Common, SyntaxEDI_Date, SyntaxEDI_Node, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_CO_EDI_INVOICE_REQUEST_OUT_cdm__2__INVOICE_2`
- package: SYNTAX_EDI_S4HC  |  namespace: `http://syntax.com/edi_s4hc`
- source: `MT_S4HC_CO_EDI_INVOICE_REQUEST_OUT_cdm`  ->  target: `MT_INVOICE`
- function libraries: SyntaxEDI_Common, SyntaxEDI_Date, SyntaxEDI_Node, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_CO_EDI_SCHEDGAGRMT_OUT__2__DELFOR`
- package: SYNTAX_EDI_S4HC  |  namespace: `http://syntax.com/edi_s4hc`
- source: `MT_S4HC_CO_SCHEDAGRMT_OUT_cdm`  ->  target: `MT_DELFOR`
- function libraries: SyntaxEDI_Common, SyntaxEDI_Node, SyntaxEDI_Text, SyntaxEDI_Lookup

### `MM_DELFOR__2__SCHEDGAGRMTDLIVSCHEDULE_IN_V3`
- package: SYNTAX_EDI_S4HC  |  namespace: `http://syntax.com/edi_s4hc`
- source: `MT_DELFOR`  ->  target: `S4HC_SCHEDGAGRMTDLIVSCHEDULE_IN_cdm`
- function libraries: SyntaxEDI_Text, SyntaxEDI_Node

### `MM_INVOICE__2__SELFBILLINGREQUEST_API_IN`
- package: SYNTAX_EDI_S4HC  |  namespace: `http://syntax.com/edi_s4hc`
- source: `MT_INVOICE`  ->  target: `S4HC_BTP_SELFBILLINGREQUEST_API_IN_cdm`
- function libraries: SyntaxEDI_Date

### `MM_INVOICE__2__SELFBILLINGREQUEST_API_IN3`
- package: SYNTAX_EDI_S4HC  |  namespace: `http://syntax.com/edi_s4hc`
- source: `MT_INVOICE`  ->  target: `SPS_BTP_SELFBILLINGREQUEST_API_IN`
- function libraries: SyntaxEDI_Date

### `MM_ORDERS__2__SALESORDERBULKREQUEST_IN`
- package: SYNTAX_EDI_S4HC  |  namespace: `http://syntax.com/edi_s4hc`
- source: `MT_ORDERS`  ->  target: `S4HC_BTP_SALESORDERBULKREQUEST_IN_cdm`

### `MM_QALITY__2__InspectionCharacateristicEntityPost`
- package: SYNTAX_EDI_S4HC  |  namespace: `http://syntax.com/edi_s4hc`
- source: `MT_QALITY`  ->  target: `MT_S4HC_InspectionCharacteristicEntitiyPost`

### `MM_QALTIY__2__InspectionCharacateristicEntityPost`
- package: SYNTAX_EDI_S4HC  |  namespace: `http://syntax.com/edi_s4hc`
- source: `MT_QALITY_96A`  ->  target: `MT_S4HC_InspectionCharacteristicEntitiyPost`

### `MM_S4HC_CO_EDI_ORDER_REQUEST_OUT_cdm__2__ORDERS`
- package: SYNTAX_EDI_S4HC  |  namespace: `http://syntax.com/edi_s4hc`
- source: `MT_S4HC_CO_EDI_ORDER_REQUEST_OUT_cdm`  ->  target: `MT_ORDERS`
- function libraries: Common

### `MM_VDA490500__2__SCHEDAGRMTDLIVSCHEDULE_IN`
- package: SYNTAX_EDI_S4HC  |  namespace: `http://syntax.com/edi_vda_s4hc`
- source: `MT_VDA490500`  ->  target: `S4HC_SCHEDGAGRMTDLIVSCHEDULE_IN_cdm`

### `MM_VDA491600__2__JITCALLREQUEST_IN`
- package: SYNTAX_EDI_S4HC  |  namespace: `http://syntax.com/edi_vda_s4hc`
- source: `MT_VDA491600`  ->  target: `S4HC_JITCALLREQUEST_IN_cdm`
- function libraries: SyntaxEDI_Node

### `MM_VDA_491600__2__JITCALLREQUEST_IN`
- package: SYNTAX_EDI_S4HC  |  namespace: `http://syntax.com/edi_vda_s4hc`
- source: `MT_VDA491600`  ->  target: `S4HC_JITCALLREQUEST_IN_cdm`

### `MM_BatchPostResponse__2__Mail`
- package: SYNTAX_S4HC  |  namespace: `http://syntax.com/cdm`
- source: `MT_S4HC_PostResponse`  ->  target: `MT_S4HC_BatchResponse`
- function libraries: Common

### `MM_BatchREsponse__2__Mail`
- package: SYNTAX_S4HC  |  namespace: `http://syntax.com/cdm`
- source: `MT_S4HC_BatchResponse`  ->  target: `MT_S4HC_BatchResponse`
- function libraries: Common

### `MM_BatchRequest__2__BatchResponse`
- package: SYNTAX_S4HC  |  namespace: `http://syntax.com/cdm`
- source: `MT_S4HC_BatchRequest`  ->  target: `MT_S4HC_BatchResponse`
- function libraries: SyntaxS4HC_Json, SyntaxS4HC_Node, SyntaxS4HC_Lookup

### `MM_BatchResponse__2__BatchResponse`
- package: SYNTAX_S4HC  |  namespace: `http://syntax.com/cdm`
- source: `MT_S4HC_BatchResponse`  ->  target: `MT_S4HC_BatchResponse`
- function libraries: Common

### `MM_CO_EDI_DELIVERY_REQUEST_OUT__2__CO_EDI_DELIVERY_REQUEST_OUT_batch_prepare`
- package: SYNTAX_S4HC  |  namespace: `http://syntax.com/cdm`
- source: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_cdm`  ->  target: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_sort_cdm`
- function libraries: SyntaxS4HC_Node

### `MM_CO_EDI_DELIVERY_REQUEST_OUT__2__CO_EDI_DELIVERY_REQUEST_OUT_batch_prepare_2`
- package: SYNTAX_S4HC  |  namespace: `http://syntax.com/cdm`
- source: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_cdm`  ->  target: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_cdm`
- function libraries: SyntaxS4HC_Node

### `MM_CO_EDI_DELIVERY_REQUEST_OUT__2__CO_EDI_DELIVERY_REQUEST_OUT_prepare`
- package: SYNTAX_S4HC  |  namespace: `http://syntax.com/cdm`
- source: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_cdm`  ->  target: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_sort_cdm`
- function libraries: SyntaxS4HC_Node

### `MM_CO_EDI_DELIVERY_REQUEST_OUT__2__CO_EDI_DELIVERY_REQUEST_OUT_prepare_No_HU`
- package: SYNTAX_S4HC  |  namespace: `http://syntax.com/cdm`
- source: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_cdm`  ->  target: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_sort_cdm`
- function libraries: SyntaxS4HC_Node

### `MM_CO_EDI_DELIVERY_REQUEST_OUT__2__CO_EDI_DELIVERY_REQUEST_OUT_prepare_V1`
- package: SYNTAX_S4HC  |  namespace: `http://syntax.com/cdm`
- source: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_cdm`  ->  target: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_sort_cdm`
- function libraries: SyntaxS4HC_Node

### `MM_CO_EDI_DELIVERY_REQUEST_OUT__2__CO_EDI_DELIVERY_REQUEST_OUT_prepare_V2`
- package: SYNTAX_S4HC  |  namespace: `http://syntax.com/cdm`
- source: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_cdm`  ->  target: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_sort_cdm`
- function libraries: SyntaxS4HC_Node

### `MM_CO_EDI_DELIVERY_REQUEST_OUT__2__CO_EDI_DELIVERY_REQUEST_OUT_prepare_V3`
- package: SYNTAX_S4HC  |  namespace: `http://syntax.com/cdm`
- source: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_cdm`  ->  target: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_sort_cdm`
- function libraries: SyntaxS4HC_Node

### `MM_CO_EDI_DELIVERY_REQUEST_OUT__2__CO_EDI_DELIVERY_REQUEST_OUT_remap`
- package: SYNTAX_S4HC  |  namespace: `http://syntax.com/cdm`
- source: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_sort_cdm`  ->  target: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_remap_cdm`

### `MM_CO_EDI_DELIVERY_REQUEST_OUT__2__CO_EDI_DELIVERY_REQUEST_OUT_remap_V1`
- package: SYNTAX_S4HC  |  namespace: `http://syntax.com/cdm`
- source: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_sort_cdm`  ->  target: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_remap_cdm`

### `MM_CO_EDI_DELIVERY_REQUEST_OUT__2__CO_EDI_DELIVERY_REQUEST_OUT_remap_V2`
- package: SYNTAX_S4HC  |  namespace: `http://syntax.com/cdm`
- source: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_sort_cdm`  ->  target: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_remap_cdm`

### `MM_CO_EDI_DELIVERY_REQUEST_OUT__2__CO_EDI_DELIVERY_REQUEST_OUT_remove_batchsplit`
- package: SYNTAX_S4HC  |  namespace: `http://syntax.com/cdm`
- source: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_cdm`  ->  target: `MT_S4HC_CO_EDI_DELIVERY_REQUEST_OUT_cdm`
- function libraries: SyntaxS4HC_Node

### `MM_PostRequest__2__PostResponse`
- package: SYNTAX_S4HC  |  namespace: `http://syntax.com/cdm`
- source: `MT_S4HC_PostRequest`  ->  target: `MT_S4HC_PostResponse`
- function libraries: SyntaxS4HC_Json, SyntaxS4HC_Node, SyntaxS4HC_Lookup

### `MM_PostResponse__2__PostResponse`
- package: SYNTAX_S4HC  |  namespace: `http://syntax.com/cdm`
- source: `MT_S4HC_PostResponse`  ->  target: `MT_S4HC_PostResponse`
- function libraries: Common

### `MM_ProductionOrderRequest__2__ProductionOrderResponse`
- package: SYNTAX_S4HC  |  namespace: `http://syntax.com/cdm`
- source: `MT_S4HC_BatchRequest`  ->  target: `MT_S4HC_BatchResponse`
- function libraries: SyntaxS4HC_Json, SyntaxS4HC_Node, SyntaxS4HC_Lookup

### `MM_S4HC_CO_EDI_ORDER_REQUEST_OUT_cdm__2__ORDERS`
- package: SYNTAX_S4HC  |  namespace: `http://syntax.com/cdm`
- source: `MT_S4HC_CO_EDI_ORDER_REQUEST_OUT_cdm`  ->  target: `MT_ORDERS`
