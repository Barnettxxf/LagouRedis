# -*- coding:utf-8 -*-

from LagouRedis.utils.common import MysqlConnection


class GetIp(MysqlConnection):

    @property
    def ip_list(self):
        return self.get_ip()

    def get_ip(self):
        query_sql = """
            select ip,port from proxyhttps order by date_time DESC limit 40;
        """
        self.execute(query_sql)
        return self.cursor.fetchall()



