# migration script from seda 2.1 to seda 2.2

import logging

logger = logging.getLogger("seda.migration")
logger.setLevel(logging.INFO)

logger.info("\n\nReplace cubicweb_eac by cubicweb_eac_seda \n\n")

drop_cube("eac")
add_cube("eac_seda")
