from krutils import utils

print(utils.__file__)
logger = utils.logger(__file__)


a = 10.0
b = 20.0

logger.syslog("[%%] %% - {%%}", a, b, a)
logger.dblog("[%%] %% - {%%}", a, b, a)
logger.debug("[%%] %% - {%%}", a, b, a)
logger.info("[%%] %% - {%%}", a, b, a)
logger.error("[%%] %% - {%%}", a, b, a)


