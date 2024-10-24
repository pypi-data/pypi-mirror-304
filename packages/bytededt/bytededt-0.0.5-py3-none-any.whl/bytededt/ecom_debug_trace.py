# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals
try:
   import Queue
except ImportError:
   import queue as Queue
import logging
import threading
import sys
# sys.path.append('/data01/rentianhang.ryan/ecom_debug_trace_py/utils')

#from databus_python.databus.collector import collect as databus_collect
from databus import collect as databus_collect
from bytedenv import get_idc_name, get_psm
from bytedenv.service import PSM_UNKNOWN
from .utils.metrics import mcli as metrics
from .utils.tools import now_time
from .utils.models import BusinessMsg
from bytedtcc import ClientV2 as TccClientV2, TCCKeyNotFoundError, TCCError
import json

class EcomDebugTrace:
    channel_dict = {
        'CN_PC': 'bmq_data_ecom_debug_trace', # 国内比价
        'CN_GR': 'bmq_data_ecom_goldrush_debug_trace' # 国内TJ
    }

    domain_dict = {
        '0':  'PC_Rule_Domain',
        '1':  'PC_Signal_Domain',
        '2':  'PC_MistakeFeedback_Domain',
        '3':  'PC_SameSearch_Domain',
        '4':  'PC_BasicData_Domain',
        '5':  'PC_Epiboly_Domain',
        '6':  'PC_Platform_Domain',
        '7':  'GR_Scheduler',
        '8':  'GR_Tc',
        '9':  'GR_Processor',
        '10': 'GR_Saver',
        '11': 'GR_Consumer',
        '12': 'GR_Pic_Downloader',
	    '13': 'GR_Out_Downloader',
        '99': 'PC_TEST'
    }

    class QueryType:
        class ConstError(TypeError):
            pass

        class ConstCaseError(ConstError):
            pass

        def __setattr__(self, name, value):
            if name in self.__dict__:
                raise self.ConstError("Can't change const value!")
            if not name.isupper():
                raise self.ConstCaseError('const "%s" is not all letters are capitalized' % name)
            self.__dict__[name] = value

    QueryType.ALL = 0

    def __init__(self):
        self.LOGGER = logging.getLogger("edt")
        self.LOGGER.info("Edt: cold start")
        self.__region = 'CN'
        self.__service_name = ''
        self.__cluster = 'default'
        self.__address = ''
        self.__priority = 6
        self.__channel_type = ''
        self.__channel_name = ''
        self.__hive_channel_name = ''
        self.__duration = 1000  # ms
        self.__requests = Queue.Queue()
        self.__dc = None
        self.__unblock = True
        self.__consumer = None
        self.__sync = False
        self.__psm = ''
        self.__storage_mode = 'bmqindex'
        self.__downsample = 100
        self.__tcc_client = TccClientV2('data.ecom.debug_trace', 'default')
        self.LOGGER.info("Edt: cold start -> end")

    def __get_psm(self,service_name):
        """Get current PSM.
        :returns: PSM
        :rtype: str
        """
        psm = get_psm()
        return psm if psm != PSM_UNKNOWN else service_name

    def __update_tcc_config(self):
        
        try:
            value = self.__tcc_client.get(self.__service_name)
            tcc_config = json.loads(value)
            # get global config
            self.__downsample = tcc_config.get('downsample',self.__downsample)
            self.__channel_name =  tcc_config.get('databus_channel',self.__channel_name)
            self.__hive_channel_name = tcc_config.get('databus_hive_channel',self.__channel_name )
            self.__storage_mode = tcc_config.get('storage_mode',self.__storage_mode)
            # get product config 
            online_psm_config = tcc_config.get(self.__psm,None)
            if online_psm_config is not None:
                self.__downsample = online_psm_config.get('downsample',self.__downsample)
                self.__channel_name =  online_psm_config.get('databus_channel',self.__channel_name)
                self.__storage_mode = online_psm_config.get('storage_mode',self.__storage_mode)
                self.LOGGER.debug("edt tcc config %s %s" %(self.__psm, online_psm_config))
            else:
                self.LOGGER.debug("not found online_psm %s config,use default config" % self.__psm)
            # 新增是否开启白名单制度
            if tcc_config.get('unblock_list')==1  and online_psm_config is None:
                self.LOGGER.error("edt unblock_list is True, failed %s" % self.__psm)
                self.__unblock = False 
        except TCCKeyNotFoundError as e:
            self.LOGGER.debug("tcc TCCKeyNotFoundError,%s" % str(e))
        except TCCError as e:
            self.LOGGER.debug("tcc TCCError,%s" % str(e))
        except Exception as e:
             self.LOGGER.debug("tcc Exception,%s" % str(e))
        return None

    def init(self, region, service_name, cluster, address, priority, channel_type='CN_PC', sync=False,psm = '',storage_mode=''):
        self.LOGGER = logging.getLogger("edt")
        self.LOGGER.info("EDT: init start, region=%s, service_name=%s, cluster=%s" % (region, service_name, cluster))
        self.__region = region
        self.__service_name = service_name
        self.__psm = psm if psm != '' else self.__get_psm(self.__service_name)
        self.__address = address
        self.__priority = priority
        self.__channel_type = channel_type
        self.__channel_name = self.channel_dict.get(channel_type, None)
        self.__duration = 1000  # ms
        self.__dc = None
        self.__unblock = True
        self.__sync = sync
        self.__storage_mode = storage_mode if storage_mode != '' else 'bmqindex'
        self.check()
        self.__update_tcc_config()
        if not self.__sync:
            self.__consumer = threading.Thread(target=self.__do_collect, name='edt_consumer')
            # self.__consumer.setDaemon(True)
            self.__consumer.start()
        self.LOGGER.info("EDT: init end, region=%s, service_name=%s, cluster=%s, PSM=%s, databus_channel=%s" % 
            (self.__region,self.__service_name,self.__cluster,self.__psm,self.__channel_name))

    def close(self):
        self.LOGGER.info("EDT: close start, region=%s service_name=%s cluster=%s" % 
            (self.__region,self.__service_name,self.__cluster))
        self.__unblock = False
        if not self.__sync:
            self.__consumer.join()
        self.LOGGER.info("EDT: close end, region=%s service_name=%s cluster=%s" % 
            (self.__region,self.__service_name,self.__cluster))

    def set_channel_type(self, channel_type):
        self.__channel_type = channel_type
        self.__channel_name = self.channel_dict.get(channel_type, None)

    def set_channel_name(self, channel_name):
        self.__channel_name = channel_name

    def set_service_name(self, service_name):
        self.__service_name = service_name

    def set_region(self, region):
        self.__region = region

    def set_cluster(self, cluster):
        self.__cluster = cluster

    def set_address(self, address):
        self.__address = address

    def enable_dc(self):
        try:
            self.__dc = get_idc_name()
        except Exception as e:
            logging.error("EDT: get_idc failed: %s" % str(e))
            self.__dc = 'unknown'

    def set_duration(self, duration):
        self.__duration = duration

    def set_priority(self, priority):
        self.__priority = priority

    def check(self):
        if self.__channel_name is None:
            self.__unblock = False
            return
        self.__unblock = self.__validate_psm()

    # SDK方法区
    def debug(self, priority, biz_index_id, biz_domain_id, payload=None, query_type=QueryType.ALL, kv_params={}, 
                extra={}, unique_key=''):
        if priority <= self.__priority:
            return self.__collect(biz_index_id=biz_index_id, biz_domain_id=biz_domain_id, payload=payload,
                                  query_type=query_type, kv_params=kv_params, extra=extra, uk=unique_key)
        return -1

    def debug2(self, priority, biz_index_id, src_index_id, biz_domain_id, payload=None, query_type=QueryType.ALL, kv_params={}, 
                extra={}, unique_key=''):
        if priority <= self.__priority:
            return self.__collect(biz_index_id=biz_index_id, biz_domain_id=biz_domain_id, payload=payload,
                                  query_type=query_type, kv_params=kv_params, extra=extra, uk=unique_key, src_index_id=src_index_id)
        return -1
    
    def event_debug(self, priority, biz_index_id, src_index_id, biz_domain_id, event, payload=None, query_type=QueryType.ALL, kv_params={}, 
                extra={}, unique_key=''):
        if priority <= self.__priority:
            return self.__collect(biz_index_id=biz_index_id, biz_domain_id=biz_domain_id, payload=payload,
                                  query_type=query_type, kv_params=kv_params, extra=extra, uk=unique_key,
                                  src_index_id=src_index_id, event=event)
        return -1

    def event_date_debug(self, priority, biz_index_id, src_index_id, biz_domain_id, event, date, payload=None, query_type=QueryType.ALL, kv_params={}, 
                extra={}, unique_key=''):
        if priority <= self.__priority:
            return self.__collect(biz_index_id=biz_index_id, biz_domain_id=biz_domain_id, payload=payload,
                                  query_type=query_type, kv_params=kv_params, extra=extra, uk=unique_key,
                                  src_index_id=src_index_id, event=event, date=date)
        return -1
    
    def gr_debug(self, priority, biz_index_id, src_index_id, biz_domain_id, thd_index_id, forth_index_id, fifth_index_id, event, sub_event, date,
            payload=None, query_type=QueryType.ALL, kv_params={}, extra={}):
        if priority <= self.__priority:
            return self.__collect(biz_index_id=biz_index_id, biz_domain_id=biz_domain_id, payload=payload,
                                  query_type=query_type, kv_params=kv_params, extra=extra, uk="",
                                  src_index_id=src_index_id, event=event, date=date, thd_index_id=thd_index_id,
                                  forth_index_id=forth_index_id, fifth_index_id=fifth_index_id, sub_event=sub_event)

        return -1

    def __validate_psm(self):
        if self.__service_name is None or self.__service_name == '' \
                or self.__service_name == 'unknown':
            return False
        psm_list = self.__service_name.split('.')
        if len(psm_list) < 3:
            return False
        return True

    def __collect(self, biz_index_id, biz_domain_id, payload=None, query_type=QueryType.ALL, kv_params={}, extra={}, uk='',
                    src_index_id='', event='', date='', thd_index_id='', forth_index_id='', fifth_index_id='', sub_event=''):
        self.__update_tcc_config()
        if not self.__unblock:
            return -2
        if biz_index_id == '' or biz_domain_id == '' or type(kv_params) != dict or type(extra) != dict:
            self.LOGGER.error("EDT: collect biz_index_id=%s; biz_domain_id=%s; kv_params=%s; kv_params=%s"
                              % (str(biz_index_id), str(biz_domain_id), str(kv_params), str(type(kv_params))))
            metrics.emit_counter('fail', 1, tags={'service_name': self.__service_name,
                                'err_code': 'edt-4'})
            return -4
        # add downsample by trace_id
        # if hash(biz_index_id)%100 > self.__downsample:
        #     metrics.emit_counter('fail', 1, tags={'service_name': self.__service_name,
        #                         'err_code': 'edt-5'})
        #     return -5
        try:
            request = BusinessMsg()
            request.biz_index_id = biz_index_id
            request.region = self.__region
            request.address = self.__address
            request.service_name = self.__service_name
            request.timestamp = now_time()
            request.query_type = query_type
            request.biz_domain_name = self.domain_dict.get(biz_domain_id, '')
            request.biz_domain_id = biz_domain_id
            request.event = event
            request.event_date = date
            request.kv_params = kv_params
            request.payload = payload if payload is not None else ''
            request.extra = extra
            
            if self.__dc is not None:
                request.dc = self.__dc
            
            if uk is not None and uk != '':
                request.unique_key = uk

            if src_index_id is not None and src_index_id != '':
                request.scd_index_id = src_index_id

            if thd_index_id != '':
                request.thd_index_id = thd_index_id
            
            if forth_index_id != '':
                request.forth_index_id = forth_index_id

            if fifth_index_id != '':
                request.fifth_index_id = fifth_index_id
            
            if sub_event != '':
                request.sub_event = sub_event
            
            if self.__cluster is not None and self.__cluster != '':
                request.cluster = self.__cluster

            self.LOGGER.debug(
                "__collect: biz_index_id=%s; address=%s; timestamp=%d; service=%s; event=%s; dc=%s; query_type=%d"
                % (request.biz_index_id, request.address,
                   request.timestamp, request.service_name, request.event,
                   str(request.dc), request.query_type))

            if not self.__sync:
                self.__requests.put(request, block=True, timeout=3)
            else:
                try:
                    request = self.__requests.get(block=True, timeout=(self.__duration / 1000))
                    databus_collect(self.__channel_name, json.dumps(request.__dict__, ensure_ascii=True).encode('utf-8'))
                    metrics.emit_counter('success', 1, tags={'service_name': self.__service_name})
                    if self.__psm:
                        metrics.emit_counter('sub_service_name', 1, tags={'service_name': self.__service_name, 'sub_service': self.__psm})
                except Exception as e:
                    self.LOGGER.error("EDT1: collect failed: %s" % str(e))
                    metrics.emit_counter('fail', 1, tags={'service_name': self.__service_name,
                                        'err_code': '-1'})
            return 0
        except Exception as e:
            self.LOGGER.error("EDT2: collect failed: %s" % str(e))
            metrics.emit_counter('fail', 1, tags={'service_name': self.__service_name,
                                'err_code': 'edt-3'})
            return -3

    def __do_collect(self):
        success_count = 0
        while self.__unblock or not self.__requests.empty():
            # self.LOGGER.debug("EDT: size of requests: %d; is empty: %s; unblock: %s"
            #              % (self.__requests.qsize(), self.__requests.empty(), self.__unblock))
            try:
                request = self.__requests.get(block=True, timeout=(self.__duration / 1000))
                databus_collect(self.__channel_name, json.dumps(request.__dict__, ensure_ascii=True).encode('utf-8'))
                metrics.emit_counter('success', 1, tags={'service_name': self.__service_name})
                success_count = success_count + 1
                if success_count >= 20:
                    metrics.emit_counter('success', success_count,
                                         tags={'service_name': self.__service_name})
                    success_count = 0
                    metrics.emit_store('queue_size', self.__requests.qsize(),
                                       tags={'service_name': self.__service_name})
            except Queue.Empty as e:
                self.LOGGER.info("EDT: cannot get request: %s" % str(e))
            except Exception as e:
                self.LOGGER.error("EDT3: collect failed: %s" % str(e))
                metrics.emit_counter('fail', 1, tags={'service_name': self.__service_name,
                                    'err_code': '-1'})
        if success_count > 0:
            metrics.emit_counter('success', success_count,
                                 tags={'service_name': self.__service_name})
            success_count = 0
            metrics.emit_store('queue_size', self.__requests.qsize(),
                               tags={'service_name': self.__service_name})
        return True


ecom_debug_trace = EcomDebugTrace()
