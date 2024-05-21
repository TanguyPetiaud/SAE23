## -----------------------------
## ----- Imports / utility -----
## -----------------------------
import pymysql
import json
import csv
import os, os.path
import cherrypy


class SAE23_Website(object):
    @cherrypy.expose
    def index(self):
        page = createPage("", "SAE 23 - Tanguy Petiaud", "\n<p>salut</p>\n")
        return page
    
    @cherrypy.expose
    def unitInfo(self, unitID: int):
        unitInfo = displayUnitInformation(unitID)
        pageContent = ""
        pageStyle = 'unitInfo'

        pageContent += '<img src="/templates/medias/images/pngegg.png" alt="le picture of spider-man">\n<ul>'
        stats = json.loads(unitInfo[4])
        tags = json.loads(unitInfo[6])
        for key in stats.keys():
            pageContent += f'<li>{key.capitalize()}: {stats[key]}</li>'

        pageContent += '\n'
        page = createPage(pageStyle, unitInfo[1], pageContent)
        return page
    
    @cherrypy.expose
    def unitList(self, faction = None, keyword = None):
        if faction is None:
            faction = ""
        if keyword is None or keyword == '':
            keyword = []
        else:
            keyword = [keyword]
        unitList = displayUnitList({"faction": faction, "keywords": keyword})
        pageContent = ""
        pageTitle = "Available units"
        pageStyle = 'unitList'

        pageContent += f'{faction}, {keyword}'

        pageContent += '<form action="/unitList">'
        pageContent += '<input type="text" name="faction" placeholder="Faction">'
        pageContent += '<input type="text" name="keyword" placeholder="Keyword">'
        pageContent += '<input type="submit" value="Apply Filters">'
        pageContent += '</form>'

        pageContent += '\n<ul class="unitList">'
        for unit in unitList:
            pageContent += '\n<li>'
            pageContent += '\n<div class="unitPreview">'
            pageContent += '\n<img src="/templates/medias/images/wojak.png" alt="unit protrait">'
            pageContent += f'\n<p>{unit[1]}</p>'
            pageContent += f'\n<a href=/unitInfo?unitID={unit[0]}>Unit info</a>'
            pageContent += '\n</div>'
            pageContent += '\n</li>'
        pageContent += '\n</ul>'

        pageContent += '\n'
        page = createPage(pageStyle, pageTitle, pageContent)
        return page

    @cherrypy.expose
    def armyList(self):
        armyList = displayArmyList({})
        pageStyle = 'armyList'
        pageTitle = "Armies created"
        pageContent = ""

        pageContent += '\n<ul class="userList">'
        for army in armyList:
            pageContent += '\n<li>'
            pageContent += '\n<div class="armyList">'
            pageContent += f'\n<p>{army[2]}</p>'
            pageContent += f'\n<a href=/armyInfo?armyID={army[0]}>Details</a>'
            pageContent += '\n</div>'
            pageContent += '\n</li>'
        pageContent += '\n</ul>'

        pageContent += '\n'
        page = createPage(pageStyle, pageTitle, pageContent)
        return page

    @cherrypy.expose
    def armyInfo(self, armyID: int):
        linkList = displayArmyInformation(armyID)
        pageStyle = 'armyInfo'
        pageTitle = ""
        pageContent = ""

        if linkList is None:
            pageContent += '<p>The army does not exist.</p>'
        else:
            armyInfo = linkList[1]
            pageTitle = armyInfo[2]
            linkList = linkList[0]
        
            pageContent += '\n<ul class="userList">'
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
        page = createPage(pageStyle, pageTitle, pageContent)
        return page

    @cherrypy.expose
    def userList(self):
        userList = displayUserList()
        pageStyle = 'userList'
        pageTitle = "Registered users"
        pageContent = ""

        pageContent += '\n<ul class="userList">'
        for user in userList:
            pageContent += '\n<li>'
            pageContent += '\n<div class="userDetails">'
            pageContent += f'\n<p>{user[2]} {user[1]}</p>'
            pageContent += f'\n<a href=/armyList?userID={user[0]}>Armies</a>'
            pageContent += '\n</div>'
            pageContent += '\n</li>'
        pageContent += '\n</ul>'

        pageContent += '\n'
        page = createPage(pageStyle, pageTitle, pageContent)
        return page




# Change these depending on the local installation
_dbUser = "root"
_dbPass = "root"
_dbName = "sae23"



def dbConnect():
    db = pymysql.connect(host='localhost', user=f'{_dbUser}', passwd=f'{_dbPass}', db=f'{_dbName}')
    return db

def dbDisconnect(db):
    db.commit()
    db.close()


def dbBackup(backupDir: str):
    db = dbConnect()
    c = db.cursor()

    if not os.path.exists(backupDir):
        createDir = input("The dir does not exist. Create it? [y/n]: ")
        if createDir.lower() == 'y':
            os.mkdir(backupDir)
        else:
            print("Aborting.")
            return None
    if os.path.exists(f"{backupDir}/units.csv") or os.path.exists(f"{backupDir}/armies.csv") or os.path.exists(f"{backupDir}/links.csv") or os.path.exists(f"{backupDir}/users.csv") or os.path.exists(f"{backupDir}/games.csv") or os.path.exists(f"{backupDir}/players.csv"):
        overwrite = input("Some of the backup files already exist. Overwrite them? [y/n]: ")
        if not overwrite.lower() == 'y':
            print("Aborting.")
            return None

    print("\nCreating backup files...")
    ## Units
    c.execute("select * from unit")
    units = c.fetchall()
    unitFile = open(f"./{backupDir}/units.csv", mode="w", encoding="utf-8")
       
    unitFile.write("ID; Name; Points; Models; Stats; Price; Tags;")
    for unit in units:
        unitFile.write(f"\n{unit[0]}; {unit[1]}; {unit[2]}; {unit[3]}; {unit[4]}; {unit[5]}; {unit[6]};")
    
    unitFile.close()


    ## Armies
    c.execute("select * from army")
    armies = c.fetchall()
    armyFile = open(f"./{backupDir}/armies.csv", mode="w", encoding="utf-8")
       
    armyFile.write("ID; Owner; Name; Points; Models; Price; Tags;")
    for army in armies:
        armyFile.write(f"\n{army[0]}; {army[1]}; {army[2]}; {army[3]}; {army[4]}; {army[5]}; {army[6]};")
    
    armyFile.close()

    c.execute("select * from armylink")
    links = c.fetchall()
    linkFile = open(f"./{backupDir}/links.csv", mode="w", encoding="utf-8")
       
    linkFile.write("ID; Army; Unit; Quantity;")
    for link in links:
        linkFile.write(f"\n{link[0]}; {link[1]}; {link[2]}; {link[3]};")
    
    linkFile.close()


    ## Users
    c.execute("select * from player")
    users = c.fetchall()
    userFile = open(f"./{backupDir}/users.csv", mode="w", encoding="utf-8")
       
    userFile.write("ID; Last Name; First Name")
    for user in users:
        userFile.write(f"\n{user[0]}; {user[1]}; {user[2]};")
    
    userFile.close()


    ## Games
    c.execute("select * from game")
    games = c.fetchall()
    gameFile = open(f"./{backupDir}/games.csv", mode="w", encoding="utf-8")
       
    gameFile.write("ID; Date; Rules; Length; Winner;")
    for game in games:
        gameFile.write(f"\n{game[0]}; {game[1]}; {game[2]}; {game[3]}; {game[4]};")
    
    gameFile.close()

    c.execute("select * from gameplayer")
    players = c.fetchall()
    playerFile = open(f"./{backupDir}/players.csv", mode="w", encoding="utf-8")
       
    playerFile.write("ID; Game; Player; Army;")
    for player in players:
        playerFile.write(f"\n{player[0]}; {player[1]}; {player[2]}; {player[3]};")
    
    playerFile.close()


    dbDisconnect(db)

    print("Backup complete.")
    return None

def dbRestore():
    db = pymysql.connect(host="localhost", user=f"{_dbUser}", passwd=f"{_dbPass}")
    c = db.cursor()
    database = f"{_dbName}"
    
    ## Database creation
    print("\n --- Database restore --- ")
    try:
        c.execute(f"USE {database}")
        print("Database already exists. Dropping and recreating...")
        c.execute(f"DROP DATABASE {database}")
    except pymysql.err.OperationalError:
        print("Database does not exist. Creating...")
    finally:
        c.execute(f"CREATE DATABASE {database}")
    print("Database created.")
    c.execute(f"USE {database}")

    ## Tables creation
    print("\nCreating tables...")

    c.execute("CREATE TABLE `army` (`Id` int(11) NOT NULL, `Owner` int(11) DEFAULT NULL, `Name` varchar(50) NOT NULL, `Points` int(11) DEFAULT NULL, `Models` int(11) DEFAULT NULL, `Price` float DEFAULT NULL, `Tags` text NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=latin1;")
    c.execute("CREATE TABLE `armylink` (`Id` int(11) NOT NULL, `ArmyId` int(11) NOT NULL, `UnitId` int(11) NOT NULL, `Quantity` int(11) NOT NULL DEFAULT '1') ENGINE=InnoDB DEFAULT CHARSET=latin1;")
    c.execute("CREATE TABLE `game` (`Id` int(11) NOT NULL, `Date` date NOT NULL, `Rules` varchar(50) NOT NULL, `Length` int(11) NOT NULL, `Winner` int(11) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=latin1;")
    c.execute("CREATE TABLE `gameplayer` (`Id` int(11) NOT NULL, `GameId` int(11) NOT NULL, `PlayerId` int(11) NOT NULL, `ArmyId` int(11) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=latin1;")
    c.execute("CREATE TABLE `player` (`Id` int(11) NOT NULL, `Name` varchar(50) NOT NULL, `FirstName` varchar(50) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=latin1;")
    c.execute("CREATE TABLE `unit` (`Id` int(11) NOT NULL, `Name` varchar(50) NOT NULL, `Points` int(11) NOT NULL, `Models` int(11) NOT NULL, `Stats` text NOT NULL, `Price` float NOT NULL, `Tags` text NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=latin1;")

    c.execute("ALTER TABLE `army` ADD PRIMARY KEY (`Id`), ADD KEY `Owner` (`Owner`);")
    c.execute("ALTER TABLE `armylink` ADD PRIMARY KEY (`Id`), ADD KEY `ArmyName` (`ArmyId`), ADD KEY `UnitId` (`UnitId`);")
    c.execute("ALTER TABLE `game` ADD PRIMARY KEY (`Id`);")
    c.execute("ALTER TABLE `gameplayer` ADD PRIMARY KEY (`Id`), ADD KEY `GameId` (`GameId`,`PlayerId`,`ArmyId`), ADD KEY `PlayerId` (`PlayerId`), ADD KEY `ArmyId` (`ArmyId`);")
    c.execute("ALTER TABLE `player` ADD PRIMARY KEY (`Id`);")
    c.execute("ALTER TABLE `unit` ADD PRIMARY KEY (`Id`);")

    c.execute("ALTER TABLE `army` MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;")
    c.execute("ALTER TABLE `armylink` MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT;")
    c.execute("ALTER TABLE `game` MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT;")
    c.execute("ALTER TABLE `gameplayer` MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT;")
    c.execute("ALTER TABLE `player` MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;")
    c.execute("ALTER TABLE `unit` MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;")

    c.execute("ALTER TABLE `army` ADD CONSTRAINT `army_ibfk_1` FOREIGN KEY (`Owner`) REFERENCES `player` (`Id`) ON DELETE SET NULL ON UPDATE CASCADE;")
    c.execute("ALTER TABLE `armylink` ADD CONSTRAINT `armylink_ibfk_1` FOREIGN KEY (`ArmyId`) REFERENCES `army` (`Id`) ON UPDATE CASCADE, ADD CONSTRAINT `armylink_ibfk_2` FOREIGN KEY (`UnitId`) REFERENCES `unit` (`Id`) ON UPDATE CASCADE;")
    c.execute("ALTER TABLE `gameplayer` ADD CONSTRAINT `gameplayer_ibfk_1` FOREIGN KEY (`GameId`) REFERENCES `game` (`Id`), ADD CONSTRAINT `gameplayer_ibfk_2` FOREIGN KEY (`PlayerId`) REFERENCES `player` (`Id`), ADD CONSTRAINT `gameplayer_ibfk_3` FOREIGN KEY (`ArmyId`) REFERENCES `army` (`Id`);")



    print("Tables created.")

    ## Backed rows insertion
    insertRows = input("\nWould you like to insert backed rows into the tables? [y/n]: ")
    if insertRows.lower() == 'y':
        backupDir = input("Enter path to backup directory (leave blank to use default directory): ")
        if backupDir == "" and os.path.exists("DB backup"):
            backupDir = "DB backup"
        elif backupDir == "" and not os.path.exists("DB backup"):
            print("Default directory not detected.")
            print("Aborting insertion of backed rows.")
            print(" --- Restore complete --- ")
            return None
        elif not os.path.exists(backupDir) and os.path.exists("DB backup"):
            print("Directory does not exist, using default directory.")
            backupDir = "DB backup"
        elif not os.path.exists(backupDir) and not os.path.exists("DB backup"):
            print("Directory does not exist, default directory not detected.")
            print("Aborting insertion of backed rows.")
            print(" --- Restore complete --- ")
            return None
        
        print("\nInserting rows...")

        ## player
        playerFile = open(f"./{backupDir}/users.csv", mode="r", encoding="utf-8")
        playerReader = csv.reader(playerFile, delimiter=";")
        next(playerReader)
        for player in playerReader:
            c.execute(f"INSERT INTO player VALUES ('{player[0]}', '{player[1]}', '{player[2]}')")
        playerFile.close()

        ## unit
        unitFile = open(f"./{backupDir}/units.csv", mode="r", encoding="utf-8")
        unitReader = csv.reader(unitFile, delimiter=";")
        next(unitReader)
        for unit in unitReader:
            c.execute(f"INSERT INTO unit VALUES ('{unit[0]}', '{unit[1]}', '{unit[2]}', '{unit[3]}', '{unit[4]}', '{unit[5]}', '{unit[6]}')")
        unitFile.close()
        
        ## army
        armyFile = open(f"./{backupDir}/armies.csv", mode="r", encoding="utf-8")
        armyReader = csv.reader(armyFile, delimiter=";")
        next(armyReader)
        for army in armyReader:
            c.execute(f"INSERT INTO army VALUES ('{army[0]}', '{army[1]}', '{army[2]}', '{army[3]}', '{army[4]}', '{army[5]}', '{army[6]}')")
        armyFile.close()

        ## armylink
        linkFile = open(f"./{backupDir}/links.csv", mode="r", encoding="utf-8")
        linkReader = csv.reader(linkFile, delimiter=";")
        next(linkReader)
        for link in linkReader:
            c.execute(f"INSERT INTO armylink VALUES ('{link[0]}', '{link[1]}', '{link[2]}', '{link[3]}')")
        linkFile.close()

        ## game
        gameFile = open(f"./{backupDir}/games.csv", mode="r", encoding="utf-8")
        gameReader = csv.reader(gameFile, delimiter=";")
        next(gameReader)
        for game in gameReader:
            c.execute(f"INSERT INTO game VALUES ('{game[0]}', '{game[1]}', '{game[2]}', '{game[3]}', '{game[4]}')")
        gameFile.close()

        ## gameplayer
        playerFile = open(f"./{backupDir}/players.csv", mode="r", encoding="utf-8")
        playerReader = csv.reader(playerFile, delimiter=";")
        next(playerReader)
        for player in playerReader:
            c.execute(f"INSERT INTO gameplayer VALUES ('{player[0]}', '{player[1]}', '{player[2]}', '{player[3]}')")
        playerFile.close()

        print("Rows inserted.")


    
    
    dbDisconnect(db)
    print(" --- Restore complete --- ")
    return None



def testFunction():
    db = dbConnect()
    c = db.cursor()
    c.execute("select * from unit;")
    print(c.fetchall())

    # c.execute("INSERT INTO `unit` (`Id`, `Name`, `Points`, `Models`, `Stats`, `Price`, `Tags`) VALUES (NULL, 'test2', '10', '2', '{}', '15.2', '{}')")
    # c.execute("select * from unit;")
    # print(c.fetchall())

    dbDisconnect(db)
    return None


def createPage(style: str, title: str, content: str):
    filePath = "./sources/index.html"
    templateFile = open(filePath, mode='r')
    returnContent = ""
    for line in templateFile.readlines():
        returnContent += line
        if "PAGE_STYLE" in line:
            returnContent += f'<link rel="stylesheet" type="text/css" href="/templates/css/{style}.css">'
        if "PAGE_TITLE" in line:
            returnContent += '<h1 id="titre">' + title + '</h1>'
        if "PAGE_CONTAINER" in line:
            returnContent += content
    print(returnContent)
    return returnContent



## ---------------------------
## ----- Unit management -----
## ---------------------------
def createUnit():
    print()
    name = input("Enter unit name: ")

    ## Points
    pointsNotSet = True
    while pointsNotSet:
        try:
            points = int(input("Enter number of points: "))
            pointsNotSet = False
        except ValueError:
            print("The value entered is incorrect")
    
    ## Models
    modelNumberNotSet = True
    while modelNumberNotSet:
        try:
            models = int(input("Enter number of models: "))
            modelNumberNotSet = False
        except ValueError:
            print("The value entered is incorrect")

    ## Stats
    movementNotSet = True
    while movementNotSet:
        try:
            statMovement = int(input("Enter unit movement range, in inches: "))
            movementNotSet = False
        except ValueError:
            print("The value entered is incorrect")
    
    toughnessNotSet = True
    while toughnessNotSet:
        try:
            statToughness = int(input("Enter unit toughness: "))
            toughnessNotSet = False
        except ValueError:
            print("The value entered is incorrect")
    
    armourNotSet = True
    while armourNotSet:
        try:
            statArmour = int(input("Enter unit armour save, excluding the '+': "))
            armourNotSet = False
        except ValueError:
            print("The value entered is incorrect")

    woundsNotSet = True
    while woundsNotSet:
        try:
            statWounds = int(input("Enter unit wounds: "))
            woundsNotSet = False
        except ValueError:
            print("The value entered is incorrect")

    leadershipNotSet = True
    while leadershipNotSet:
        try:
            statLeadership = int(input("Enter unit leadership, excluding the '+': "))
            leadershipNotSet = False
        except ValueError:
            print("The value entered is incorrect")

    ocNotSet = True
    while ocNotSet:
        try:
            statOC = int(input("Enter unit objective control: "))
            ocNotSet = False
        except ValueError:
            print("The value entered is incorrect")

    invulnNotSet = True
    while invulnNotSet:
        try:
            statInvulnSave = int(input("Enter unit invulnerable save, excluding the '+': "))
            invulnNotSet = False
        except ValueError:
            print("The value entered is incorrect")

    stats = {
        "movement" : statMovement,
        "toughness" : statToughness,
        "armour save" : statArmour,
        "wounds" : statWounds,
        "leadership" : statLeadership,
        "objective control" : statOC,
        "invulnerable save" : statInvulnSave
    }
    jsonStats = json.dumps(stats)

    ## Price
    priceNotSet = True
    while priceNotSet:
        try:
            price = float(input("Enter price: "))
            priceNotSet = False
        except ValueError:
            print("The value entered is incorrect")
    
    
    tags = {
        "faction" : input("Enter unit faction: "),
        "keywords" : []
    }
    keepGoing = True
    while keepGoing:
        keyword = input("Enter unit keyword, leave blank to quit: ")
        if keyword == '':
            keepGoing = False
        else:
            tags["keywords"].append(keyword)
    jsonTags = json.dumps(tags)


    db = dbConnect()
    c = db.cursor()
    c.execute(f"INSERT INTO `unit` (`Id`, `Name`, `Points`, `Models`, `Stats`, `Price`, `Tags`) VALUES (NULL, '{name}', '{points}', '{models}', '{jsonStats}', '{price}', '{jsonTags}')")
    dbDisconnect(db)

    print("\nUnit created.")
    return None


def modifyUnit(unitID: int):
    db = dbConnect()
    c = db.cursor()

    c.execute(f"SELECT * FROM army WHERE Id = {unitID}")
    if c.fetchone() == None:
        print("\nThe army does not exist.")
        return None

    dbDisconnect(db)

    while True:
        print("\n1. Change unit name")
        print("2. Change unit stats")
        print("3. Change unit model number")
        print("4. Change unit point number")
        print("5. Change unit faction")
        print("6. Change unit tags")
        print("7. Change unit price")
        print("0. Quit")
        operation = input("What would you like to do?: ")
        print()
        match operation:
            case '1':
                unitName = input("Enter unit name: ")
                
                db = dbConnect()
                c = db.cursor()
                c.execute(f"UPDATE unit SET Name = '{unitName}' WHERE Id = {unitID}")
                dbDisconnect(db)
            case '2':
                movementNotSet = True
                while movementNotSet:
                    try:
                        statMovement = int(input("Enter unit movement range, in inches: "))
                        movementNotSet = False
                    except ValueError:
                        print("The value entered is incorrect")
                
                toughnessNotSet = True
                while toughnessNotSet:
                    try:
                        statToughness = int(input("Enter unit toughness: "))
                        toughnessNotSet = False
                    except ValueError:
                        print("The value entered is incorrect")
                
                armourNotSet = True
                while armourNotSet:
                    try:
                        statArmour = int(input("Enter unit armour save, excluding the '+': "))
                        armourNotSet = False
                    except ValueError:
                        print("The value entered is incorrect")

                woundsNotSet = True
                while woundsNotSet:
                    try:
                        statWounds = int(input("Enter unit wounds: "))
                        woundsNotSet = False
                    except ValueError:
                        print("The value entered is incorrect")

                leadershipNotSet = True
                while leadershipNotSet:
                    try:
                        statLeadership = int(input("Enter unit leadership, excluding the '+': "))
                        leadershipNotSet = False
                    except ValueError:
                        print("The value entered is incorrect")

                ocNotSet = True
                while ocNotSet:
                    try:
                        statOC = int(input("Enter unit objective control: "))
                        ocNotSet = False
                    except ValueError:
                        print("The value entered is incorrect")

                invulnNotSet = True
                while invulnNotSet:
                    try:
                        statInvulnSave = int(input("Enter unit invulnerable save, excluding the '+': "))
                        invulnNotSet = False
                    except ValueError:
                        print("The value entered is incorrect")

                stats = {
                    "movement" : statMovement,
                    "toughness" : statToughness,
                    "armour save" : statArmour,
                    "wounds" : statWounds,
                    "leadership" : statLeadership,
                    "objective control" : statOC,
                    "invulnerable save" : statInvulnSave
                }
                jsonStats = json.dumps(stats)

                db = dbConnect()
                c = db.cursor()
                c.execute(f"UPDATE unit SET Stats = '{jsonStats}' WHERE Id = {unitID}")
                dbDisconnect(db)
            case '3':
                modelNumberNotSet = True
                while modelNumberNotSet:
                    try:
                        models = int(input("Enter number of models: "))
                        modelNumberNotSet = False
                    except ValueError:
                        print("The value entered is incorrect")

                db = dbConnect()
                c = db.cursor()
                c.execute(f"UPDATE unit SET Models = '{models}' WHERE Id = {unitID}")
                dbDisconnect(db)
            case '4':
                pointsNotSet = True
                while pointsNotSet:
                    try:
                        points = int(input("Enter number of points: "))
                        pointsNotSet = False
                    except ValueError:
                        print("The value entered is incorrect")
                
                db = dbConnect()
                c = db.cursor()
                c.execute(f"UPDATE unit SET Points = '{points}' WHERE Id = {unitID}")
                dbDisconnect(db)
            case '5':
                db = dbConnect()
                c = db.cursor()

                c.execute(f"SELECT Tags FROM unit WHERE Id = {unitID}")
                unitInfo = c.fetchone()
                unitTags = json.loads(unitInfo[0])
                unitFaction = input("Enter unit name: ")
                unitTags["faction"] = unitFaction
                jsonTags = json.dumps(unitTags)

                c.execute(f"UPDATE unit SET Tags = '{jsonTags}' WHERE Id = {unitID}")
                dbDisconnect(db)
            case '6':
                db = dbConnect()
                c = db.cursor()

                c.execute(f"SELECT Tags FROM unit WHERE Id = {unitID}")
                unitTags = json.loads(c.fetchone()[0])
                unitTags["keywords"] = []

                keepGoing = True
                while keepGoing:
                    keyword = input("Enter unit keyword, leave blank to quit: ")
                    if keyword == '':
                        keepGoing = False
                    else:
                        unitTags["keywords"].append(keyword)
                
                jsonTags = json.dumps(unitTags)
                
                c.execute(f"UPDATE unit SET Tags = '{jsonTags}' WHERE Id = {unitID}")
                dbDisconnect(db)
            case '7':
                priceNotSet = True
                while priceNotSet:
                    try:
                        unitPrice = float(input("Enter price: "))
                        priceNotSet = False
                    except ValueError:
                        print("The value entered is incorrect")
            
                db = dbConnect()
                c = db.cursor()
                c.execute(f"UPDATE unit SET Price = '{unitPrice}' WHERE Id = {unitID}")
                dbDisconnect(db)
            case '0':
                return True


def displayUnitList(filters):
    db = dbConnect()
    c = db.cursor()

    c.execute("SELECT * FROM unit")
    print(f"\n ----- Units available - Filters: {filters} -----")
    toPrint = []
    unitList = c.fetchall()
    for unitInfo in unitList:
        unitTags = json.loads(unitInfo[6])
        toPrint.append(unitInfo)
        if filters["faction"] != "" and unitTags["faction"] != filters["faction"]:
            toPrint.pop()
        else:
            for tag in filters["keywords"]:
                if tag not in unitTags["keywords"]:
                    toPrint.pop()
                    break
    
    for unit in toPrint:
        print(f"{unit[1]} - Unit ID:{unit[0]}")

    dbDisconnect(db)
    return toPrint


def displayUnitInformation(unitID: int):
    db = dbConnect()
    c = db.cursor()

    c.execute(f"select * from unit where Id={unitID}")
    unitInfo = c.fetchone()
    if unitInfo == None:
        print(f"\nThe unit with ID {unitID} does not exist.")
    else:
        stats = json.loads(unitInfo[4])
        tags = json.loads(unitInfo[6])
        print(f"\n ----- {unitInfo[1]} -----")
        print(f"Movement: \t\t", stats["movement"])
        print(f"Toughness: \t\t", stats["toughness"])
        print(f"Armour save: \t\t", stats["armour save"], "+")
        print(f"Wounds: \t\t", stats["wounds"])
        print(f"Leadership: \t\t", stats["leadership"], "+")
        print(f"Objective control: \t", stats["objective control"])
        print(f"Invulnerable save: \t", stats["invulnerable save"], "+")
        print(f"\nPoints: ", unitInfo[2])
        print(f"Models: ", unitInfo[3])
        print(f"\nCost: ", unitInfo[5], "euros")

    dbDisconnect(db)
    return unitInfo




## ---------------------------
## ----- Army management -----
## ---------------------------
def createArmy():
    # showUsers = input("Would you like to see the available users? [y/n]: ")
    # if showUsers.lower() == 'y':
    #     displayUserList()
    ownerNotSet = True
    while ownerNotSet:
        try:
            userID = int(input("\nEnter the owner's ID: "))
            ownerNotSet = False
        except ValueError:
            print("The value entered is incorrect")
    armyName = input("Enter the army's name: ")
    armyPoints = 0
    armyModels = 0
    armyPrice = 0
    armyTags = {}

    db = dbConnect()
    c = db.cursor()

    try:
        c.execute(f"INSERT INTO army (Owner, Name, Points, Models, Price, Tags) VALUES ('{userID}', '{armyName}', '{armyPoints}', '{armyModels}', '{armyPrice}', '{armyTags}')")
        c.execute("SELECT LAST_INSERT_ID()")
        returnValue = c.fetchone()
        dbDisconnect(db)
        print("\nArmy created. The new army ID is: ", int(returnValue[0]))
    except pymysql.err.IntegrityError:
        print("\nInvalid owner ID")
    except Exception as e:
        print("\nUnknown error: ", e)

    return None


def modifyArmy(armyID: int):
    db = dbConnect()
    c = db.cursor()

    c.execute(f"SELECT * FROM army WHERE Id = {armyID}")
    if c.fetchone() == None:
        print("\nThe army does not exist.")
        return None

    dbDisconnect(db)

    while True:
        print("\n1. Change army name")
        print("2. Change army owner")
        print("3. Add unit to army")
        print("4. Remove unit from army")
        print("0. Quit")
        operation = input("What would you like to do?: ")
        print()
        match operation:
            case '1':
                armyName = input("Enter army name: ")
                
                db = dbConnect()
                c = db.cursor()
                c.execute(f"UPDATE army SET Name = '{armyName}' WHERE Id = {armyID}")
                dbDisconnect(db)
            case '2':
                # showUsers = input("Would you like to see the available users? [y/n]: ")
                # if showUsers.lower() == 'y':
                #     displayUserList()
                ownerNotSet = True
                while ownerNotSet:
                    try:
                        userID = int(input("\nEnter the owner's ID: "))
                        ownerNotSet = False
                    except ValueError:
                        print("The value entered is incorrect")

                db = dbConnect()
                c = db.cursor()
                try:
                    c.execute(f"UPDATE army SET Owner = '{userID}' WHERE army.Id = {armyID}")
                    dbDisconnect(db)
                except pymysql.err.IntegrityError:
                    print("\nInvalid owner ID")
                except Exception as e:
                    print("\nUnknown error: ", e)
            case '3':
                idNotSet = True
                while idNotSet:
                    try:
                        unitID = int(input("Enter the unit's ID: "))
                        idNotSet = False
                    except ValueError:
                        print("The value entered is incorrect")
                
                quantityNotSet = True
                while quantityNotSet:
                    try:
                        unitQuantity = int(input("Enter the quantity of units: "))
                        quantityNotSet = False
                    except ValueError:
                        print("The value entered is incorrect")
                
                db = dbConnect()
                c = db.cursor()

                try:
                    c.execute(f"INSERT INTO armylink (ArmyID, UnitId, Quantity) VALUES ('{armyID}', '{unitID}', '{unitQuantity}')")
                    c.execute(f"SELECT * from army WHERE Id = {armyID}")
                    armyInfo = c.fetchone()
                    c.execute(f"SELECT * from unit WHERE Id = {unitID}")
                    unitInfo = c.fetchone()
                    newPoints = armyInfo[3] + unitInfo[2] * unitQuantity
                    newModels = armyInfo[4] + unitInfo[3] * unitQuantity
                    newPrice = armyInfo[5] + unitInfo[5] * unitQuantity
                    newTags = armyInfo[6]
                    c.execute(f"UPDATE army SET Points = '{newPoints}', Models = '{newModels}', Price = '{newPrice}' WHERE army.Id = {armyID}")

                    dbDisconnect(db)
                except pymysql.err.IntegrityError:
                    print("\nInvalid unit ID")
                except Exception as e:
                    print("\nUnknown error: ", e)
            case '4':
                idNotSet = True
                while idNotSet:
                    try:
                        unitID = int(input("Enter the unit's ID: "))
                        idNotSet = False
                    except ValueError:
                        print("The value entered is incorrect")

                
                db = dbConnect()
                c = db.cursor()

                c.execute(f"SELECT * from army WHERE Id = {armyID}")
                armyInfo = c.fetchone()
                c.execute(f"SELECT * FROM unit WHERE Id = '{unitID}'")
                unitInfo = c.fetchone()
                c.execute(f"SELECT * FROM armylink WHERE ArmyId = '{armyID}' AND UnitId = '{unitID}'")
                newPoints = armyInfo[3]
                newModels = armyInfo[4]
                newPrice = armyInfo[5]
                for link in c.fetchall():
                    newPoints = newPoints - unitInfo[2] * link[3]
                    newModels = newModels - unitInfo[3] * link[3]
                    newPrice = newPrice - unitInfo[5] * link[3]
                    c.execute(f"UPDATE army SET Points = '{newPoints}', Models = '{newModels}', Price = '{newPrice}' WHERE army.Id = {armyID}")
                    c.execute(f"DELETE FROM armylink WHERE armylink.Id = '{link[0]}'")

                dbDisconnect(db)
            case '0':
                return None


def displayArmyList(filters):
    if filters == {}:
        command = "select * from army"
    else:
        print("Not implemented yet.")


    db = dbConnect()
    c = db.cursor()

    c.execute(command)
    armyList = c.fetchall()
    print("\n ----- Armies available -----")
    for army in armyList:
        print(f"{army[2]} - Army ID: {army[0]}")

    dbDisconnect(db)
    return armyList


def displayArmyInformation(armyID: int):
    db = dbConnect()
    c = db.cursor()

    c.execute(f"SELECT * FROM army WHERE Id = {armyID}")
    armyInfo = c.fetchone()
    if armyInfo == None:
        print("\nThe army does not exist.")
        return None
    print(f"\n ----- {armyInfo[2]} -----")
    c.execute(f"SELECT * FROM armylink JOIN unit WHERE ArmyId = {armyID} AND armylink.UnitId = unit.Id;")
    unitCount = 0
    linkList = c.fetchall()
    for link in linkList:
        print(f"{link[3]} x {link[5]} - {link[6]*link[3]} points, {link[7]*link[3]} models")
        unitCount += link[3]
    print(f"Total -  Units: {unitCount}, Points: {armyInfo[3]}, Models: {armyInfo[4]}")

    dbDisconnect(db)
    return linkList, armyInfo




## ---------------------------
## ----- Game management -----
## ---------------------------
def createGame():
    return None


def modifyGame(gameID):
    return None


def displayGameList():
    return None


def diplayGameInformation():
    return None




## ---------------------------
## ----- User management -----
## ---------------------------
def createUser():
    name = input("Enter user last name: ")
    firstName = input("Enter user first name: ")

    db = dbConnect()
    c = db.cursor()
    c.execute(f"INSERT INTO `player` (`Id`, `Name`, `FirstName`) VALUES (NULL, '{name}', '{firstName}')")
    dbDisconnect(db)
    
    print("\nUser created.")
    return None


def deleteUser(userID: int):
    db = dbConnect()
    c = db.cursor()

    c.execute(f"SELECT * FROM player WHERE Id = {userID}")
    userInfo = c.fetchone()
    if userInfo == None:
        print("\nThe user does not exist.")
        return None
    c.execute(f"DELETE FROM player WHERE Id = {userID}")

    dbDisconnect(db)
    print("\nUser deleted.")
    return None


def displayUserList():
    db = dbConnect()
    c = db.cursor()

    c.execute("SELECT * FROM player")
    userList = c.fetchall()
    print("\n ----- Registered users -----")
    for user in c.fetchall():
        print(f"{user[0]} - {user[2]} {user[1]}")
    return userList






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
        print(" --- Game Management - Not implemented yet ---")
        print("7. View recorded games")
        print("71. View specific game information")
        print("8. Create game")
        print("81. Modify game")
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
                displayUnitList(filters)                                                                                     ## Done
            case '11':
                try:
                    unitID = int(input("Enter unit ID: "))
                    displayUnitInformation(unitID)                                                                          ## Done
                except ValueError:
                    print("\nThe value entered is incorrect\n")
                except:
                    print("Unknown error")
            case '2':
                createUnit()                                                                                                ## Done
            case '21':
                unitID = input("Enter unit ID: ") 
                modifyUnit(unitID)                                                                                          ## Done

            case '3':
                # doFilters = input("Would you like to apply some filter? [y/n]: ")
                # if doFilters == 'y':
                #     ## Filter choice
                #     pass
                filters = {}
                displayArmyList(filters)                                                                                     ## Done, add filters feature?
            case '31':
                idNotSet = True
                while idNotSet:
                    try:
                        armyID = int(input("Enter army ID: "))
                        idNotSet = False
                    except ValueError:
                        print("The value entered is incorrect")
                displayArmyInformation(armyID)                                                                              ## Done
            case '4':
                createArmy()                                                                                                ## Done
            case '41':
                armyID = input("Enter army ID: ") 
                modifyArmy(armyID)                                                                                          ## Done

            case '5':
                displayUserList()                                                                                           ## Done
            case '6':
                createUser()                                                                                                ## Done
            case '61':
                idNotSet = True
                while idNotSet:
                    try:
                        userID = int(input("Enter user ID: "))
                        idNotSet = False
                    except ValueError:
                        print("The value entered is incorrect")
                deleteUser(userID)                                                                                                ## Done

            case '7':
                doFilters = input("Would you like to apply some filter? [y/n]: ")
                if doFilters == 'y':
                    ## Filter choice
                    pass
                displayGameList(filters)                                                                                     ## To do
            case '71':
                armyID = input("Enter game ID: ") 
                diplayGameInformation(armyID)                                                                               ## To do
            case '8':
                createGame()                                                                                                ## To do
            case '81':
                gameID = input("Enter game ID: ") 
                modifyGame(gameID)

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
                dbBackup(backupDir)
            case 'R' | 'r':
                dbRestore()

            case '9':
                testFunction()                                                                                              ## lol
            case '0':
                keepGoing = False
                break
        input("\nPress enter to continue...")
        print()
    print("And a good day to you!")


