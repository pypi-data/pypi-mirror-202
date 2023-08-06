'''
LOG처리
    내가 필요한것은 로그 문자열 포멧팅 밖에 없다.
    나중에 logging을 래핑하자

'''




# 로그 설정값을 관리
class _logger_config:

    def __init__(self):
        ######################
        # 기본 변수

        # 호출자 인덱스
        self._CALLER_IDX        = 4;

        # 문자열 치환자
        self._LOG_SUBSTITUTOR    = "%%";

        # 시스템 로그를 포함하여 출력
        self.DEBUG_LEVEL_ALL    = _logger_util().get_log_level_index("SYSTEM");
        # # DB접근 로그를 포함하여 출력
        self.DEBUG_LEVEL_DB     = _logger_util().get_log_level_index("DB");
        # # 프로그램 로그를 포함하여 출력
        self.DEBUG_LEVEL_DEBUG  = _logger_util().get_log_level_index("DEBUG");
        # # 중요 정보 발생시 출력
        self.DEBUG_LEVEL_INFO   = _logger_util().get_log_level_index("INFO");
        # # 오류 발생시 출력
        self.DEBUG_LEVEL_ERROR  = _logger_util().get_log_level_index("ERROR");


        ######################
        # 설정

        # 파일명 지정
        self.CONFIG_FILE_PATH = './'
        self.CONFIG_FILE_NAME = 'logger.json'

        ######################
        # 로거 동작 설정
        ######################
        # 현재 로그레벨 (최초 생성시 기본로그레벨로 세팅)
        self.CURR_DEBUG_LEVEL       = _logger_util().get_log_level_index("INFO");

        # 디버깅 출력 방법 : 콘솔 출력 여부
        self.DEBUG_CONSOLE_PRINT_YN = "Y";

        # 디버깅 출력 방법 : 파일 출력 여부
        self.DEBUG_FILE_PRINT_YN    = "N";


        # 디버깅 출력 방법 : 파일 출력 경로
        from datetime import datetime
        self.DEBUG_FILE_DIR_PATH  = "./logs";
        self.DEBUG_FILE_FILE_NAME  = datetime.now().strftime("%H%M%S") + '.log';




class _logger_util:

    def _find_config_file_path(self, start_path: str) -> str:

        import os

        curr_dir = os.path.dirname(start_path)
        # print("start_path[{0}]".format(curr_dir))

        _cfg = _logger_config()

        config_file_path = ""
        # while True:
        for ii in range(5):
            # print("seeking..[{0}]th : {1}".format(ii, curr_dir))

            if (os.path.isfile(curr_dir + "/" + _cfg.CONFIG_FILE_NAME) == True):
                config_file_path = os.path.join(curr_dir, _cfg.CONFIG_FILE_NAME)
                # print("찾았다!", config_file_path)
                break
            else:
                # print("상위로 찾아 올라간다[{0}]->[{1}]".format(curr_dir, os.path.abspath(os.path.join(curr_dir, '..'))))
                # root까지 확인된 경우 : 더이상 찾을 수 없을 때
                if (curr_dir == os.path.abspath(os.path.join(curr_dir, '..'))):
                    # print("못찾았다!")
                    config_file_path = ''
                    # raise Exception(_cfg.CONFIG_FILE_NAME + " 파일을 찾을 수 없습니다.")
                    break
                else:
                    curr_dir = os.path.abspath(os.path.join(curr_dir, '..'))

        # print("get_config_file_path() -> [{0}]".format(config_file_path))
        return config_file_path



    # 로깅 레벨 설정
    def get_log_level_index(self, level: str) -> int:
        if level == None:
            return 4
        elif level == "ERROR":
            return 4
        elif level == "INFO":
            return 3
        elif level == "DEBUG":
            return 2
        elif level == "DB":
            return 1
        elif level == "SYSTEM":
            return 0
        return 4



# 로깅 클래스의 기능을 담아놓는다.
class _logging:

    def __init__(self):

        super().__init__()

        # 기본 설정 값
        self.config = _logger_config()



    # 호출자 파일 명
    def _caller_file_name(self) -> str:

        import os, inspect
        caller_file_path = inspect.stack()[self.config._CALLER_IDX][1]

        return os.path.basename(caller_file_path)

    # 호출자 라인번호
    def _caller_file_line(self) -> int:
        import inspect
        return inspect.stack()[self.config._CALLER_IDX][2]


    ##########################################
    ##      log
    ##########################################
    def _gen_substitutor_dummy_string(self, cnt: int) -> str:
        '''Dummy 치환자 문자열 생성'''
        ret = ""

        for ii in range(cnt):
            ret = ret + self.config._LOG_SUBSTITUTOR

        return ret


    def _gen_log_header(self, debug_level) -> str:
        '''[HH24MISS.FFF][CALLER_NAME:LINE5byte]'''

        from datetime import datetime

        HEADER_LENGTH = 40

        header = ""
        if (debug_level == self.config.DEBUG_LEVEL_ALL):
            header = header + "[SYS]"
        elif (debug_level == self.config.DEBUG_LEVEL_DB):
            header = header + "[SQL]"
        elif (debug_level == self.config.DEBUG_LEVEL_APP):
            header = header + "[DBG]"
        elif (debug_level == self.config.DEBUG_LEVEL_INFO):
            header = header + "[INF]"
        elif (debug_level == self.config.DEBUG_LEVEL_ERROR):
            header = header + "[ERR]"

        header = header + " " + "[" + datetime.now().strftime("%H%M%S.%f")[:-3] + "]"                               # 일시
        header = header + " " + "[" + self._caller_file_name() + ":" + str(self._caller_file_line()).zfill(5) + "]"       # 호출자
        header = header.ljust(HEADER_LENGTH, " ")                                                                   # 길이 맞추기


        return header



    def _substitute_string(self, input: str, *args) -> str:

        if input == None:
            return None

        # print ("len", str(len(args)))
        # print (args)
        for ii, arg in enumerate(args):

            idx = 0
            try:
                idx = input.index(self.config._LOG_SUBSTITUTOR)
            except Exception as e:
                break;

            # print (idx)
            if (idx < 0):
                break;

            # print (self.config._LOG_SUBSTITUTOR)
            # print (input, input.replace(self.config._LOG_SUBSTITUTOR, str(arg), 1))
            input = input.replace(self.config._LOG_SUBSTITUTOR, str(arg), 1)

        return input


    def _print_log(self, debug_level, template="", *args):
        '''
        로그처리
        header + debug_strings...
        '''

        # 정합성 체크 : 시스템에 정의된 디버그레벨과 비교하여 로깅처리를 할지 정한다
        if (debug_level == None):
            return

        if (debug_level < self.config.CURR_DEBUG_LEVEL):
            return

        # object를 입력한 경우(예 : Exception) 문자로 변환하여 처리
        template_str = str(template)


        ######################
        # 처리

        # 문자열 치환
        log_body = self._substitute_string(template_str, *args)

        # 남은 치환자 제거
        log_body = log_body.replace(self.config._LOG_SUBSTITUTOR, "")


        #################
        # CONSOLE PRINT
        if self.config.DEBUG_CONSOLE_PRINT_YN == "Y":
            print (self._gen_log_header(debug_level) + " " + log_body)


        #################
        # FILE PRINT
        if self.config.DEBUG_FILE_PRINT_YN == "Y":
            print("파일프린트 시작한다[{}]".format(self.config.DEBUG_FILE_PRINT_PATH))
            # writelog (_gen_log_header(debug_level) + " " + log_body)
            pass



######################
# logger 클래스 메인
#   1. 설정파일을 찾아 적용한다. 없으면 기본값으로 적용한다.
class logger(_logging):
    '''
    My favorite log format maker.
    [LEVEL] [TIME] [SOURCE] contents...

    sample>
        logger = krutils.logger(__file__)

        a = 10.0
        b = 20.0

        logger.syslog("[%%] %% - {%%}", a, b, a)
        logger.dblog("[%%] %% - {%%}", a, b, a)
        logger.debug("[%%] %% - {%%}", a, b, a)
        logger.info("[%%] %% - {%%}", a, b, a)
        logger.error("[%%] %% - {%%}", a, b, a)

    result>
        [SYS] [103350.469] [tester.py:00010] [10.0] 20.0 - {10.0}
        [SQL] [103350.512] [tester.py:00011] [10.0] 20.0 - {10.0}
        [DBG] [103350.515] [tester.py:00012] [10.0] 20.0 - {10.0}
        [INF] [103350.518] [tester.py:00013] [10.0] 20.0 - {10.0}
        [ERR] [103350.520] [tester.py:00014] [10.0] 20.0 - {10.0}


    Options>
        Set option can redefine with 'logger.json' file.
        The 'logger.json' file can be caller program directory or above. krutil.logger will seek the 'logger.json' file from caller program directory to root diredctory.
        First found file will be adapted.

        SAMPLE> 'logger.json'
        {
            "LOG_LEVEL" : "INFO",
            "LOG_CONSOLE_YN" : "Y",
            "LOG_FILE_YN" : "N",
            "LOG_DIR_PATH" : "./logs",
            "LOG_FILE_NAME" : "mylog.log"
        }

        DESC> * is default value
        * LOG_LEVEL : SYSTEM/DB/DEBUG/INFO*/ERROR
        * LOG_CONSOLE_YN : Y*/N
        * LOG_FILE_YN : Y/N*
        * LOG_DIR_PATH : log directory path(None is default)
        * LOG_FILE_NAME : log file name(None is default)

    '''

    def __init__(self, caller_path: str):

        # logger에 필요한 변수와 기능이 담겨있는 super 클래스를 초기화 한다.
        super().__init__()

        # 인자로 받은 호출자 경로로 부터 root까지 탐색하며 config 파일을 찾는다.
        # 존재시 설정을 덮어 씌운다
        self.config.CONFIG_FILE_PATH = _logger_util()._find_config_file_path(caller_path)

        # realizer!!! is_empty로 변경, paser 메서드 작성.
        if (len(self.config.CONFIG_FILE_PATH) != 0):
            import json
            with open(self.config.CONFIG_FILE_PATH) as _cf:
                _cfc = json.load(_cf)

            # print(_cfc)

            # print("__LOG_LEVEL__[" + _cfc["__LOG_LEVEL__"] + "]")
            # print(_cfc["__LOG_LEVEL_"])       # 이렇게 하면 오류난다.



    def syslog(self, template="", *args):
        self._print_log(self.config.DEBUG_LEVEL_ALL, template, *args)



    def dblog(self, template="", *args):
        self._print_log(self.config.DEBUG_LEVEL_DB, template, *args)



    def debug(self, template="", *args):
        self._print_log(self.config.DEBUG_LEVEL_APP, template, *args)



    def info(self, template="", *args):
        self._print_log(self.config.DEBUG_LEVEL_INFO, template, *args)



    def error(self, template="", *args):
        self._print_log(self.config.DEBUG_LEVEL_ERROR, template, *args)


