## -----------------------------
## ----- Imports / utility -----
## -----------------------------
import os, os.path
import cherrypy
import json
import dbUtils


class SAE23_Website(object):
    @cherrypy.expose
    def index(self):
        page = dbUtils.createPage("", "SAE 23 - Tanguy Petiaud", "\n<p>salut</p>\n")
        cherrypy.session["filters"] = []
        return page
    
    @cherrypy.expose
    def unitInfo(self, unitID: int):
        unitInfo = dbUtils.displayUnitInformation(unitID)
        pageContent = ""
        pageStyle = 'unitInfo'

        stats = json.loads(unitInfo[4])
        tags = json.loads(unitInfo[6])
        pageContent += f'<img src="/templates/medias/images/{tags["faction"]}.svg" alt="le picture of spider-man">\n<ul>'
        for key in stats.keys():
            pageContent += f'<li>{key.capitalize()}: {stats[key]}</li>'

        pageContent += '\n'
        page = dbUtils.createPage(pageStyle, unitInfo[1], pageContent)
        return page
    
    @cherrypy.expose
    def unitList(self, faction = None, keywords = None):
        if faction is None:
            faction = ""
        if keywords is None or keywords == '':
            keywords = []
        else:
            keywords = [keywords]
        unitList = dbUtils.displayUnitList({"faction": faction, "keywords": keywords})
        pageContent = ""
        pageTitle = "Available units"
        pageStyle = 'unitList'

        pageContent += f'''
            <input type="text" id="factionInput" placeholder="Faction" value={faction}>
            <button onclick="setFaction()">Set faction</button>
            <button onclick="clearFaction()">Clear faction</button>
            <input type="text" id="keywordInput" placeholder="Keyword">
            <button onclick="addKeyword()">Add keyword</button>
            <button onclick="clearKeywords()">Clear keywords</button>
            <button onclick="filterUnits()">Display units</button>
        '''


        pageContent += '''
            <script>'''
        unitListCopy = []
        for unit in unitList:
            unitCopy = []
            unitCopy.append(unit[0])
            unitCopy.append(unit[1])
            unitCopy.append(unit[2])
            unitCopy.append(unit[3])
            unitCopy.append(unit[4])
            unitCopy.append(unit[5])
            unitCopy.append(json.loads(unit[6]))
            unitListCopy.append(unitCopy)
        pageContent += f'var unitList = {unitListCopy};'
        pageContent += '''
                var faction = "";
                var keywords = [];

                function setFaction() {
                    faction = document.getElementById("factionInput").value
                    console.log("Faction is: " + faction)
                }

                function clearFaction() {
                    faction = ""
                    console.log("Faction is: " + keywords)
                }

                function addKeyword() {
                    keywords.push(document.getElementById("keywordInput").value)
                    console.log("Keywords are: " + keywords)
                }

                function clearKeywords() {
                    keywords = []
                    console.log("Keywords are: " + keywords)
                }

                function filterUnits() {
                    let addUnit = false
                    let toPrint = []
                    let ul = document.getElementById("unitList")
                    ul.innerHTML = ''

                    console.log(keywords)

                    for (let i=0; i<unitList.length; i++) {
                        addUnit = true
                        for (let j=0; j<keywords.length; j++) {
                            if (unitList[i][6]["keywords"].includes(keywords[j]) == false) {
                                addUnit = false
                            }
                        }
                        if (unitList[i][6]["faction"] != faction && faction != "") {
                            addUnit = false
                        }

                        if (addUnit == true) {
                            toPrint.push(unitList[i])
                            li = document.createElement("li")
                            div = document.createElement("div")
                            div.setAttribute("class", "unitPreview")

                            img = document.createElement("img")
                            img.setAttribute("src", "/templates/medias/images/" + unitList[i][6]["faction"] + ".svg")
                            img.setAttribute("alt", "unit protrait")
                            div.appendChild(img)
                            
                            p = document.createElement("p")
                            p.appendChild(document.createTextNode(unitList[i][1]))
                            div.appendChild(p)

                            a = document.createElement("a")
                            a.setAttribute("href", "/unitInfo?unitID="+unitList[i][0])
                            a.appendChild(document.createTextNode("Unit info"))
                            div.appendChild(a)

                            li.appendChild(div)
                            ul.appendChild(li)
                        }
                    }

                    console.log(toPrint)
                }
            </script>
        '''

        pageContent += ""





        pageContent += '\n<ul id="unitList">'
        ## for unit in unitList:
        ##     pageContent += '\n<li>'
        ##     pageContent += '\n<div class="unitPreview">'
        ##     pageContent += '\n<img src="/templates/medias/images/wojak.png" alt="unit protrait">'
        ##     pageContent += f'\n<p>{unit[1]}</p>'
        ##     pageContent += f'\n<a href=/unitInfo?unitID={unit[0]}>Unit info</a>'
        ##     pageContent += '\n</div>'
        ##     pageContent += '\n</li>'
        pageContent += '\n</ul>'

        pageContent += '\n'
        page = dbUtils.createPage(pageStyle, pageTitle, pageContent)
        return page

    @cherrypy.expose
    def armyList(self, ownerID = ""):
        armyList = dbUtils.displayArmyList(ownerID)
        pageStyle = 'armyList'
        pageTitle = "Armies created"
        pageContent = ""

        pageContent += '''
            <form action="/armyList">
                <input type="text" name="ownerID" placeholder="Owner ID">
                <button type="submit">Set owner</button>
            </form>
        '''

        pageContent += '\n<ul id="armyList">'
        for army in armyList:
            pageContent += '\n<li>'
            pageContent += '\n<div class="armyPreview">'
            pageContent += f'\n<p>{army[2]}</p>'
            pageContent += f'\n<a href=/armyInfo?armyID={army[0]}>Details</a>'
            pageContent += '\n</div>'
            pageContent += '\n</li>'
        pageContent += '\n</ul>'

        pageContent += '\n'
        page = dbUtils.createPage(pageStyle, pageTitle, pageContent)
        return page

    @cherrypy.expose
    def armyInfo(self, armyID: int):
        linkList = dbUtils.displayArmyInformation(armyID)
        pageStyle = 'armyInfo'
        pageTitle = ""
        pageContent = ""

        if linkList is None:
            pageContent += '<p>The army does not exist.</p>'
        else:
            armyInfo = linkList[1]
            pageTitle = armyInfo[2]
            linkList = linkList[0]
        
            pageContent += '\n<ul id="userList">'
            unitCount = 0
            for link in linkList:
                pageContent += '\n<li>'
                pageContent += '\n<div class="linkList">'
                pageContent += f'\n<p>{link[3]} x {link[5]} - {link[6]*link[3]} points, {link[7]*link[3]} models</p>'
                pageContent += f'\n<a href=/unitInfo?unitID={link[2]}>Details</a>'
                pageContent += '\n</div>'
                pageContent += '\n</li>'
                unitCount += link[3]
            pageContent += '\n</ul>'
            pageContent += f'Total -  Units: {unitCount}, Points: {armyInfo[3]}, Models: {armyInfo[4]}'
            


        pageContent += '\n'
        page = dbUtils.createPage(pageStyle, pageTitle, pageContent)
        return page

    @cherrypy.expose
    def userList(self):
        userList = dbUtils.displayUserList()
        pageStyle = 'userList'
        pageTitle = "Registered users"
        pageContent = ""

        pageContent += '\n<ul id="userList">'
        for user in userList:
            pageContent += '\n<li>'
            pageContent += '\n<div class="userDetails">'
            pageContent += f'\n<p>{user[0]}</p>'
            pageContent += f'\n<p>{user[2]} {user[1]}</p>'
            pageContent += f'\n<a href=/armyList?ownerID={user[0]}>Armies</a>'
            pageContent += '\n</div>'
            pageContent += '\n</li>'
        pageContent += '\n</ul>'

        pageContent += '\n'
        page = dbUtils.createPage(pageStyle, pageTitle, pageContent)
        return page








if __name__ == "__main__":
    print("----- SAE 23 - Tanguy Petiaud -----")
    keepGoing = True
    while keepGoing:
        print("Choose an input:")
        print(" --- Unit Management ---")
        print("1. View units list")
        print("11. View specific unit information")
        print("2. Create unit")
        print("21. Modify unit")
        print(" --- Army Management ---")
        print("3. View armies list")
        print("31. View specific army information")
        print("4. Create army")
        print("41. Modify army")
        print(" --- User Management ---")
        print("5. Display users list")
        print("6. Create user")
        print("61. Delete user")
        print(" --- Webserver --- ")
        print("9. Start webserver.")
        print(" --- Database Management ---")
        print("B. Backup database")
        print("R. Restore database")
        print("\n0. Quit")
        menuChoice = input("Your choice: ")

        match menuChoice:
            case '1':
                doFilters = input("Would you like to apply some filter? [y/n]: ")
                if doFilters == 'y':
                    faction = input("Enter faction: ")
                    keywords = []
                    keepGoing2 = True
                    while keepGoing2:
                        keyword = input("Enter keyword, leave blank to quit: ")
                        if keyword == '':
                            keepGoing2 = False
                        else:
                            keywords.append(keyword)
                else:
                    faction = ""
                    keywords = []
                filters = {"faction": faction, "keywords": keywords}
                dbUtils.displayUnitList(filters)                                                                                     ## Done
            case '11':
                try:
                    unitID = int(input("Enter unit ID: "))
                    dbUtils.displayUnitInformation(unitID)                                                                          ## Done
                except ValueError:
                    print("\nThe value entered is incorrect\n")
                except:
                    print("Unknown error")
            case '2':
                dbUtils.createUnit()                                                                                                ## Done
            case '21':
                unitID = input("Enter unit ID: ") 
                dbUtils.modifyUnit(unitID)                                                                                          ## Done

            case '3':
                # doFilters = input("Would you like to apply some filter? [y/n]: ")
                # if doFilters == 'y':
                #     ## Filter choice
                #     pass
                ownerID = int(input("Enter the owner ID: "))
                dbUtils.displayArmyList(ownerID)                                                                                     ## Done, add filters feature?
            case '31':
                idNotSet = True
                while idNotSet:
                    try:
                        armyID = int(input("Enter army ID: "))
                        idNotSet = False
                    except ValueError:
                        print("The value entered is incorrect")
                dbUtils.displayArmyInformation(armyID)                                                                              ## Done
            case '4':
                dbUtils.createArmy()                                                                                                ## Done
            case '41':
                armyID = input("Enter army ID: ") 
                dbUtils.modifyArmy(armyID)                                                                                          ## Done

            case '5':
                dbUtils.displayUserList()                                                                                           ## Done
            case '6':
                dbUtils.createUser()                                                                                                ## Done
            case '61':
                idNotSet = True
                while idNotSet:
                    try:
                        userID = int(input("Enter user ID: "))
                        idNotSet = False
                    except ValueError:
                        print("The value entered is incorrect")
                dbUtils.deleteUser(userID)                                                                                                ## Done

            case '9':
                rootPath = os.path.abspath(os.getcwd())
                conf = {
                    '/': {
                        'tools.sessions.on': True,
                        'tools.staticdir.root': rootPath
                        },
                    '/templates': {
                        'tools.staticdir.on': True,
                        'tools.staticdir.dir': './sources'
                }
                }
                cherrypy.quickstart(SAE23_Website(), '/', conf)

            case 'B' | 'b':
                backupDir = input("Enter target directory (leave blank to use default directory): ")
                if backupDir == "":
                    backupDir = "DB backup"
                dbUtils.dbBackup(backupDir)
            case 'R' | 'r':
                dbUtils.dbRestore()

            case '0':
                keepGoing = False
                break
        input("\nPress enter to continue...")
        print()
    print("And a good day to you!")


