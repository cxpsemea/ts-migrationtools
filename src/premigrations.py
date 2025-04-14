import json
import os
from shared.package.common import cxutils
from shared.package.common.cxconfig import cxconfig
from shared.package.common.cxcsv import CxCsv
from shared.package.common.cxlogging import cxlogger


PROJS_JSON_FILE: str = "projects.json"
PROJS_MAPS_FILE: str = "projects.csv"

GROUPS_JSON_FILE: str = "teams.json"
GROUPS_MAPS_FILE: str = "groups.csv"


class CxPreImporter() :

    def __init__(self) :
        self.__cxcsv: CxCsv = None


    @property
    def csv(self) -> CxCsv :
        if not self.__cxcsv :
            self.__cxcsv = CxCsv()
        return self.__cxcsv


    def processprojectnames(self) :
        # Location for "projects.json" exported file
        # xjsonorig: str = cxconfig.getvalue("names.folder")
        xjsonorig: str = cxconfig.getvalue("export-folder")
        if not xjsonorig :
            xjsonorig = cxutils.application_path() + os.sep + PROJS_JSON_FILE
        elif not xjsonorig.endswith(os.sep + PROJS_JSON_FILE) :
            xjsonorig = xjsonorig + os.sep + PROJS_JSON_FILE
        # Check existance of "projects.json" exported file
        if not os.path.exists(xjsonorig) :
            raise FileNotFoundError('A SAST exported file "' + PROJS_JSON_FILE + '" was not found')

        # Existance of project name mappings file
        xmapsfile: str = cxutils.application_path() + os.sep + PROJS_MAPS_FILE
        if not os.path.exists(xmapsfile) :
            raise FileNotFoundError('The projects mapping file "' + PROJS_MAPS_FILE + '" was not found')
        # Check csv separator to use
        self.csv.csvseparatorfromfile(xmapsfile)

        # Load the mappings file
        projects, columns = self.csv.csvload( xmapsfile, True )

        # Check source name column name (mandatory)
        xsrccolumn: str = None
        if ("NAME" in columns) :
            xsrccolumn = "NAME"
        elif ("SAST" in columns) :
            xsrccolumn = "SAST"
        elif ("SAST-NAME" in columns) :
            xsrccolumn = "SAST-NAME"
        if not xsrccolumn :
            raise Exception( 'Column with source SAST project name not found in csv file')
        # Check destination name column name (mandatory)
        xdestcolumn: str = None
        if ("NEW-NAME" in columns) :
            xdestcolumn = "NEW-NAME"
        elif ("CXONE" in columns) :
            xdestcolumn = "CXONE"
        elif ("CXONE-NAME" in columns) :
            xdestcolumn = "CXONE-NAME"
        if not xdestcolumn :
            raise Exception( 'Column with destination CXONE project name not found in csv file')

        # Load json file
        with open(xjsonorig, "r", encoding = "utf-8") as f:
            xjsonsrc: list[dict] = json.load(f)
        if not isinstance(xjsonsrc, list):
            raise Exception( 'Expected a JSON array (list of objects) in file "projects.json"')

        xjsondest: list[dict] = []
        # Process it
        for project in xjsonsrc :
            destname: str = None
            srcname: str = project.get("name")
            # Find mapping
            if srcname :
                destref: dict = next( filter( lambda el: el[xsrccolumn] == srcname, projects ), None )
                if destref :
                    destname = destref.get(xdestcolumn)
            # Have a mapping ?
            if destname :
                project["name"] = destname
                xjsondest.append(project)
                cxlogger.info( 'Project "' + srcname + '" renamed to "' + destname + '"')
            else :
                cxlogger.warning( 'Mapping for project "' + srcname + '" not found, ignoring')

        # Save the updated projects file
        with open(xjsonorig, "w", encoding="utf-8") as f:
            json.dump(xjsondest, f, ensure_ascii = False, indent = None)


    def processgroupnames(self) :
        # Location for "teams.json" exported file
        # xjsonorig: str = cxconfig.getvalue("names.folder")
        xjsonorig: str = cxconfig.getvalue("export-folder")
        if not xjsonorig :
            xjsonorig = cxutils.application_path() + os.sep + GROUPS_JSON_FILE
        elif not xjsonorig.endswith(os.sep + GROUPS_JSON_FILE) :
            xjsonorig = xjsonorig + os.sep + GROUPS_JSON_FILE
        # Check existance of "teams.json" exported file
        if not os.path.exists(xjsonorig) :
            raise FileNotFoundError('A SAST exported file "' + GROUPS_JSON_FILE + '" was not found')

        # Existance of teams name mappings file
        xmapsfile: str = cxutils.application_path() + os.sep + GROUPS_MAPS_FILE
        if not os.path.exists(xmapsfile) :
            raise FileNotFoundError('The projects mapping file "' + GROUPS_MAPS_FILE + '" was not found')
        # Check csv separator to use
        self.csv.csvseparatorfromfile(xmapsfile)

        # Load the mappings file
        groups, columns = self.csv.csvload( xmapsfile, True )

        # Check source name column name (mandatory)
        xsrccolumn: str = None
        if ("TEAM-NAME" in columns) :
            xsrccolumn = "TEAM-NAME"
        elif ("SAST-TEAM" in columns) :
            xsrccolumn = "SAST-TEAM"
        elif ("SAST-TEAM-NAME" in columns) :
            xsrccolumn = "SAST-TEAM-NAME"
        if not xsrccolumn :
            raise Exception( 'Column with source SAST team name not found in csv file')
        # Check destination name column name (mandatory)
        xdestcolumn: str = None
        if ("NEW-TEAM-NAME" in columns) :
            xdestcolumn = "NEW-TEAM-NAME"
        elif ("CXONE-GROUP" in columns) :
            xdestcolumn = "CXONE-GROUP"
        elif ("CXONE-GROUP-NAME" in columns) :
            xdestcolumn = "CXONE-GROUP-NAME"
        if not xdestcolumn :
            raise Exception( 'Column with destination CXONE group name not found in csv file')

        # Load json file
        with open(xjsonorig, "r", encoding = "utf-8") as f:
            xjsonsrc: list[dict] = json.load(f)
        if not isinstance(xjsonsrc, list):
            raise Exception( 'Expected a JSON array (list of objects) in file "teams.json"')

        xjsondest: list[dict] = []
        # Process it
        for team in xjsonsrc :
            destname: str = None
            destfullname: str = None
            srcfullname: str = team.get("fullName")

            if srcfullname :
                # Find mapping, non fatten
                destref: dict = next( filter( lambda el: el[xsrccolumn] == srcfullname, groups ), None )
                if destref :
                    destfullname = destref.get(xdestcolumn)
                if not destfullname :
                    srcfullname = "/" + srcfullname.replace("/", " ").strip()
                    destref: dict = next( filter( lambda el: el[xsrccolumn] == srcfullname, groups ), None )
                    if destref :
                        destfullname = destref.get(xdestcolumn)

            # Resolve group small name, if present
            if destfullname :
                xlist: list[str] = destfullname.split("/")
                destname = xlist[len(xlist) - 1]

            # Have a mapping ?
            if destname and destfullname:
                team["name"] = destname
                team["fullName"] = destfullname
                xjsondest.append(team)
                cxlogger.info( 'Team "' + srcfullname + '" renamed to group "' + destfullname + '"')
            else :
                cxlogger.warning( 'Mapping for team "' + srcfullname + '" not found, ignoring')

        # Save the updated projects file
        with open(xjsonorig, "w", encoding="utf-8") as f:
            json.dump(xjsondest, f, ensure_ascii = False, indent = None)
