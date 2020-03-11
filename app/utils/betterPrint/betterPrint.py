# @Time    : 2020/3/7 13:58
# @Author  : yuzhanglong
# @Email   : yuzl1123@163.com


class BetterPrint:
    def __init__(self, name):
        self.name = name
        self.temp = []

    def route(self, rule, **options):
        def decorator(f):
            self.temp.append((f, rule, options))
            return f
        return decorator

    def register(self, bluePrint, urlPrefix=None):
        if urlPrefix is None:
            urlPrefix = '/' + self.name
        # 序列解包
        for f, rule, options in self.temp:
            endpoint = self.name + '+' + options.pop("endpoint", f.__name__)
            bluePrint.add_url_rule(urlPrefix + rule, endpoint, f, **options)



