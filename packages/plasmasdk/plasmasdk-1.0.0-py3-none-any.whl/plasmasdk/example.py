from plasmasdk.sdk_v2 import *

if __name__ == '__main__':
    # 鉴权信息
    access_key = ""
    secret_key = ""
    res_method = 'POST'
    server_ip = ''
    # 设置全局鉴权信息
    set_global_info(AccessKey = access_key,SecretKey = secret_key,ResMethod = res_method,ServerIp = server_ip)
    # 000688科创50指数成分股
    index_component = get_index_indexcomponent(symbols=["000688"])
    # 成分股数量
    print("index_component_length:",len(index_component['symbol']))
    symbols = index_component['symbol']
    # 设置报告期
    report_date1 =['20231231']
    # 指标字段域 (资产总计,负债合计,归属于母公司所有者权益合计,货币资金)
    field = ["totasset","totliab","paresharrigh","curfds"]
    # 指标对应函数
    # functions_and_args = [  ("totasset", "get_s_totasset",{"code": symbols, "report_date": report_date1, "report_type": '3'}),
    #                         ("totliab", "get_s_totliab",{"code": symbols, "report_date": report_date1, "report_type": '3'}),
    #                         ("paresharrigh", "get_s_paresharrigh",{"code": symbols, "report_date": report_date1, "report_type": '3'}),
    #                         ("curfds", "get_s_curfds",{"code": symbols, "report_date": report_date1, "report_type": '3'})
    #                     ]
    functions_and_args = [("totasset", "get_s_totasset",{"code": symbols, "report_date": report_date1, "report_type": '3'})]

    import time
    start_time = time.time()
    result = get_query_builder(field,functions_and_args)
    # result['symbol']=result.apply(lambda x:str(x['symbol']),axis=1)
    # result.to_csv("fundamental.csv",index=False)
    print("finance date :" + str(result))
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"ALLQUERY执行时间：{execution_time} 秒")