# coding=utf-8

import web

from .ValueCalculator import PriceDataStructure
from .ValueCalculator import ValueCalculator

render = web.template.render('interface/')

urls = (
    '/', 'index',
)
app = web.application(urls, globals())


class index:
    def GET(self):
        return render.index()

    def POST(self):
        self.profileURL = ""
        i = web.input()

        for tag in i:
            if tag == "profileURL":
                self.profileURL = i[tag]

        if self.profileURL == "":
            return render.result("<center>You need to specify a profile URL!</center><br>")

        calculator = ValueCalculator(self.profileURL)
        ds = calculator.calculate()

        return render.result(ds)


def main():
    calculator = ValueCalculator("http://steamcommunity.com/id/diogocme")
    ds = calculator.calculate()

    print(ds)


if __name__ == '__main__':
    app.run()
#    main()
