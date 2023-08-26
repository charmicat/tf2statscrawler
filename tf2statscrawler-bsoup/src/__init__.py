import web

from .crawler import Crawler

render = web.template.render('interface/')

urls = (
    '/', 'index',
)
app = web.application(urls, globals())


class index:
    def GET(self):
        return render.index()

    def POST(self):
        self.groupURL = ""
        selected_stats = []
        selected_classes = dict({"Soldier": False, "Spy": False, "Scout": False,
                                 "Medic": False, "Engineer": False, "Demoman": False,
                                 "Heavy": False, "Pyro": False, "Sniper": False})
        i = web.input()

        for tag in i:
            if tag.startswith("stat_"):
                selected_stats.append(i[tag])
            elif tag.startswith("class_"):
                selected_classes[i[tag]] = True
            elif tag == "groupURL":
                self.groupURL = i[tag]

        if len(selected_stats) < 1 or len(selected_classes) < 1:
            return render.result("<center>You need to select at least one Class and one Stat!</center><br>")

        if self.groupURL == "":
            return render.result("<center>You need to specify a group URL!</center><br>")

        c = Crawler(selected_stats, selected_classes)
        self.filledStats = c.getStatsFromGroupProfile(self.groupURL)

        fScore = self.formatScore()
        return render.result(fScore)

    def formatScore(self):
        # Ridiculo fazer isso aqui, mas nao consegui formatar no template nem a pau
        i = 0
        content = ""
        content += "Summary of stats for the group: <a href=\"" + self.groupURL + "\"> " + self.groupURL + "</a><br>"
        content += "<br>"

        for stat in self.filledStats:
            i += 1
            content += "<b>__ Stat: </b>" + stat + "<br>"
            content += "<table class=\"userTable\">"

            for classStats in self.filledStats[stat].statByClass:

                currentClass = self.filledStats[stat].statByClass[classStats]

                if currentClass.statValue != -1:
                    content += "<tr><td>"
                    content += "<img src=\"http://steamcommunity.com/public/images/apps/440/" + classStats.lower() + ".jpg\">"
                    content += "</td><td><br>"

                    content += "<b>Class:  </b>" + classStats + "<br>"
                    content += "<b>User:   </b>" + currentClass.userName + "<br>"
                    content += "<b>Points: </b>%s" % currentClass.statValue + "<br>"
                    content += "<b>URL:    </b><a href=\"" + currentClass.profileURL + "\">" + currentClass.profileURL + "</a><br>"
                    content += "<br>"
                    content += "</tr></td>"

            content += "</table>"

            if (i < len(self.filledStats)):
                content += "<hr><br>"

        return content


if __name__ == "__main__":
    app.run()
