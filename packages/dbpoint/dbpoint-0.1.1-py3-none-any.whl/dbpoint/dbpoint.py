#import datacontroller.datacontroller_exceptions as unified
from typing import Iterable, Callable
from dbpoint.perks import get_custom_logger, mem_free_now

logging = get_custom_logger('dbpoint')

class Hub(object):
    
    profiles = {}
    known_drivers = {}
    # implemented saab known-iks, kui a) teda esimest korda soovitakse ja b) siinses kaustas on sellenimeline .py fail  
    implemented_drivers = {'pg' : ['pg'], 'oracle' : ['oracle']
                           , 'asa' : ['asa'], 'maria' : ['maria']
                           , 'mssql' : ['mssql'], 'odbc' : ['odbc']}
    
    
    def __init__(self, list_of_profiles: list[dict]):
        #print(f"Init of {self.__class__.__name__}") # kuna metaclass on Singleton, siis juhtub see ühe korra ainult
        # siin võib ka kulutada aega ja uurida välja, kas kõvakettal on midagi, mis kvalifitseeruks draiveriks -> implemented_drivers
        # aga midagi ei tohi importida, initsialiseerida, ühendada (sest kõiki kindlasti vaja ei lähe)
        
        self.last_sql = ''
        self.last_sql_with_error = ''
        
        for one_profile in list_of_profiles or []:
            if isinstance(one_profile, dict): 
                self.add_profile(one_profile.get('name', ''), one_profile.copy())
        
        
    def get_last_error_command(self):
        return self.last_sql_with_error

    
    def get_last_command(self):
        return self.last_sql
        

    def run(self, profile_name: str, sql: str, do_return: bool = True, **kwargs):
        # param "sql" on üldjuhul SQL-KÄSK
        # aga see võib olla ka midagi muud, kui driaver pole SQL-draiver (X-tee jm hierahr json/xml, excel/csv)
        # see võib olla path/url    
        self.last_sql = sql
        driver = self.get_driver(profile_name)
    
        rs = None
        try:
            #logging.debug(f"Command for profile '{profile_name}'")
            rs = driver.run(sql, do_return, **kwargs)
        # vigu tasub püüda, kui otsustame mingeid olukordi üldtasemel ise ära töödelda
        except Exception as e3:
            self.last_sql_with_error = sql
            raise e3
        #self.last_sql_with_error = "" (jätame viimase vea puutumata, isegi kui on väga vana)
        return rs # mis võib olla ka tühi list (kui ei soovitud datat)
    
    
    def fn_stream(self, profile_name: str):
        def streamer(sql):
            driver = self.get_driver(profile_name)
            return driver.stream(sql)
        return streamer


    def copy_to(self, sql : str, profile_name : str, first_row_grab : Callable, side_effects : Callable | None, prepare_row_command : Callable, save_command : Callable, info_step: int = 1000):
        permanent_info = {}
        pos = 0
        logging.debug(f"copy_to.. {profile_name}")
        flow = self.fn_stream(profile_name)
        for pos, row in enumerate(flow(sql), 1):
            if pos == 1:
                permanent_info : dict = first_row_grab()
                if permanent_info is None:
                    logging.error("Problem with GRAB")
                    return -1
                #logging.debug(f"pos=1 start side effect")
                side_quest = side_effects() if side_effects is not None else True
                #logging.debug(f"pos=1 end side effect")
            command = prepare_row_command(row, permanent_info)
            if not save_command(command, pos):
                logging.error(f"Problem with SAVE, made {pos}")
                return -pos # if 1st row failes, return -1, if second returns -2
            if pos % info_step == 0:
                mem_free = mem_free_now()
                logging.info(f"Pulled up to here {pos} rows, free memory {mem_free:.2f}")
                if mem_free < 1:
                    logging.error(f"Out of memory very soon, so lets quit as we can it do now")
                    return -pos
            
        logging.info(f"copy_to END {pos} rows")
        return pos


    def generate_command_for_create_table(self, target_table: str, create_as_temp: False, cols_def = None, map_columns: dict = None) -> str:
        as_temp = ' TEMP' if create_as_temp else ''
        if map_columns is None:
            create_columns = ', '.join([col_def['name'] + ' ' + col_def['type'] for col_def in cols_def])
        else:
            create_columns = ', '.join([map_columns[col_def['name']] + ' ' + col_def['type'] for col_def in cols_def if col_def['name'] in map_columns and map_columns[col_def['name']] != ''])
        
        create_table = f"CREATE{as_temp} TABLE {target_table} ({create_columns})"
        print(f"{create_table=}")
        return create_table
        
    
    def to_file(self, profile_name: str, query: str, file_path) -> int:
        
        driver = self.get_driver(profile_name)
        
        try:
            number_of_rows = driver.to_file(query, file_path)
        except: # FIXME unified.DataControllerException as e0:
            print('vigusk juhtus: ' + str(e0))
            return -1
        return number_of_rows

    
    def get_driver(self, profile_name: str | None): # -> (Cursor, None)
        """
        Returns object capable to make actions and thus having database connection (makes on if no)
        """
        if profile_name is None:
            logging.error("Missing profile name for driver")
            return None
        
        profile_data = self.get_profile(profile_name)
        if profile_data is None:
            return None
        # lugeda profiilist välja, kes tagab teostuse
        driver_name = profile_data['driver']
        if profile_data['class'] is None: 
            driver_class = self.known_drivers[driver_name].DataDriver()
            self.set_profile_class(profile_name, driver_class)
        else:
            driver_class = profile_data['class']
        
        if driver_class.connect(profile_data) == 1: # 0 => was already connected
            logging.debug(f"Profile {profile_name} connected")
        
        return driver_class
        
        
    def get_profile(self, profile_name: str | None) -> dict | None:
        if profile_name is None:
            msg = f"Profile name (connection alias) is missing"
            logging.error(msg)
            return None
            #raise Exception(msg)
        if self.is_profile_exists(profile_name):
            return self.profiles[profile_name] # see on py suva, kas see on viide sama obj sisse või uus -- seega alati muuta selfi!
        else:
            msg = f"{profile_name} does not exists"
            logging.error(msg)
            return None
            #raise unified.DataControllerProfileExistenceException(f"Profile '{profile_name}' not existing")
            #raise Exception(msg)
    
    
    def find_driver(self, named_driver):
        '''
        Find driver by name, and import module containing it
        '''
        import importlib
        import os.path
        logging.debug(f"finding driver for '{named_driver}'")
        # turvameede -- mapper
        if named_driver not in self.implemented_drivers:
            msg = f"Driver {named_driver} is not implemented"
            raise Exception(msg)
            #raise unified.DataControllerProfileUnknowDriverException(f"Driver {named_driver} is not implemented")
        #module_to_import = self.implemented_drivers[named_driver][0] # vana
        
        module_name = self.implemented_drivers[named_driver][0]
        logging.debug(f"Module name for {named_driver} is {module_name}")
        long_module_name = '.'.join(['dbpoint', 'drivers', module_name]) # need on built-in moodulid! aga custom?
        logging.debug(f"Long module name is {long_module_name}")
        try: # lets try to import module, starting from root package and long_module_name
            named_driver_module = importlib.import_module(long_module_name, 'dbpoint') # package = self.current_file_dir_name)
            self.known_drivers[named_driver] = named_driver_module
        except Exception as e1:
            print(e1)
            msg = f"Cannot import module {long_module_name} from package dbpoint"
            logging.error(msg)
            return None
        
    
    def is_profile_exists(self, profile_name: str) -> bool:
        return profile_name in self.profiles 
    
    
    def is_driver_known(self, driver_name: str, try_to_find: bool = True) -> bool:
        if driver_name in self.known_drivers:
            return True
        if not try_to_find:
            return False
        self.find_driver(driver_name)
        return self.is_driver_known(driver_name, False) # kutsume välja iseenda, aga ei luba tsüklisse minna
        
    
    def add_profile(self, profile_name, profile_data) -> None:
        
        if 'driver' not in profile_data:
            msg = f"{profile_name} do not have driver"
            logging.error(msg)
            #raise unified.DataControllerProfileValidationException(f"Profile '{profile_name}' don't specify driver")
            raise Exception(msg)
        driver_name = profile_data['driver']
        if self.is_driver_known(driver_name):
            profile_data['class'] = None
            self.profiles[profile_name] = profile_data
            return
        logging.error(f"{profile_name} uses unknown driver {driver_name}")
        msg = f"Profile '{profile_name}' uses unknown driver '{driver_name}'"
        raise Exception(msg)
        #raise unified.DataControllerProfileUnknowDriverException()
    
    
    def is_profile_connected(self, profile_name) -> bool: # kas kasutame nime? või sisu dicti?
        return self.profiles[profile_name]['connected']
    
    
    def set_profile_class(self, profile_name: str, profile_class):
        self.profiles[profile_name]['class'] = profile_class
    
    
    def do_real_connection_check(self, profile_name):
        '''
        see võiks veenduda, kas ühendus on jätkuvalt olemas ja kui pole, siis markeerida kadunuks 
        '''
        ...

    def commit(self, profile_name):
        driver = self.get_driver(profile_name)
        if driver is None:
            error.log("Cannot commit, because of missing profile name")
            return None
        return driver.commit() # == None anyway

    def rollback(self, profile_name):
        driver = self.get_driver(profile_name)
        if driver is None:
            error.log("Cannot rollback, because of missing profile name")
            return None
        return driver.rollback()

    def disconnect(self, profile_name):
        if not self.is_profile_exists(profile_name):
            print(f"Profiili nimega '{profile_name}' pole olemas")
            return
        driver_class = self.profiles[profile_name]['class']
        if driver_class is None: # olukord, kus pole veel ühendust vajatudki, st pole loodud
            return 
        driver_class.disconnect() # siia ümber pole try vaja, sest driver peaklass juba tegeleb
        self.profiles[profile_name]['connected'] = False


    def disconnect_all(self):
        for profile_name in self.profiles:
            self.disconnect(profile_name)
            logging.debug(f"{profile_name} disconnected")

    def escape(self, profile_name, cell_value, data_class, needs_escape):
        driver = self.get_driver(profile_name)
        if driver is None:
            error.log("Cannot make escape expression, because of missing profile name")
            return None
        return driver.escape(cell_value, data_class, needs_escape)
    
    def get_columns_definition(self, profile_name):
        driver = self.get_driver(profile_name)
        if driver is None:
            error.log("Cannot get columns list, because of missing profile name")
            return None
        return driver.get_columns_definition()

    def __repr__(self):
        # kõik profiilid ühendusinfoga (parool on varjestatud) ja profiilide metainfoga (millal, palju)
        str_lines = []
        for jrk, (name, profile) in enumerate(self.profiles.items(), 1):
            str_lines.append(f"{jrk}) {name}")
            for key, value in profile.items():
                if key in ['password']:
                    out_value = "'" + value[0:1] + '*****' + "'"
                else:
                    out_value = repr(value) # nt class
                str_lines.append(f"  {key} = {out_value}")
            str_lines.append("")
        str_lines.append("")
        return "\n".join(str_lines)
    
