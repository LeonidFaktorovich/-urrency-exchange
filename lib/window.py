import ibm_db
import ibm_db_dbi
import pandas

class plot_1_to_550():
    dsn_hostname = ""
    dsn_uid = ""
    dsn_pwd = ""
    dsn_driver = ""
    dsn_database = ""
    dsn_port = ""
    dsn_protocol = ""
    dsn_security = ""
    dsn = (
        "DRIVER={0};"
        "DATABASE={1};"
        "HOSTNAME={2};"
        "PORT={3};"
        "PROTOCOL={4};"
        "UID={5};"
        "PWD={6};"
        "SECURITY={7};").format(dsn_driver, dsn_database, dsn_hostname,
                                dsn_port, dsn_protocol, dsn_uid, dsn_pwd, dsn_security)
    conn = ibm_db.connect(dsn, "", "")
    pconn = ibm_db_dbi.Connection(conn)
    